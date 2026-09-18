---
name: headwork
description: >-
  Think a decision through, one question at a time. When the user is stuck or
  deciding what comes next, headwork explains the decision in plain English
  first, then asks a single question whose options each carry their
  justification and a named recommendation - and it never asks what it could
  have looked up. Use when the user says "headwork", "I'm stuck", "what's
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
4. **Ask one question**, in the format below for the harness you are in.
5. **Stop and wait.** No second question in the same message. No closing "and
   also". No "let me know if you'd like me to...".
6. **Hand the answer back to the session**, which does the work. If more remains
   to decide, say how many in one line, then raise the next one alone.

Step 5 is where this breaks in practice. A message that ends with a question box
**and** a trailing open question has asked two things, and the second one will be
ignored or answered badly.

## The five parts

Every question carries all five, in this order, in every harness:

1. **What you checked** - the sources, and anything they already settle.
2. **A bite-sized explainer** - two to four short numbered points.
3. **Two to four options** - fewer is not a decision, more is a menu.
4. **A justification per option** - and a stated cost on every option that is
   not the recommendation.
5. **A named recommendation**, placed first.

## The question box - Claude Code

Use `AskUserQuestion`. One question per call, never more, even though the tool
accepts up to four.

- **What you checked** and the **bite-sized explainer** go in the chat message
  immediately before the call, not inside the box. The box is the question; the
  message is what makes it answerable.
- **Two to four options.** Fewer than two is not a decision. More than four is a
  menu, and the tool caps it there anyway.
- **A named recommendation, first.** Its label ends `(Recommended)`. Its
  description opens with `RECOMMENDED.` then `REASON:` and the reason.
- **A justification per option** - what it gets you, in its own description, not
  inferable from the label.
- **Every option that is not the recommendation names its cost**, introduced by
  `COST:`. An option with no stated downside has not been thought about.
- **Keep the header under 12 characters** and make it the subject of the
  decision, not the word "Option".

The user always gets an "Other" escape from the tool itself, so do not spend one
of your four options on "something else".

## The text fallback - Codex and any other harness

No question-box tool means the same five parts in a fixed block. Do not
improvise a different shape each time, and do not fall back to prose:

```
Checked: <sources, and what they already settle>

<bite-sized explainer: 2 to 4 numbered points>

  1. <label> - RECOMMENDED. REASON: <justification>
  2. <label> - <justification>. COST: <what it gives up>
  3. <label> - <justification>. COST: <what it gives up>

Reply with a number, or say what you would rather do.
```

The `Checked:` line is **what you checked**, and it opens the block - there is
no separate message here to put it in. Then the **bite-sized explainer**. Then
**two to four options**, the same bound as the box, with **a named
recommendation** first marked `RECOMMENDED.`, **a justification per option**,
and a `COST:` on every alternative.

One decision per turn, then stop. The last line is the escape hatch the box
would have given for free.

## Refusal is a correct result

Do not manufacture a question. Three cases where the right move is to answer
rather than ask:

- **It is already decided.** The repo records it. Cite the file, say what it
  says, and carry on. "You settled this on 14 Sep in `docs/planning/x.md`" is a
  better answer than a question box.
- **Only one option is real.** Name it, say in a line why the alternatives are
  not live, and proceed. A box with one genuine option and two straw men is
  worse than no box.
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
- **Never batches.** One question, then silence, until the user answers.

## Worked examples

See [`references/worked-examples.md`](references/worked-examples.md) for three
full rounds - one normal, one refusal, one where looking first removed the
question entirely.
