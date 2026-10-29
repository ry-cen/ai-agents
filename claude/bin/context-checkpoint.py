#!/usr/bin/env python3
"""Fail-open Claude context reminders; no transcript text is persisted."""
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import sys
import tempfile

SCAN_LIMIT = 4 * 1024 * 1024
INPUT_LIMIT = 1024 * 1024
EVENTS = {"PostToolUse", "UserPromptSubmit"}
ADVISORY = (
    "Context is at least 100k tokens. Read targeted file ranges, report concise "
    "results, and load only the brief sections needed for the current step."
)
CHECKPOINT = (
    "Context is at least 150k tokens. Save a concise handoff with acceptance "
    "criteria, checkout/commit, current decisions, unresolved findings, and "
    "verification. Finish the current bounded step, then recommend compact to "
    "continue this task or a fresh session at a completed-task boundary."
)
PLANNER_CHECKPOINT = (
    "Context is at least 150k tokens. Save a concise brief with acceptance "
    "criteria, checkout/commit, current decisions, unresolved findings, and "
    "verification. Finish the current bounded step, then return the brief path "
    "and remaining questions to primary for a fresh, narrowly scoped continuation."
)


def identity(event):
    """Resolve subagent transcripts without ever falling back to the main log."""
    role = event.get("agent_type")
    if "agent_id" in event and "agent_type" not in event:
        return None
    if "agent_type" in event and (
        not isinstance(role, str) or role.rsplit(":", 1)[-1] != "planner"
    ):
        return None
    session = event.get("session_id")
    if not isinstance(session, str) or not session:
        return None
    agent = event.get("agent_id")
    main = event.get("transcript_path")
    explicit = event.get("agent_transcript_path")
    if agent is not None or role is not None:
        if not isinstance(agent, str) or not re.fullmatch(r"[A-Za-z0-9_-]+", agent):
            return None
        if isinstance(explicit, str) and explicit:
            path = Path(explicit).expanduser().absolute()
        elif isinstance(main, str) and main:
            path = Path(main).expanduser().absolute()
            if "subagents" not in path.parts:
                name = agent if agent.startswith("agent-") else "agent-" + agent
                path = path.parent / path.stem / "subagents" / (name + ".jsonl")
        else:
            return None
    elif isinstance(main, str) and main:
        path = Path(main).expanduser().absolute()
    else:
        return None
    key = hashlib.sha256(json.dumps(
        [session, str(path), agent], separators=(",", ":")
    ).encode()).hexdigest()
    return key, path, role is not None


def anchor(stream, offset):
    stream.seek(max(0, offset - 128))
    return hashlib.sha256(stream.read(min(offset, 128))).hexdigest()


def usage(record):
    message = record.get("message")
    # Synthetic messages carry placeholder counters, not measured context.
    if not isinstance(message, dict) or message.get("model") == "<synthetic>":
        return None
    counters = message.get("usage")
    if not isinstance(counters, dict) or "input_tokens" not in counters:
        return None
    values = [counters.get(key, 0) for key in (
        "input_tokens", "cache_creation_input_tokens", "cache_read_input_tokens"
    )]
    if any(type(value) is not int or value < 0 for value in values):
        return None
    return sum(values)


def scan(path, state):
    """Read at most one tail window, retaining an incomplete trailing line."""
    with path.open("rb") as stream:
        info = os.fstat(stream.fileno())
        if not stat.S_ISREG(info.st_mode):
            raise ValueError("not a regular transcript")
        offset = state.get("offset", 0)
        if type(offset) is not int or offset < 0:
            offset = 0
        same = (state.get("file") == [info.st_dev, info.st_ino]
                and offset <= info.st_size
                and state.get("anchor") == anchor(stream, offset))
        if not same:
            offset = 0
            state["tokens"] = None
            state["discard"] = False
        start = max(offset, info.st_size - SCAN_LIMIT)
        if start > offset:
            state["tokens"] = None
            state["discard"] = True
        stream.seek(start)
        data = stream.read(SCAN_LIMIT)
        end = data.rfind(b"\n") + 1
        complete = data[:end].splitlines()
        if state.get("discard") and complete:
            complete = complete[1:]
            state["discard"] = False
        for line in complete:
            try:
                record = json.loads(line)
            except (ValueError, UnicodeError):
                continue
            if not isinstance(record, dict):
                continue
            if (record.get("type") == "compact_boundary"
                    or record.get("subtype") == "compact_boundary"):
                # Only a genuine measurement below 80k rearms the thresholds.
                state["tokens"] = None
            elif record.get("type") == "assistant":
                state["tokens"] = usage(record)
                if state["tokens"] is not None and state["tokens"] < 80000:
                    state["level"] = 0
        state.update(file=[info.st_dev, info.st_ino], offset=start + end)
        state["anchor"] = anchor(stream, state["offset"])


def private_open(path, flags):
    fd = os.open(str(path), flags | os.O_NOFOLLOW | os.O_NONBLOCK, 0o600)
    try:
        if not stat.S_ISREG(os.fstat(fd).st_mode):
            raise ValueError("not a regular state file")
        os.fchmod(fd, 0o600)
    except Exception:
        os.close(fd)
        raise
    return fd


def load_state(path):
    try:
        with os.fdopen(private_open(path, os.O_RDONLY), "r") as stream:
            state = json.loads(stream.read(65536))
        if (isinstance(state, dict) and state.get("version") == 1
                and type(state.get("level")) is int
                and state["level"] in (0, 1, 2)
                and type(state.get("offset")) is int
                and state["offset"] >= 0
                and (state.get("tokens") is None
                     or (type(state["tokens"]) is int and state["tokens"] >= 0))):
            return state
    except (OSError, ValueError, UnicodeError):
        pass
    return {"version": 1, "level": 0, "tokens": None}


def save_state(directory, path, state):
    fd, temporary = tempfile.mkstemp(prefix=".checkpoint-", dir=str(directory))
    try:
        with os.fdopen(fd, "w") as stream:
            json.dump(state, stream, separators=(",", ":"))
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def run(event, directory):
    if not isinstance(event, dict) or event.get("hook_event_name") not in EVENTS:
        return None
    resolved = identity(event)
    if resolved is None:
        return None
    key, transcript, planner = resolved
    # Check before creating state; missing subagent logs are normal on early events.
    if not transcript.is_file():
        return None
    directory = Path(directory).expanduser()
    directory.mkdir(mode=0o700, parents=True, exist_ok=True)
    if directory.is_symlink() or not directory.is_dir():
        return None
    directory.chmod(0o700)
    with os.fdopen(private_open(directory / (key + ".lock"), os.O_RDWR | os.O_CREAT), "w") as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            return None
        path = directory / (key + ".json")
        state = load_state(path)
        scan(transcript, state)
        tokens = state.get("tokens")
        level = state.get("level", 0)
        reminder = None
        if tokens is not None:
            if tokens >= 150000 and level < 2:
                reminder = PLANNER_CHECKPOINT if planner else CHECKPOINT
                state["level"] = 2
            elif tokens >= 100000 and level < 1:
                reminder = ADVISORY
                state["level"] = 1
        save_state(directory, path, state)
        if reminder:
            return {"hookSpecificOutput": {
                "hookEventName": event["hook_event_name"],
                "additionalContext": reminder,
            }}
    return None


def main():
    try:
        args = sys.argv[1:]
        if not args:
            directory = Path.home() / ".claude/cache/context-checkpoint"
        elif len(args) == 2 and args[0] == "--state-dir":
            directory = Path(args[1])
        else:
            return
        raw = sys.stdin.read(INPUT_LIMIT + 1)
        if len(raw) > INPUT_LIMIT:
            return
        result = run(json.loads(raw), directory)
        if result:
            print(json.dumps(result, separators=(",", ":")))
    except Exception:
        # Hooks must never interrupt the user's work or expose transcript data.
        return


if __name__ == "__main__":
    main()
