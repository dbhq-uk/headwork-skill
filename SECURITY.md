# Security

## Reporting

Email **dan@dbhq.uk**. Please do not open a public issue for a vulnerability.

Expect an acknowledgement within a few days. If the report is valid you will be
credited in the fix unless you would rather not be.

## What headwork does with your data

Very little, because it is instructions rather than a program.

- **No network access.** headwork makes no request to anything. It has no
  endpoint, no account and no telemetry.
- **No credentials.** Nothing to store, so nothing to leak.
- **No state on disk.** No config file, no run log, no directory of its own. It
  writes nothing anywhere, which is a stated design rule with a test behind it.
- **No execution.** There are no scripts in this repository. Installing it
  places a symlink to a directory of markdown.

## The one thing worth knowing

headwork instructs an agent to **read your repository before asking you a
question** - git history, source files, open issues, whatever bears on the
decision. That reading happens in your own agent session, with whatever
permissions you have already granted it, and nothing leaves that session by way
of headwork.

But the agent's own model provider sees what the agent reads. That is true of
any agent session and headwork does not change it. It does mean headwork will
often cause more of your repository to be read than a question-free conversation
would, which is the trade for not being asked things your files already answer.

If a repository is sensitive enough that you mind which files an agent opens,
constrain that at the agent's permission layer, not here.
