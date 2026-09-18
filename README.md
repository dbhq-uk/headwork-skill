<div align="center">

<img src="assets/logo.svg" alt="headwork - one decision at a time, with a recommendation, by DBHQ" width="560">

# headwork

**One decision at a time, with a recommendation**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude_Code-Plugin-blueviolet)](https://code.claude.com/docs/en/plugins)
[![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20macOS%20%7C%20WSL-lightgrey)]()

A free, open-source tool by [DBHQ](https://dbhq.uk) - documented at [skills.dbhq.uk](https://skills.dbhq.uk/headwork/)

</div>

---

The decision blocking you right now, explained in plain English and put as a
single question whose options each carry their justification and a named
recommendation - and never a question it could have answered by looking.

## What makes it different

Ask an agent to unblock you and three things usually go wrong at once. It asks
several questions in one message, as prose. It offers options as bare labels, so
choosing means reconstructing the trade-off yourself. And it asks things it
could have looked up, which is worse than not asking at all.

headwork fixes the third one first, because it is the one that matters:

> **Never ask what you can find out.**

Before every question it looks - the session, `git log`, the file, the open
issues, the register - and then states in one line what it checked and what that
settled. A question a file could have answered is a bug, not a style lapse.

The rule earns its keep by deleting questions. The best round headwork runs is
the one where looking removes the decision entirely, and it tells you that
instead of building a nicely formatted box around a question nobody needed to
answer.

## What a round looks like

1. **Look** - session first, then whatever the decision touches.
2. **Say what you checked**, in one line, including anything it already settles.
3. **Explain in bite-sized chunks** - two to four short points, plain English.
4. **Ask one question** - two to four options, the recommendation named first,
   every option carrying its justification and every alternative its cost.
5. **Stop and wait.** No second question, no trailing "and also".
6. **Hand the answer back** to the session, which does the work.

## What it will not do

- **headwork never goes looking for work.** No backlog sweep, no stalled-item
  hunt, no scheduled triage. You bring the thing you are stuck on, or it asks
  what you are working on.
- **headwork never edits anything.** It decides; the session does the work with
  the tools it already has.
- **headwork keeps no state.** No log, no files, no directory of its own. The
  reasoning belongs in what the answer produces - the commit message, the pull
  request body, or the register the repo already keeps.

## Install

### As a Claude Code plugin (recommended)

```
/plugin marketplace add dbhq-uk/marketplace
/plugin install headwork@dbhq
```

### Any agent (Cursor, Copilot, Windsurf, Gemini, Cline and more)

```bash
npx skills add dbhq-uk/headwork-skill
```

### From source

```bash
git clone https://github.com/dbhq-uk/headwork-skill.git
cd headwork-skill
./install.sh          # Claude Code
./install-codex.sh    # Codex
```

Nothing to configure. No dependencies, no credentials, no state directory.

## Codex and other harnesses

The question box is a Claude Code tool. Codex has none, so headwork ships a
**specified** text fallback rather than an improvised one - the same five parts
in a fixed block, one decision per turn, then stop and wait. The two paths are
held in step by test, so the Codex side cannot quietly rot into prose.

## Using it

It fires on its own when you say you are stuck, ask what comes next, or ask to
be unblocked. You can also call it directly:

```
/headwork
```

There is nothing to pass it. It reads what the session is already working on.

## Also from DBHQ

Sixteen free agent skills, all of them installable from the same marketplace and
all documented at **[skills.dbhq.uk](https://skills.dbhq.uk)**. The marketplace
itself is [dbhq-uk/marketplace](https://github.com/dbhq-uk/marketplace) - one
`/plugin marketplace add` and every one of them is available.

Five of them share the `-work` suffix because they share a shape - each does one
part of getting work done, and none needs the others. `legwork` researches,
**headwork** decides, `deskwork` tracks and orders, `buildwork` executes, and
`groupwork` puts a second agent on any of it.

| Skill | What it does |
|---|---|
| [outlook](https://skills.dbhq.uk/outlook/) | Microsoft 365 mail and calendar, from the terminal |
| [trello](https://skills.dbhq.uk/trello/) | Your boards, run from your agent |
| [legwork](https://skills.dbhq.uk/legwork/) | Research that settles a decision, and says when it cannot |
| [dovetail](https://skills.dbhq.uk/dovetail/) | Checks whether your repository still agrees with itself |
| [verve](https://skills.dbhq.uk/verve/) | Strips AI tells from prose and puts a voice back |
| [vela](https://skills.dbhq.uk/vela/) | Compiler-exact code search, in any language you index |
| [garmin](https://skills.dbhq.uk/garmin/) | Your Garmin data, answered in the terminal |
| [imager](https://skills.dbhq.uk/imager/) | Images from GPT Image 2, costed before it spends |
| [gitview](https://skills.dbhq.uk/gitview/) | Which branches are finished, and safe to delete |
| [atlassian](https://skills.dbhq.uk/atlassian/) | Jira issues and Confluence pages |
| [pennyblack](https://skills.dbhq.uk/pennyblack/) | A physical letter, posted from the terminal |
| [buildwork](https://skills.dbhq.uk/buildwork/) | Your open issues, run as parallel agents |
| [deskwork](https://skills.dbhq.uk/deskwork/) | What an agent noticed, tracked as real work |
| [groupwork](https://skills.dbhq.uk/groupwork/) | A second agent on the work, and a result you can cite |

Plus [heliograph](https://skills.dbhq.uk/heliograph/), for a machine you cannot log into.

## Contributing

Issues and pull requests welcome - see [`CONTRIBUTING.md`](CONTRIBUTING.md), and
read [`AGENTS.md`](AGENTS.md) first for the rules this skill does not break.

## Licence

MIT - see [`LICENSE`](LICENSE).
