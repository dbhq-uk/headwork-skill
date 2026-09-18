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

Asking one thing at a time and looking before you ask are table stakes - other
skills do both. The argued recommendation is the part that is actually worth
installing something for.

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

Every question carries all six, in this order, in every harness:

1. **What you checked** - the sources, and anything they already settle.
2. **A bite-sized explainer** - two to four short numbered points.
3. **Two to four options** - fewer is not a decision, more is a menu.
4. **A justification per option** - and a stated cost on every option that is
   not the recommendation.
5. **A named recommendation**, placed first.
6. **What would overturn the recommendation** - the condition that would make a
   different option right.

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
- **What would overturn it**, in the same description, introduced by
  `OVERTURNED IF:`. One clause naming the condition under which a different
  option wins.
- **A justification per option** - what it gets you, in its own description, not
  inferable from the label.
- **Every option that is not the recommendation names its cost**, introduced by
  `COST:`. An option with no stated downside has not been thought about.
- **Keep the header under 12 characters** and make it the subject of the
  decision, not the word "Option".

The user always gets an "Other" escape from the tool itself, so do not spend one
of your four options on "something else".

## The text fallback - Codex and any other harness

No question-box tool means the same six parts in a fixed block. Do not
improvise a different shape each time, and do not fall back to prose:

```
Checked: <sources, and what they already settle>

<bite-sized explainer: 2 to 4 numbered points>

  1. <label> - RECOMMENDED. REASON: <justification>
     OVERTURNED IF: <the condition that makes another option right>
  2. <label> - <justification>. COST: <what it gives up>
  3. <label> - <justification>. COST: <what it gives up>

Reply with a number, or say what you would rather do.
```

The `Checked:` line is **what you checked**, and it opens the block - there is
no separate message here to put it in. Then the **bite-sized explainer**. Then
**two to four options**, the same bound as the box, with **a named
recommendation** first marked `RECOMMENDED.`, its **`OVERTURNED IF:`** clause
saying **what would overturn it**, **a justification per option**, and a
`COST:` on every alternative.

One question per turn, then stop and wait. The last line is the escape hatch the
box would have given for free.

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
