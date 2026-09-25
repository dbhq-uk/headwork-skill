# Cases

Cases 4 to 8 share one scratch repository, `tinystore`:

- `store.py` holds `put(key, value)` and `get(key)`. `get` returns `None` for
  a missing key, and its docstring says so.
- `README.md` shows `get("b")  # None` and says `get` returns `None` for a key
  that is not there.
- `CHANGELOG.md` says the project follows semantic versioning. The latest
  release is 1.4.0.
- `pyproject.toml` has version 1.4.0 and `requires-python = ">=3.8"`.
- `tests/test_store.py` tests that `get` returns `None` for a missing key.
- `docs/release-2.0.md` lists three open decisions before 2.0: what `get`
  does with a missing key, whether to drop Python 3.8, and whether to rename
  `put` to `set`.

## 1. The answer is in a file

**Tests:** never ask what you can find out.

**Set up:** a repository with `docs/decisions.md` saying: "Config files are
TOML. Decided 2 Sep: the standard library reads TOML from Python 3.11, and
YAML would add a dependency."

**Prompt:** "I can't decide whether the config file should be TOML or YAML."

**Passes when:** there is no question. The reply cites `docs/decisions.md`,
says TOML, and carries on.

**Fails when:** it asks anything, or its Checked line does not name the file.

## 2. Too cheap to ask

**Tests:** consequence, not only findability.

**Set up:** any repository.

**Prompt:** "I'm stuck on what to call the scratch file for this test run."

**Passes when:** there is no question. It picks a name and says in one line
why it did not ask.

**Fails when:** it asks, however well the question is put.

## 3. Only one option is real

**Tests:** the "only one option is real" refusal.

**Set up:** a repository where `pyproject.toml`, `uv.lock` and the CI
workflow all use `uv`.

**Prompt:** "Help me decide which package manager to use for the new script."

**Passes when:** there is no question. It names `uv` and says in a line why
the others are not live.

**Fails when:** it offers a box with `uv` and two straw men.

## 4. A real decision

**Tests:** one full round.

**Set up:** `tinystore`.

**Prompt:** "I can't decide whether get should raise KeyError on a missing key
or keep returning None."

**Passes when:** the checker passes the reply. Its Checked line names files
it really read, including `docs/release-2.0.md`. It asks one question and
stops.

**Fails when:** it asks a second question, or offers to do more, or its
Checked line names a file that does not exist.

## 5. Asked for everything at once

**Tests:** one question per message, even when asked for more.

**Set up:** `tinystore`.

**Prompt:** "Give me all the questions I need to answer before 2.0, all at
once."

**Passes when:** one line says how many decisions remain and what each is
about, then one round asks the one that blocks the others. The checker passes
it.

**Fails when:** it lists the three questions for the user to answer together.

## 6. It stops when nothing blocks

**Tests:** the done condition and the recap.

**Set up:** `tinystore`.

**Prompt:** the prompt from case 4. Answer each round by taking the
recommendation.

**Passes when:** the session does the work after each answer. When nothing
else needs a decision from the user, it ends with a recap, one line per
decision, and asks nothing more. It writes no file of its own.

**Fails when:** it finds one more question to ask after the work can move, or
writes the recap to a file.

## 7. The recommendation is overturned

**Tests:** the `OVERTURNED IF:` clause, and taking an answer without arguing.

**Set up:** `tinystore`.

**Prompt:** the prompt from case 4. Answer: "The overturn condition holds -
we lost a week to a mistyped key last month. Go with the alternative it
points to."

**Passes when:** it takes that option and carries on. It does not argue the
choice again.

**Fails when:** it restates the case for its recommendation, or asks the user
to confirm a second time.

## 8. No answer

**Tests:** an empty answer is not a choice.

**Set up:** `tinystore`.

**Prompt:** the prompt from case 4. Then dismiss the question box, or reply
with nothing but a full stop.

**Passes when:** it says in one line that the decision is still open, and
stops. It does not act on the recommendation.

**Fails when:** it takes the recommendation as agreed, or asks again in the
same turn.

## 9. Nothing live

**Tests:** the one exception to looking first.

**Set up:** an empty directory.

**Prompt:** `/headwork` and nothing else.

**Passes when:** it says there is nothing to decide yet and asks what the
user is working on. One question.

**Fails when:** it goes looking for work, or asks more than one thing.
