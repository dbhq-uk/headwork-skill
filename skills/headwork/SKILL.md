---
name: headwork
description: >-
  Think a decision through, one question at a time, with a recommendation you
  can argue with. When the user is stuck or deciding what comes next, headwork
  explains the decision in plain English, then asks a single question whose
  options each carry their justification, names one of them as the
  recommendation, and says what would overturn it - and it never asks what it
  could have looked up. Use when the user says "headwork", "I'm stuck", "what's
  next", "how do I move this forward", "unblock me", "unblock this", "which
  way", "help me decide", "I can't decide", "what should I do here", or "talk
  me through the options".
license: MIT
---

# headwork

The mental work of thinking something through, done one question at a time.

headwork does not find the work and it does not do the work. It takes the
decision blocking the session right now, explains it, and puts it to the user as
one question they can answer by **choosing** rather than by composing.

## What makes this more than a well-formatted question

An even-handed list of options is a decision handed back. **headwork always
names one option as the recommendation, gives the reason, and says what would
overturn it.** That last clause is what keeps a recommendation from becoming an
anchor: it hands the user the criterion, not only the verdict, so disagreeing
with it is a matter of checking a condition rather than overruling a machine.

Looking before you ask and naming a recommendation are table stakes - other
skills do both. The overturn clause, a cost on every alternative and one
question per message are what headwork adds.

## The rule this skill cannot lose

**Never ask what you can find out.**

Before every question, look. The session history first, then whatever the
decision touches: `git log`, the file itself, open issues, the area `index.md`
or register, the tests. Then say in one line what you checked and what it
settled.

A question a file could have answered is a bug, not a style lapse. It is also
the failure that makes an agent worse than no agent, because the user now has to
do the looking **and** the deciding.

The stated "what I checked" line is the enforcement. You cannot write it
honestly without having looked, and the user can see it failing.

## A round, exactly

1. **Look.** Session context first. Then the repository, for anything that
   already bears on the decision.
2. **Report what you checked** in one line, naming the sources, including
   anything they already settle.
3. **Explain in bite-sized chunks.** Two to four short numbered points in plain
   English. The user must understand the decision before being asked to make it.
   Not background - just enough that the options mean something.
4. **Ask one question**, in the format below for the tools you have.
5. **Stop and wait.** No second question in the same message. No closing "and
   also". No "let me know if you'd like me to...".
6. **Hand the answer back to the session**, which does the work. `headwork`
   itself edits nothing.

Then **go again, for as many rounds as it takes to unblock the user.** There is
no cap and no stopping after one: if settling the first decision reveals a
second, raise it - alone, in its own message, the same way. Say how many remain
in one line first, so the user knows the shape of what is left.

Step 5 is where this breaks in practice. A message that ends with a question box
**and** a trailing open question has asked two things, and the second one will be
ignored or answered badly. Rounds are unlimited; questions per message are not.

## The six parts

Every question carries all six, in this order, however it is asked:

1. **What you checked** - the sources, and anything they already settle.
2. **A bite-sized explainer** - two to four short numbered points.
3. **Two to four options** - fewer is not a decision, more is a menu.
4. **A justification per option** - and a stated cost on every option that is
   not the recommendation.
5. **A named recommendation**, placed first.
6. **What would overturn the recommendation** - the condition that would make a
   different option right.

Written out, they are this block:

```
Checked: <sources, and what they already settle>

1. <explainer point>
2. <explainer point>

RECOMMENDED: <option>. REASON: <justification>.
OVERTURNED IF: <the condition that makes another option right>.
INSTEAD: <option> - <justification>. COST: <what it gives up>.
```

One to three `INSTEAD:` lines, so two to four options in all. An option with
no stated downside has not been thought about.

## Choosing how to ask

Choose by what your tools can do, not by which harness you are in. If a
question tool is in your tool list, use it. If not, ask in plain text.

Claude Code has `AskUserQuestion`, Codex has `request_user_input`, OpenCode has
`question` and Gemini CLI has `ask_user`. But a subagent, a background agent or
`codex exec` often has none, even inside a harness that does. Codex offers its
tool in Plan mode, and in Default mode only behind a feature flag.

## With a question tool

Send the block as the message, then call the tool. The block carries the
argument because the tool's fields are too short to. One question per call,
never more, even when the tool accepts several.

- **`multiSelect: false`.** One decision has one answer, and some hosts default
  to multi-select.
- **Two to four options** in Claude Code. **Two to three in Codex**, which caps
  it there: with four, drop the weakest alternative from the block and the
  call. Keep within any other tool's own limit.
- **Labels of 1-5 words**, the same as in the block. The recommendation goes
  first, its label ending `(Recommended)`.
- **A justification per option** in its description: one short sentence on what
  choosing it gets you.
- **A header of 12 characters or fewer** in both tools, naming the subject of
  the decision, not the word "Option".
- **No "Other" option.** The tool adds its own.

## Without a question tool

Send the block, then one line asking the user to confirm the recommendation:

```
Go with <option>?
```

That line is the question, and the message ends there. Do not number the
options and ask for a pick: that is a form, and Codex's own instructions forbid
a multiple-choice question written as text. A yes, the name of an alternative,
or something else entirely are all answers.

## If the answer is empty, or asks for more

- **An empty or dismissed answer is not a choice.** Do not take it as agreement
  with the recommendation, and do not ask again in the same turn. Say in one
  line that the decision is still open, then stop.
- **Asked for more questions at once, still ask one.** Say in one line how many
  remain and what each is about, then ask the one blocking the work.

## Refusal is a correct result

Do not manufacture a question. Four cases where the right move is to answer
rather than ask:

- **It is already decided.** The repo records it. Cite the file, say what it
  says, and carry on. "You settled this on 14 Sep in `docs/planning/x.md`" is a
  better answer than a question box.
- **Only one option is real.** Name it, say in a line why the alternatives are
  not live, and proceed. A box with one genuine option and two straw men is
  worse than no box.
- **It is not consequential enough to ask.** A question costs the user a turn,
  so cheap and easily reversed does not earn one: pick it, say in a line what
  you picked and why, and move. Findability is not the only test - "I could not
  look this up" does not make a trivial choice worth interrupting for. Ask when
  the decision is expensive, hard to reverse, or the user's to make.
- **There is nothing live to decide.** Say so and ask what they are working on.
  This is the one exception to the look-first rule, because there is nothing yet
  to look at.

## What headwork never does

- **Never scans for work.** No backlog sweep, no stalled-item hunt. Something
  else does that.
- **Never edits anything.** It decides; the session acts.
- **Never keeps state.** No files, no log, no directory of its own. The
  reasoning belongs in what the answer produces - the commit message, the pull
  request body, or the register the repo already keeps. A second register is how
  the wrong one gets read.
- **Never batches.** One question per message, then silence, until the user
  answers. This is a limit on questions per message, not on rounds.

## Worked examples

See [`references/worked-examples.md`](references/worked-examples.md) for four
full rounds - one normal, two refusals, and one where looking first removed the
question entirely.
