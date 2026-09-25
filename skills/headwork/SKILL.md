---
name: headwork
description: >-
  Think a decision through, one question at a time, with a recommendation you
  can argue with. When the user is stuck between options on the work in hand,
  headwork explains the decision, asks one question with a justification on
  every option, names the recommendation and says what would overturn it. It
  never asks what it could have looked up. Use when the user says "headwork",
  "I'm stuck between", "stuck on which", "how do I move this forward", "unblock
  me", "unblock this", "which way", "help me decide", "I can't decide", "what
  should I do here", or "talk me through the options". Not for designing
  something new, stress-testing a whole plan, or picking the next issue.
license: MIT
---

# headwork

Take the one decision blocking the work in hand and put it to the user as one
question they answer by **choosing**, not by composing. Name a recommendation
and say what would overturn it, so disagreeing means checking a condition, not
overruling a machine.

## When not to use

- **Designing a new thing** - `superpowers:brainstorming`.
- **Stress-testing a whole plan** - grill-me, from
  [`mattpocock/skills`](https://github.com/mattpocock/skills).
- **An independent model's view** - `groupwork`.
- **Which issue comes next** - `deskwork`.
- **A stalled Trello board** - `life-manager`.
- **A failing problem rather than a choice** -
  `superpowers:systematic-debugging` or `paseo-committee`.

## Never ask what you can find out

Before every question, look: the session first, then whatever the decision
touches - `git log`, the file, open issues, the register, the tests. Say in one
line what you checked and what it settled; that line is the proof you looked. A
question a file could have answered is a bug.

## A round, exactly

1. **Look.**
2. **Say what you checked**, in one line.
3. **Explain** in two to four short numbered points: just enough that the
   options mean something.
4. **Ask one question**, in the form for your tools.
5. **Stop and wait.** No second question in the same message, no closing "and
   also", no "let me know if you'd like me to...".
6. **Carry out the chosen option as normal work, before any next round.** Start
   a new round only if another decision blocks the work.

Go on for as many rounds as it takes to unblock the user: there is no cap on
rounds, only on questions per message. Before each new round, say in one line
how many decisions remain. **The session is done when the work can take its
next action without another decision from the user.** After more than one
round, end with a recap, one line per decision. The recap lives in the
conversation, not in a file.

## The six parts

Every question carries these six parts, in this order, however it is asked:

```
Checked: <sources, and what they already settle>

1. <explainer point>
2. <explainer point>

RECOMMENDED: <option>. REASON: <justification>.
OVERTURNED IF: <the condition that makes another option right>.
INSTEAD: <option> - <justification>. COST: <what it gives up>.
```

One to three `INSTEAD:` lines, so two to four options in all. Only the
alternatives carry a `COST:`.

## Choosing how to ask

Choose by what your tools can do, not by which harness you are in. Use a
question tool if you have one: `AskUserQuestion` (Claude Code),
`request_user_input` (Codex), `question` (OpenCode) or `ask_user` (Gemini CLI).
A subagent or `codex exec` often has none, so ask in plain text.

## With a question tool

Send the block as the message, then call the tool. One question per call.

- **`multiSelect: false`.** Some hosts default to multi-select.
- **Two to four options** in Claude Code, **two to three in Codex**, and within
  any other tool's limit. With four in Codex, drop the weakest alternative from
  the block and the call.
- **Labels of 1-5 words**, as in the block. The recommendation goes first, its
  label ending `(Recommended)`.
- **A one-sentence description** per option. **A header of 12 characters or
  fewer**, naming the subject. No "Other" option: the tool adds one.

## Without a question tool

Send the block, then one line confirming the recommendation, and stop:

```
Go with <option>?
```

Do not number the options and ask for a pick: that is a form.

## Taking the answer

- **A choice, including one against the recommendation.** Take it, and do not
  argue it again. Flag it once only if it breaks a stated constraint.
- **"Just pick" or "you decide".** Take the recommendation and say so.
- **An "Other" answer.** Read it as the choice.
- **No answer, or an empty one.** It is not a choice. Say the decision is still
  open, and stop.
- **Asked for more questions at once, still ask one.** Say in one line how many
  remain and what each is about, then ask the one blocking the work.

## Refusal is a correct result

Do not manufacture a question. Answer instead when:

- **It is already decided.** Cite the file, say what it says, carry on.
- **Only one option is real.** Name it, say why the others are not live, and
  proceed.
- **It is not consequential enough to ask.** Cheap and easily reversed gets
  decided and stated, even when nothing could be looked up:
  findability is not the only test. Ask when the decision is expensive, hard to
  reverse, or the user's to make.
- **There is nothing live to decide.** Say so, and ask what they are working
  on. It is the one question asked without looking first.

## What headwork never does

- **Never scans for work.** No backlog sweep, no stalled-item hunt.
- **Never edits anything.** The session acts, as step 6 says.
- **Never keeps state.** No files, no log, no directory of its own. Reasoning
  goes in the commit or the pull request.

## Worked examples

[`references/worked-examples.md`](references/worked-examples.md) has seven,
including a round with no question tool and an overturned recommendation.
