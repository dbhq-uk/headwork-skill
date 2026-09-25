# Working on headwork

Read this before changing `skills/headwork/SKILL.md`. That file is the product -
there is no program here, so a careless edit to the prose is a careless edit to
the behaviour.

## The thing that makes this skill worth having

Not the question box, not the look-first rule, and **not the recommendation on
its own**. Each of those has been the answer here, and each is now common.

The skill to compare against is `grill-me` in
[`mattpocock/skills`](https://github.com/mattpocock/skills). It hands off to
the same repo's
[`grilling`](https://github.com/mattpocock/skills/blob/main/skills/productivity/grilling/SKILL.md)
skill, which maps a plan as a tree of decisions and works it in rounds. Each
round asks every question whose prerequisites are settled, all at once, each
with a recommended answer. It sends a subagent to find facts rather than asking
the user for them. It is done when no questions are left, and it does not act
until the user confirms they share an understanding.

It is not alone in recommending. `superpowers:brainstorming` says to lead with
the recommended option, and the question tools in Claude Code and Codex both ask
for the recommended option first, marked "(Recommended)". Looking before asking
and naming a recommendation are table stakes.

(An earlier version of this file compared headwork with
`RobMitt/grill-me-skill`. That is a short copy, not the original, and the
comparison built on it was wrong.)

What headwork has that the others do not, and what every change has to leave
standing:

1. **The recommendation says what would overturn it.** An `OVERTURNED IF:`
   clause, naming the condition under which another option is right. grilling's
   recommended answer carries no stated escape. Rule 3a.
2. **Every alternative names its cost.** A `COST:` on each option that is not
   the recommendation. Rule 3.
3. **One question per message.** grilling asks a whole round at once. Rule 2.
4. **It refuses to spend a question on a cheap, reversible decision.** grilling
   aims to leave nothing assumed; headwork decides small things and says so.
   Rule 5.
5. **It works on the one decision blocking the work right now.** grilling maps
   the whole plan. headwork takes what is stopping the session and leaves the
   rest until it blocks.

The best outcome headwork can produce is still **no question at all** - it
looked, the answer was in the repo, and it said so. A change that makes a
well-formatted box easier to produce, at the cost of making that outcome rarer,
is the wrong change however good the box looks.

## The rules

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

**Rounds are a different thing and are not capped** (Dan, 18 Sep 2026). headwork
keeps going for as many rounds as it takes to unblock the user. Do not reinstate
a stop-after-one: the limit is questions per message, never how many decisions a
session may settle.

Uncapped is not endless. A session is done when the work can take its next
action without another decision from the user, because an agent can always find
one more question. It ends with a recap, one line per decision, in the
conversation. Not in a file: the no-state rule below still holds.

### 3. Every option carries a justification, and every alternative its cost

An option with a bare label is not an option, it is a word to pick between. An
option with no stated downside has not been thought about. The recommendation
goes first, labelled, with its reason - and it names what it costs too.

### 3a. The recommendation says what would overturn it

An `OVERTURNED IF:` clause on every recommendation, naming the condition under
which a different option is right.

This is not politeness. A recommendation with no stated escape is an anchor, and
the HCI literature treats anchoring as a facet of automation bias - users fixate
on machine-generated advice even when they hold the context to judge it, and
warnings are weak debiasing. What does work is anchoring the judgement on
relevant criteria, which is exactly what this clause supplies: the user overrules
by checking a condition they know about, rather than by disagreeing with a
machine.

It also bites hardest where the decision feels unimportant, which is why rule 5
exists.

### 4. Both ways of asking carry the same parts

The way of asking is chosen by capability, not by harness name. With a question
tool in the tool list, the agent sends the written-out block and then calls the
tool. Without one, it sends the same block and asks one plain-text question that
confirms the recommendation. Both carry all six parts: the checked line, the
bite-sized explainer, the options, a justification per option, a named
recommendation, and what would overturn it.

Do not go back to choosing by name. Codex, OpenCode and Gemini CLI all have a
question tool now, and Codex's own prompt forbids the numbered text menu this
skill used to send it. A Claude Code subagent, meanwhile, has no question tool
at all.

The no-tool path is the one more at risk of rotting - nobody developing this
runs it that way daily. The test asserting both paths send the block is the only
thing holding it, so do not delete it when it becomes inconvenient.

### 5. Findability is not the only test - consequence is the other one

"I could not look this up" does not make a decision worth asking about. A
question spends the user's attention, so cheap and easily reversed gets decided
and stated, not asked.

The evidence is direct. "Ask or Assume? Uncertainty-Aware Clarification-Seeking
in Coding Agents" ([arXiv 2603.26233](https://arxiv.org/abs/2603.26233)) reports
a 69.40% resolve rate for an uncertainty-aware scaffold against a standard
single-agent setup, and the behaviour behind the number is conserving queries on
simple tasks while seeking information on complex ones. Related work scores
agents on *redundant questions asked* - a question is a cost, not free
insurance.

Ask when the decision is expensive, hard to reverse, or genuinely the user's to
make. This is the fourth refusal case in `SKILL.md`.

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
they assert that `SKILL.md` states the rules, that both ways of asking carry the
same parts, and that nothing writes state. They cannot test the behaviour of a
model reading the file, and they do not pretend to.

That is a real limit, stated rather than hidden. It means a change that keeps
every rule visible in the file but buries them under three screens of new prose
would pass. Keep the file short.
