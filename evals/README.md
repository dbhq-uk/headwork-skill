# Evals

Prompt cases for running headwork against a real model, by hand, now and then.
They are **not** run in CI, and a test makes sure of that.

The tests in `tests/` check what can be checked offline: that `SKILL.md` states
its rules, and that every saved round has the right shape. They cannot check
what a model does. These cases can. Each one targets a behaviour the offline
checker cannot see, such as a question a file could have answered, or a
session that never stops.

## Running a case

1. Build the scratch repository the case describes, and commit it.
2. Start a session there with headwork installed, and send the prompt. Some
   cases then script one or more answers.
3. Save the reply to a file, exactly as it came. With a question tool, quote
   the message with `> ` and put the call after it as a `json` block, with
   the tool's name in backticks in the line before. See
   `skills/headwork/references/worked-examples.md` for the shape.
4. Run the checker over it:

   ```bash
   python3 tests/roundcheck.py reply.md
   ```

5. Judge the rest against the case's "Passes when". The checker sees shape,
   not judgement.

A reply that is a round and passes both can go in `tests/transcripts/`, with
an HTML comment at the top saying which case, which harness and which commit
of `SKILL.md`. CI then checks it on every push, which holds the checker to
real output rather than to fixtures written for it.

## The cases

See [`cases.md`](cases.md).
