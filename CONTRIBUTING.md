# Contributing

Issues and pull requests are welcome.

## Before you start

Read [`AGENTS.md`](AGENTS.md). It sets out the four rules headwork does not
break and why each one exists. A change that weakens one will not be merged,
however convenient - they are the difference between a skill and a prompt.

## Running the tests

```bash
python3 -m pytest skills/headwork/tests -q
```

Python 3.9 or newer, standard library plus pytest. No credentials, no network,
nothing to install.

The tests are structural: they assert `SKILL.md` states its rules, that the
Claude Code and Codex paths carry the same five parts, and that nothing writes
state. They cannot test how a model behaves after reading the file. That limit
is real and is stated in `AGENTS.md` rather than papered over.

## The most useful contribution

**A worked example of the look-first rule deleting a question.**
`skills/headwork/references/worked-examples.md` has one. The rule is the whole
skill, and the clearest way to teach it is a case where looking turned a
decision into a fact - a constraint somebody was about to hold a vote on.

Second most useful: **a harness path**. If you use headwork somewhere with its
own structured-input mechanism, the text fallback probably is not the best it
can do. Add a section to `SKILL.md` carrying the same five parts, and extend
`test_both_paths_carry_the_same_parts` to cover it.

## Style

- **British English** throughout.
- **Plain hyphens, never em or en dashes.** CI fails on them.
- **No trailing full stop** on a heading, label or button.
- Keep `SKILL.md` short. It is read by a model on every invocation, and a rule
  buried under three screens of prose is a rule that does not fire.
