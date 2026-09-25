# Worked examples

Four rounds. The last is the one that matters most, because the best outcome is
often that the question disappears.

## 1. A normal round

The user has been editing a deploy workflow and says "right, I'm stuck - what's
next here?"

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

Then one call to the question tool, with `multiSelect: false` and the header
`Deploy fix`. The argument is already in the message, so each description is one
short sentence:

| Label | Description |
|---|---|
| **Fix the variable and push (Recommended)** | One push proves the build and the purge together. |
| **Prove the purge locally first** | Tests the purge by hand before CI relies on it. |
| **Revert the purge step** | Gets deploys working today and puts the purge off. |

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
