<!--
Saved reply, evals/cases.md case 4 ("A real decision"), run on 25 Sep 2026 by
a Claude Code subagent with no question tool, reading SKILL.md after the cut to
under 1,000 words (#11). The reply is verbatim.
-->
Checked: store.py, README.md, tests/test_store.py, CHANGELOG.md, docs/release-2.0.md and git log. `get` returns `None` today, the README says so, a test pins it, and docs/release-2.0.md lists it as an open decision for 2.0. Nothing in the repo settles it.

1. Today `get` works like Python's `dict.get`: a missing key gives `None`. Python users expect that from a method called `get`. `KeyError` is what `d[key]` raises.
2. Raising `KeyError` would break existing callers. The CHANGELOG says the project follows semantic versioning, so the change could only go into 2.0. After it, every caller that checks `get(k) is None` gets an exception instead.
3. `None` has one real weakness. After `put("x", None)`, `get("x")` and `get("missing")` return the same value.

RECOMMENDED: keep returning `None`. REASON: it is what `get` means in Python, the README and the test already promise it, and no caller breaks.
OVERTURNED IF: callers store `None` as a real value and need to tell it apart from a missing key.
INSTEAD: raise `KeyError` in 2.0 - a missing key can never be mistaken for a stored `None`, and semver allows a breaking change in 2.0. COST: every caller that relies on `None` breaks, and the README and the test must change.
INSTEAD: keep `None` and add `get(key, default=None)` - a caller who needs the difference passes their own sentinel, and it can ship in a 1.x release without breaking anyone. COST: `get` gets a second way to be called, and callers who leave out the default still cannot tell the two cases apart.

Go with keeping `None`?
