<!--
Saved reply, evals/cases.md case 4 ("A real decision"), run on 25 Sep 2026 by
a Claude Code subagent with no question tool, reading SKILL.md at 40c1c01. The
reply is verbatim.
-->
Checked: `store.py`, the README, `tests/test_store.py`, `CHANGELOG.md`, `docs/release-2.0.md` and the git log, which has one commit (1.4.0) and no remote or issues. Returning None is the documented and tested behaviour today. The changelog says the project follows semantic versioning. `docs/release-2.0.md` lists "What `get` does with a missing key" as an open decision before 2.0, so nothing has settled it yet.

1. Returning None is the contract today. The README and the docstring both say so, and `test_get_returns_none_for_a_missing_key` checks it. Raising KeyError breaks every caller that relies on it, so under semantic versioning it can only ship in 2.0.
2. A 2.0 is already planned, and this question is on its list. So a break would have a release to go out in, but every breaking change in 2.0 is more migration work for users.
3. None has one real flaw. After `put("a", None)`, `get("a")` looks the same as a missing key. KeyError fixes that. So does letting callers pass their own default, which is how `dict.get` works.

RECOMMENDED: Keep returning None and add a `default` argument, `get(key, default=None)`. REASON: nothing breaks, so it can ship in 1.5 and come off the 2.0 list. It matches `dict.get`, which the name `get` already suggests. It also fixes None's one real flaw: a caller who needs to tell a stored None from a missing key passes their own sentinel as the default.
OVERTURNED IF: callers have had bugs where a missing key was silently passed on as None. Then the silent failure is the real problem, and KeyError in 2.0 is worth the break.
INSTEAD: Raise KeyError in 2.0 - a missing key fails at the lookup, and a stored None is no longer ambiguous. COST: it is a breaking change, so it must wait for 2.0. The API has only `get` and `put`, so there is no way to check whether a key exists first. Every caller would need a try/except, or 2.0 would need an existence check as well.
INSTEAD: Keep returning None exactly as it is - no code change, and it closes the item on the 2.0 list. COST: a stored None and a missing key still look the same, and callers get no way to tell them apart.

Go with keeping None and adding a `default` argument?
