# Working on headwork

Read this before changing `skills/headwork/SKILL.md`. That file is the product -
there is no program here, so a careless edit to the prose is a careless edit to
the behaviour.

## The thing that makes this skill worth having

Not the question box. Any agent can call `AskUserQuestion`, and one that does it
badly is what this skill exists to replace.

What headwork has is the **look-first rule**: it may not ask what it could have
found out, and it has to say what it checked before it asks. That rule is what
separates a skill from a prompt, because it changes which questions get asked
rather than how they are dressed.

The best outcome headwork can produce is **no question at all** - it looked, the
answer was in the repo, and it said so. A change that makes a well-formatted box
easier to produce, at the cost of making that outcome rarer, is the wrong change
however good the box looks.

## The four rules

Each has tests in `skills/headwork/tests/`. Do not weaken one to make something
else easier.

### 1. Never ask what you can find out

`SKILL.md` requires a look step and a stated "what I checked" line before every
question. The line is the enforcement: it cannot be written honestly without
having looked, and a reader can catch it failing.

Do not soften this to "where practical" or "if time allows". The failure it
prevents - an agent asking a question a file already answers - makes the user do
both the looking and the deciding, which is worse than no skill.

### 2. One question per message, then stop

No second question in the same message. No closing "and also". No "let me know
if you would like me to".

This is the rule most likely to erode, because a trailing open question always
feels helpful in the moment. It is not: a message that ends with a box **and** a
loose question has asked two things, and the second gets ignored or answered
badly. The message ends at the question.

### 3. Every option carries a justification, and every alternative its cost

An option with a bare label is not an option, it is a word to pick between. An
option with no stated downside has not been thought about. The recommendation
goes first, labelled, with its reason - and it names what it costs too.

### 4. The two harness paths carry the same parts

Claude Code gets a question box; Codex and anything else gets the specified text
block. Both carry all five parts: the checked line, the bite-sized explainer,
the options, a justification per option, and a named recommendation.

The Codex path exists because it was asked for over a recommendation to ship
Claude Code only. That makes it more at risk of rotting, not less - nobody
developing this runs it in Codex daily. The test asserting both sections carry
all five parts is the only thing holding it, so do not delete it when it
becomes inconvenient.

## What headwork must never grow

- **A scanner.** No backlog sweep, no stalled-item hunt. `deskwork` tracks and
  orders; `dovetail` finds what a repo disagrees with itself about. A third
  implementation would be the worst of the three.
- **Write access.** It decides; the session acts. The moment headwork edits a
  file, "it only asks questions" stops being true and every safety argument for
  letting it run unprompted goes with it.
- **State.** No `~/.dbhq/headwork/`, no `.headwork/`, no run log, no settings.
  The reasoning belongs in the commit message, the pull request body, or the
  register the repo already keeps. A second register is how the wrong one gets
  read - the same failure as two generators emitting skill marks.

A test greps for the state paths, because the no-state decision is the one most
likely to erode: a run log always looks harmless in the pull request that adds
it.

## Running the tests

```bash
python3 -m pytest skills/headwork/tests -q
```

Python 3.9 or newer, standard library plus pytest. The tests are **structural** -
they assert that `SKILL.md` states the rules, that both harness paths carry the
same parts, and that nothing writes state. They cannot test the behaviour of a
model reading the file, and they do not pretend to.

That is a real limit, stated rather than hidden. It means a change that keeps
every rule visible in the file but buries them under three screens of new prose
would pass. Keep the file short.
