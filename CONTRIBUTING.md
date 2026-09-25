# Contributing

Issues and pull requests are welcome.

## Before you start

Read [`AGENTS.md`](AGENTS.md). It sets out the rules headwork does not
break and why each one exists. A change that weakens one will not be merged,
however convenient - they are the difference between a skill and a prompt.

## Running the tests

```bash
python3 -m pytest tests -q
```

Python 3.9 or newer, standard library plus pytest. No credentials, no network,
nothing to install.

The tests are structural: they assert `SKILL.md` states its rules, that asking
with a question tool and asking without one carry the same six parts, and that
nothing writes state. They cannot test how a model behaves after reading the file. That limit
is real and is stated in `AGENTS.md` rather than papered over.

## The most useful contribution

**A worked example of a recommendation being overturned by its own clause.**
`skills/headwork/references/worked-examples.md` has four rounds but none yet
where the user reads the `OVERTURNED IF:` condition, knows it holds, and picks
something else. That is the clause working, and it is the hardest part of the
skill to teach from an example where the recommendation simply wins.

Also welcome: a case where looking first turned a decision into a fact, which is
the look-first rule deleting a question rather than dressing one.

Second most useful: **a question tool's limits**. If you use headwork with a
question tool that `SKILL.md` does not name, or one whose limits differ from the
ones in "With a question tool", add them there and extend
`test_the_tool_path_sets_single_select_and_the_limits` to cover them.

## Style

- **British English** throughout.
- **Plain hyphens, never em or en dashes.** CI fails on them.
- **No trailing full stop** on a heading, label or button.
- Keep `SKILL.md` short. It is read by a model on every invocation, and a rule
  buried under three screens of prose is a rule that does not fire.
