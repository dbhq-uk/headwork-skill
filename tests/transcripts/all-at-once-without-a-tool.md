<!--
Saved reply, evals/cases.md case 5 ("Asked for everything at once"), run on
25 Sep 2026 by a Claude Code subagent with no question tool, reading SKILL.md
at 40c1c01. The reply is verbatim.
-->
Three decisions are open for 2.0: what `get` does with a missing key, whether to drop Python 3.8, and whether to rename `put` to `set`. I'll ask them one at a time. `get` comes first because it is the only one that changes what existing code does when it runs.

Checked: `docs/release-2.0.md`, `store.py`, the README, `tests/test_store.py`, `CHANGELOG.md`, `pyproject.toml` and the git log. All three decisions are listed as open, and nothing in the repo settles any of them.

1. Today `get` returns `None` for a missing key. The README says so and `test_get_returns_none_for_a_missing_key` tests it.
2. That means a missing key and a stored `None` look the same. After `put("a", None)`, both `get("a")` and `get("nope")` return `None`, and a caller cannot tell them apart.
3. The changelog says the project follows semantic versioning, so 2.0 is where a breaking change is allowed. A change that breaks nobody can ship in a 1.x release instead.

RECOMMENDED: Add a `default` argument. REASON: `get(key, default=None)` keeps today's behaviour for every existing caller. Anyone who needs to tell a stored `None` from a missing key can pass their own sentinel. Python users already know this from `dict.get`. It breaks nothing, so it does not have to wait for 2.0.
OVERTURNED IF: returning `None` quietly has already caused real bugs, such as a mistyped key that went unnoticed, and you want 2.0 to make a missing key fail loudly. Then raise `KeyError`, because 2.0 is the only chance to make that break before 3.0.
INSTEAD: Raise `KeyError` - a missing key can never pass for a stored `None`, and a mistyped key fails straight away. COST: every caller that checks `is None` breaks at run time. A search for `get(` finds every call but not which ones rely on `None`.
INSTEAD: Keep returning `None` - nothing to change or document. COST: a stored `None` still looks the same as a missing key, and callers who care have no way around it.

Go with adding a `default` argument?
