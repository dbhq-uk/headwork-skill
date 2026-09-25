# Worked examples

Seven examples. The fourth is the one that matters most, because the best
outcome is often that the question disappears. The fifth shows a session of
more than one round, and how it ends. The sixth is a round with no question
tool, and the seventh is a recommendation overturned by its own clause.

## 1. A normal round

The user has been editing a deploy workflow and says "right, I'm stuck on which
way to take this".

**Look:** `git log -10`, the workflow file, and `gh run list` for whether the
last run passed.

**The message:**

> Checked: `deploy.yml`, the last ten commits and the three most recent runs -
> the cache purge step was added on 16 Sep and has never actually run, because
> every push since then failed earlier at the build step.
>
> 1. The build has been broken for two days, so nothing has deployed and the
>    purge step is untested.
> 2. The failure is a missing environment variable, not a code problem - the
>    build worked locally on the same commit.
> 3. You can fix the variable and find out whether the purge works, or fix the
>    variable and prove the purge separately first.
>
> RECOMMENDED: Fix the variable and push. REASON: the purge step is four lines
> calling one documented endpoint, and the only thing standing between you and
> knowing is a green run. Proving it separately costs an hour to learn what one
> push tells you in ninety seconds.
> OVERTURNED IF: a failed purge would serve stale files to real traffic rather
> than to you - then it is worth proving first, because the cost of being wrong
> stops being ninety seconds.
> INSTEAD: Prove the purge locally first - runs the purge by hand against the
> zone before trusting it in CI. COST: an hour, and it does not exercise the CI
> credentials, which are a different token from the one in your shell - so the
> thing most likely to break is the thing you would not have tested.
> INSTEAD: Revert the purge step - gets deploys working again today. COST: stale
> files at the edge are the exact bug the step was added for on 16 Sep, so this
> reinstates a known problem to avoid an unknown one.

Then one call to `AskUserQuestion`. The argument is already in the message, so
each description is one short sentence:

```json
{
  "questions": [
    {
      "question": "How do you want to fix the deploy?",
      "header": "Deploy fix",
      "multiSelect": false,
      "options": [
        {"label": "Fix the variable and push (Recommended)", "description": "One push proves the build and the purge together."},
        {"label": "Prove the purge locally first", "description": "Tests the purge by hand before CI relies on it."},
        {"label": "Revert the purge step", "description": "Gets deploys working today and puts the purge off."}
      ]
    }
  ]
}
```

With no question tool, the same message ends with one line instead of the call:

> Go with fixing the variable and pushing?

Then stop and wait. If the answer turns out to reveal a second decision, that is
a new round in its own message - not an addition to this one.

The `OVERTURNED IF:` clause is the part most likely to be dropped, and it is the
part that makes the recommendation arguable rather than authoritative. A reader
who knows the traffic situation can now overrule the recommendation by checking
a condition instead of by disagreeing with a machine.

## 2. A refusal, because only one option is real

The user asks which package manager to use for a new script in a repo that has
used `uv` everywhere for a year.

Do not build a box. Say:

> Checked the six scripts in `scripts/` and the CI workflow - all six use `uv`,
> and `validate.yml` installs it. There is one real option here, so I have taken
> it rather than ask: `uv`. A second package manager in this repo would mean two
> lockfiles and a CI step that installs both.

Then get on with it.

## 3. A refusal, because the decision is too cheap to spend a turn on

The user is mid-task and the agent needs to name a temporary file.

There is no way to look this up - nothing in the repo settles it - so the
look-first rule would let the question through. Refuse anyway:

> Called it `/tmp/headwork-check.json`. It is a temp file in a scratch directory
> and renaming it later costs nothing, so it is not worth a question.

The test is not only "can I find this out". It is also "is this worth a turn".
A question costs the user their attention, and an unfindable trivial decision
spends that for nothing. Cheap and easily reversed gets decided and stated.

Ask when the decision is expensive, hard to reverse, or genuinely theirs to
make - a hostname that will end up in other people's links, a schema everything
downstream reads, anything that spends money.

## 4. The best outcome - looking removed the question

The user says "I can't decide whether to make the banner generator emit PNG or
SVG".

**Look:** the org profile README, and how the tiles are served.

Do not ask. The answer is in the repo:

> Checked `org-profile/README.md` and how the tiles load. This is already
> decided by a constraint rather than a preference: `raw.githubusercontent.com`
> serves SVG as `text/plain`, so an SVG tile renders as source text in the
> README. It has to be PNG. No decision needed.

A question box here would have been the skill working exactly as designed and
still being useless. The look-first rule exists to catch this case, and catching
it is worth more than any well-formatted question.

## 5. Two rounds, then a recap

The user maintains a command-line tool and wants to rename its `--out` flag to
`--output`. They say "I can't decide how to do this rename".

**Look:** the argument parser, the README, `CHANGELOG.md` and the release tags.

**Round one:**

> Checked: `cli.py`, the README, `CHANGELOG.md` and the release tags - `--out`
> has been in every release since 1.0, the README uses it in four examples, and
> the changelog says the project follows semantic versioning.
>
> 1. Removing a flag breaks every script that passes it, so under semantic
>    versioning an outright rename needs a 3.0.
> 2. Keeping `--out` as an alias costs a few lines in the parser and no new
>    major version.
> 3. The alias can print a warning, so users learn the new name before the old
>    one goes.
>
> RECOMMENDED: Keep a warning alias. REASON: it ships in a minor release,
> breaks nobody, and the warning teaches the new name where the changelog
> cannot.
> OVERTURNED IF: a 3.0 is already planned with other breaking changes - then
> rename outright and let it ride along with them.
> INSTEAD: Rename outright - one name everywhere and a cleaner parser. COST:
> every script using `--out` breaks, and it forces a major release for one flag.
> INSTEAD: Keep a silent alias - nothing breaks and nothing nags. COST: nobody
> learns the new name, so the alias can never be removed.

Then one call to `AskUserQuestion`:

```json
{
  "questions": [
    {
      "question": "How should `--out` become `--output`?",
      "header": "Flag rename",
      "multiSelect": false,
      "options": [
        {"label": "Keep a warning alias (Recommended)", "description": "Ships in a minor release and breaks nobody."},
        {"label": "Rename outright", "description": "One name everywhere, in a major release."},
        {"label": "Keep a silent alias", "description": "Nothing breaks and nothing nags."}
      ]
    }
  ]
}
```

The user picks the warning alias. The session adds `--output`, keeps `--out`
as an alias that warns, and updates the tests and the README. Writing the
warning text turns up one more decision: it has to say when the alias goes.

**Round two:**

> One decision left, then this is done.
>
> Checked: `CHANGELOG.md` and the open milestones - there is no 3.0 milestone
> and nothing else is deprecated, so no removal date is already set.
>
> 1. A warning with no end date teaches users to ignore it.
> 2. Tying the removal to a version is predictable. Tying it to a date is
>    easier to state, but releases here are irregular.
>
> RECOMMENDED: Remove it in 3.0. REASON: semantic versioning already tells users
> that a major release breaks things, so the warning can name a version they
> will see coming.
> OVERTURNED IF: 3.0 is likely to be more than a year away - then a date keeps
> the alias from living for ever.
> INSTEAD: Remove it after six months - a fixed end the warning can print.
> COST: the removal would land in a minor release, which is the break the alias
> exists to avoid.

Then one call to `AskUserQuestion`:

```json
{
  "questions": [
    {
      "question": "When should the `--out` alias go?",
      "header": "Alias end",
      "multiSelect": false,
      "options": [
        {"label": "Remove it in 3.0 (Recommended)", "description": "The warning names the version it goes in."},
        {"label": "Remove it after six months", "description": "A fixed end date, whatever the version."}
      ]
    }
  ]
}
```

The user picks 3.0. The session writes the warning text and the changelog
entry. Nothing else needs a decision from the user, so the session is done, and
it ends with the recap:

> Decided:
> - `--out` stays as an alias that warns, so the rename ships in a minor
>   release and breaks nobody.
> - The alias goes in 3.0, and the warning says so.

The recap is part of the conversation. It is not written to a file, and the
reasoning it summarises belongs in the commit message.

## 6. A round with no question tool

The user is working through a subagent, which has no question tool, and says
"I'm stuck between splitting out the slow tests and running them in parallel".

**Look:** the CI workflow, the pytest configuration, and the durations in the
last run's log.

**The message**, which ends with its only question:

> Checked: `ci.yml`, `pyproject.toml`, `conftest.py` and the last run's log -
> the suite takes nine minutes, 40 of its 600 tests take seven of them, and
> every test builds its own temporary directory, so no two share a file.
>
> 1. Running in parallel spreads all 600 tests over the runner's four cores.
>    Nothing is skipped.
> 2. Splitting moves the 40 slow tests to a nightly job. Every push is faster,
>    but those 40 stop checking pull requests.
> 3. Tests that share a file or a database break when they run in parallel.
>    These do not.
>
> RECOMMENDED: Run the tests in parallel. REASON: every test still runs on
> every pull request, and four cores should more than halve the nine minutes.
> OVERTURNED IF: the slow tests need something only one test can use at a
> time, such as a shared staging service - then split them out.
> INSTEAD: Split out the slow tests - the fastest push of the three. COST: a
> bug that only those 40 catch reaches `main` and waits for the nightly run.
> INSTEAD: Pay for a bigger runner - no change to the tests. COST: it costs
> money every month, and the suite still runs one test at a time.
>
> Go with running the tests in parallel?

The message ends at the question. It does not number the options and ask for
a pick, because that is a form. "Yes", "split them" or an answer that is none
of the three all work.

## 7. The recommendation overturned by its own clause

The user is in Codex, in Plan mode, where `request_user_input` is on. They are
starting a small internal tool and say "help me decide which database this
should use".

**Look:** the repository, its README and the open issues.

**The message:**

> Checked: the repository, its README and the three open issues - the app is
> one web process with a few hundred rows, nothing else writes to it yet, and
> no issue mentions another service.
>
> 1. SQLite is a file next to the app. There is no server to run or back up.
> 2. SQLite lets one process write at a time, and the others wait for the lock.
> 3. Moving from SQLite to Postgres later means migrating the data, which gets
>    harder as it grows.
>
> RECOMMENDED: Use SQLite. REASON: one process writes a few hundred rows, and a
> file needs nothing else to run.
> OVERTURNED IF: another process will write while the app runs - then use
> Postgres, because two writers queue for SQLite's one lock.
> INSTEAD: Use Postgres - any number of writers. COST: a server to run, back up
> and upgrade, for a few hundred rows.
> INSTEAD: Use JSON files - nothing to install. COST: no queries and no
> transactions, so two saves at once can lose one of them.

Then one call to `request_user_input`. Codex allows three options, so the block
has three as well:

```json
{
  "questions": [
    {
      "id": "database",
      "header": "Database",
      "question": "Which database should the tool use?",
      "options": [
        {"label": "Use SQLite (Recommended)", "description": "One file and no server, for one writer."},
        {"label": "Use Postgres", "description": "Any number of writers, and a server to run."},
        {"label": "Use JSON files", "description": "Nothing to install, and no transactions."}
      ]
    }
  ]
}
```

The user picks **Use Postgres**, and says why: a nightly importer, not written
yet, will write to the database while the app is up.

That is the clause working. No amount of looking would have found an importer
that does not exist yet. The user did not have to argue with the
recommendation. They checked its condition against something only they knew,
and it held.

So the agent takes the answer, and does not argue it again:

> Postgres, then, since the importer will write while the app is up. Setting it
> up now.

Then it does the work.

## The anti-pattern

What headwork exists to stop:

> I can help with that. A few questions first:
>
> 1. Do you want to prioritise speed or correctness here?
> 2. Should this live in `scripts/` or `tools/`?
> 3. Do you want tests for it, and if so what kind?
> 4. Is there a deadline I should know about?
>
> Let me know and I'll get started. Also, do you want me to check the CI config
> while I'm in there?

Five questions, no explanation of why any of them matters, no options, no
recommendation, and two of them answerable by reading the repo. The reply has to
be composed rather than chosen, so it will be short and partial, and the work
will start on a guess.
