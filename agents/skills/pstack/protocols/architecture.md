# Architecture

Adapted from pstack skills/architect, skills/principle-model-the-domain, skills/principle-foundational-thinking, skills/principle-boundary-discipline (MIT).

Use before code when the change locks in a shape: new types, signatures, module boundaries, or shared state. Design only; no implementation.

1. Trace every system the change touches: callers, data owners, tests, and external boundaries.
2. Sketch two different shapes (types, signatures, module structure). Do not sketch one and defend it.
3. Pick the shape where each piece of state has a single owner, each task has one way to do it, and callers need to know the least.
4. Get the data model right first: encode the domain in a structure (union, state machine, map) instead of scattered conditionals, so invalid states cannot be represented.
5. Validate and narrow types where data crosses a boundary (CLI, config, network, files). Inside, trust the types. Keep business logic in pure functions behind a thin shell.
6. If workarounds keep piling up, redesign instead of patching.

Done when the chosen shape, the rejected shape and why, the interfaces, and the tests that pin the behavior are written down. Unresolved compatibility, security, or concurrency questions go to the Opus planner, not the worker.
