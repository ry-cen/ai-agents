# Principles

Condensed from pstack (MIT) in our own words. Upstream skill names are in parentheses.

- **Subtract before you add; stay lazy.** Remove dead code first, then build on the simpler base. Prefer the smallest diff that solves the problem and one source of truth for each decision. (principle-laziness-protocol, principle-subtract-before-you-add)
- **Think foundationally.** Get core data shapes right before logic; ask what concurrent actors share. (principle-foundational-thinking)
- **Model the domain.** Put domain rules in a structure so invalid states cannot exist. (principle-model-the-domain)
- **Boundary discipline.** Validate where data enters; trust types inside; keep logic pure and the shell thin. (principle-boundary-discipline)
- **Fix root causes.** Find the first wrong decision; a guard is a fix only when the guarded state is legitimate. (principle-fix-root-causes)
- **Attack the premise.** When fixes sharing an assumption keep failing, write the assumption down and test it. (principle-attack-the-premise)
- **Prove it works.** Observe the real behavior; proxies do not count. (principle-prove-it-works)
- **Test behavior, not implementation.** Assert what users of the code can observe. (principle-test-behavior-not-implementation)
- **Sequence verifiable units.** Small steps, each checked before the next. (principle-sequence-verifiable-units)
- **Minimize reader load.** Collapse forwarding layers and shrink mutable state scope. (principle-minimize-reader-load)
