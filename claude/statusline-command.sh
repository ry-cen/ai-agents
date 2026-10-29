#!/bin/bash
# Claude Code status line: folder, git branch, model, context usage

input=$(cat)

cwd=$(echo "$input" | jq -r '.workspace.current_dir // .cwd // empty')
[ -z "$cwd" ] && cwd="$(pwd)"

# Colors (ANSI)
limegreen='\033[38;5;118m'
turquoise='\033[38;5;81m'
orange='\033[38;5;166m'
hotpink='\033[38;5;161m'
purple='\033[38;5;135m'
gray='\033[38;5;245m'
cyan='\033[38;5;51m'
yellow='\033[38;5;226m'
reset='\033[0m'

# Folder (shorten home to ~)
short_cwd="${cwd/#$HOME/~}"
folder_part="${limegreen}${short_cwd}${reset}"

# Git branch with status dots (skip optional locks to avoid blocking)
git_part=""
if git_branch=$(git -C "$cwd" --no-optional-locks symbolic-ref --short HEAD 2>/dev/null); then
    git_status=$(git -C "$cwd" --no-optional-locks status --porcelain 2>/dev/null)
    staged=""; unstaged=""; untracked=""
    echo "$git_status" | grep -q "^[MADRC]"   && staged="\033[38;5;118m\xe2\x97\x8f"
    echo "$git_status" | grep -q "^.[MADRC?]" && unstaged="\033[38;5;166m\xe2\x97\x8f"
    echo "$git_status" | grep -q "^??"        && untracked="\033[38;5;161m\xe2\x97\x8f"
    git_part=" ${gray}(${turquoise}${git_branch}${unstaged}${staged}${untracked}${gray})${reset}"
fi

# Model display name
model_part=""
model_name=$(echo "$input" | jq -r '.model.display_name // empty')
[ -n "$model_name" ] && model_part=" ${gray}[${purple}${model_name}${gray}]${reset}"

# Context usage
used_pct=$(echo "$input" | jq -r '.context_window.used_percentage // empty')
ctx_total=$(echo "$input" | jq -r '.context_window.context_window_size // empty')
total_in=$(echo "$input" | jq -r '.context_window.total_input_tokens // 0')
total_out=$(echo "$input" | jq -r '.context_window.total_output_tokens // 0')
total_in=${total_in:-0}; total_out=${total_out:-0}

if [ -z "$used_pct" ]; then
    window=${ctx_total:-200000}
    used_pct=$(awk -v tin="$total_in" -v tout="$total_out" -v win="$window" \
        'BEGIN { if (win > 0) printf "%.2f", (tin + tout) * 100 / win; else print "" }')
fi

ctx_part=""
if [ -n "$used_pct" ] && [ "$used_pct" != "0.00" ]; then
    pct_color=$(awk -v pct="$used_pct" -v hp="$hotpink" -v yw="$yellow" -v cy="$cyan" \
        'BEGIN { if (pct+0 > 75) print hp; else if (pct+0 > 50) print yw; else print cy }')
    used_pct_fmt=$(printf "%.0f" "$used_pct")
    total_tokens=$((total_in + total_out))
    total_k=$(echo "$total_tokens" | awk '{printf "%.1fk", $1/1000}')
    # Build a 10-char progress bar: filled blocks vs empty blocks
    bar=$(awk -v pct="$used_pct" -v pc="$pct_color" -v gc="$gray" -v rs="$reset" 'BEGIN {
        filled = int(pct * 10 / 100 + 0.5)
        if (filled > 10) filled = 10
        empty = 10 - filled
        bar = pc
        for (i = 0; i < filled; i++) bar = bar "\xe2\x96\x88"
        bar = bar gc
        for (i = 0; i < empty; i++) bar = bar "\xe2\x96\x91"
        bar = bar rs
        print bar
    }')
    ctx_part=" ${gray}[${bar}${gray} ${pct_color}${used_pct_fmt}%${gray} ${cyan}${total_k}${gray}]${reset}"
fi

# Rate limit bars (5-hour session and 7-day weekly)
five_pct=$(echo "$input" | jq -r '.rate_limits.five_hour.used_percentage // empty')
week_pct=$(echo "$input" | jq -r '.rate_limits.seven_day.used_percentage // empty')

make_bar() {
    pct="$1"
    awk -v pct="$pct" -v hp="$hotpink" -v yw="$yellow" -v cy="$cyan" -v gc="$gray" -v rs="$reset" 'BEGIN {
        if (pct+0 > 75) pc = hp
        else if (pct+0 > 50) pc = yw
        else pc = cy
        filled = int(pct * 10 / 100 + 0.5)
        if (filled > 10) filled = 10
        empty = 10 - filled
        bar = pc
        for (i = 0; i < filled; i++) bar = bar "\xe2\x96\x88"
        bar = bar gc
        for (i = 0; i < empty; i++) bar = bar "\xe2\x96\x91"
        pct_fmt = sprintf("%.0f", pct)
        bar = bar rs
        printf "%s %s%s%%%s", bar, pc, pct_fmt, rs
    }'
}

rate_part=""
if [ -n "$five_pct" ] || [ -n "$week_pct" ]; then
    rate_part=" ${gray}["
    if [ -n "$five_pct" ]; then
        five_bar=$(make_bar "$five_pct")
        rate_part="${rate_part}${gray}5h:$(printf '%b' "$five_bar")"
    fi
    if [ -n "$five_pct" ] && [ -n "$week_pct" ]; then
        rate_part="${rate_part}${gray} "
    fi
    if [ -n "$week_pct" ]; then
        week_bar=$(make_bar "$week_pct")
        rate_part="${rate_part}${gray}7d:$(printf '%b' "$week_bar")"
    fi
    rate_part="${rate_part}${gray}]${reset}"
fi

bars_part="${ctx_part}${rate_part}"
[ -n "$bars_part" ] && bars_part=$'\n'"${bars_part# }"
printf '%b' "${folder_part}${git_part}${model_part}${bars_part}"
