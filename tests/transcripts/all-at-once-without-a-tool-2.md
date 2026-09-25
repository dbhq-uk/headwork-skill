<!--
Saved reply, evals/cases.md case 5 ("Asked for everything at once"), run on
25 Sep 2026 by a Claude Code subagent with no question tool, reading SKILL.md
after the cut to under 1,000 words (#11). The reply is verbatim.
-->
Three decisions stand before 2.0, all listed in docs/release-2.0.md: what `get` does with a missing key, whether to drop Python 3.8, and whether to rename `put` to `set`. I'll take them one at a time, starting with `get`, because it is the only one that changes what running code returns.

Checked: docs/release-2.0.md lists the three decisions. store.py, README.md and tests/test_store.py show what `get` does today. CHANGELOG.md says the project follows semver. git log has one commit (1.4.0), and nothing in the repo already decides any of the three.

1. Today `get` returns None for a missing key. The README, the docstring and `test_get_returns_none_for_a_missing_key` all promise that, so every caller can see any change here.
2. The catch: store None under a key and `get` returns None for it too. A caller cannot tell "stored None" from "not there".
3. Under semver, a breaking change here can only go in 2.0. After that, the next chance is 3.0.

RECOMMENDED: Add a default argument, `get(key, default=None)`, as `dict.get` does. REASON: every caller that checks for None keeps working, and a caller that needs to tell a stored None from a missing key passes its own default. It breaks nothing, so it does not have to wait for 2.0.
OVERTURNED IF: you want a missing key to be an error that callers cannot ignore. Then raise KeyError, and 2.0 is the release for it.
INSTEAD: Raise KeyError - a missing key fails loudly, like `d[key]` on a dict. COST: it breaks every caller that tests `is None`, and the README, the docstring and the test all have to change.
INSTEAD: Keep returning None - no work at all. COST: a stored None and a missing key still look the same.

Go with a default argument on `get`?
