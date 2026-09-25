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
nothing writes state. `tests/roundcheck.py` checks the shape of every saved
round: the worked examples and the real replies in `tests/transcripts/`.

None of that can test how a model behaves after reading the file. That limit is
real and is stated in `AGENTS.md` rather than papered over. The prompt cases in
`evals/` are for that, run by hand.

## The most useful contribution

**A real reply, saved.** Run one of the cases in `evals/` against a real model
and save the reply in `tests/transcripts/`, as `evals/README.md` describes.
Each one holds the checker to real output rather than to fixtures written for
it. A reply that fails the checker is worth an issue instead.

Also welcome: a worked example where looking first turned a decision into a
fact, which is the look-first rule deleting a question rather than dressing one.

Second most useful: **a question tool's limits**. If you use headwork with a
question tool that `SKILL.md` does not name, or one whose limits differ from the
ones in "With a question tool", add them there and to `TOOLS` in
`tests/roundcheck.py`, and extend
`test_the_tool_path_sets_single_select_and_the_limits` to cover them.

## Style

- **British English** throughout.
- **Plain hyphens, never em or en dashes.** CI fails on them.
- **No trailing full stop** on a heading, label or button.
- Keep `SKILL.md` short. It is read by a model on every invocation, and a rule
  buried under three screens of prose is a rule that does not fire.
