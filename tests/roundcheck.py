"""Check that a headwork round follows the format in SKILL.md.

A round is the message the user sees and, when a question tool is used, the
one call that follows it. This checks the shape, offline and without a model:

- It opens with a Checked line. At most one line may come first, and it has
  to give a count: how many decisions remain.
- Two to four numbered explainer points come next.
- Then the options. RECOMMENDED comes first, with a REASON and no COST. Then
  OVERTURNED IF. Then one to three INSTEAD lines, each with a justification
  and a COST. That is two to four options in all, and two to three for
  Codex's request_user_input.
- There is one question and nothing follows it. Without a tool, it is the
  last line of the message. With a tool, it is in the call, and the message
  asks nothing.
- With a tool, the call keeps to that tool's limits, and its labels are the
  block's option names: 1-5 words each, the recommendation first.

It cannot tell whether the Checked line is true, or whether the question was
worth asking. The prompt cases in evals/ cover those, by hand.

In a markdown file, a round is a quoted block that holds a RECOMMENDED line.
With a question tool, the call follows it as a ```json block, and the
paragraph before that block names the tool in backticks. Without one, the
quoted block ends with the question. A file with no quoted block is read as
one message sent without a tool, so a reply can be saved exactly as it came.

    python3 tests/roundcheck.py FILE...

Standard library only, Python 3.9 or newer.
"""

import json
import re
import sys
from pathlib import Path

# The limits each question tool sets. A tool not listed here is refused rather
# than guessed at: add it with its real limits.
TOOLS = {
    "AskUserQuestion": {"max_options": 4, "multi_select_field": True},
    "request_user_input": {"max_options": 3, "multi_select_field": False},
}
MAX_OPTIONS = 4
TOKENS = ("Checked:", "RECOMMENDED:", "OVERTURNED IF:", "INSTEAD:")
MARK = "(Recommended)"
COUNT = r"\b(\d+|one|two|three|four|five|six|seven|eight|nine|ten)\b"


def _items(message):
    """Split a message into items, each a (kind, text) pair.

    An item starts at a line that begins with a token or a number, and runs on
    over wrapped lines until a blank line or the next such line. Any other line
    after a blank starts a 'prose' item. So does a line that ends in a question
    mark, because that line is a question.
    """
    items = []
    for raw in message.replace("**", "").splitlines():
        line = raw.strip()
        if not line:
            items.append(None)
            continue
        kind = next((token for token in TOKENS if line.startswith(token)), None)
        if kind is None and re.match(r"\d+\. ", line):
            kind = "point"
        if kind is None and line.endswith("?"):
            kind = "prose"
        if kind is None and items and items[-1] is not None:
            items[-1] = (items[-1][0], items[-1][1] + " " + line)
            continue
        items.append((kind or "prose", line))
    return [item for item in items if item is not None]


def _questions(text):
    """How many question marks text holds, outside inline code."""
    return re.sub(r"`[^`]*`", "", text).count("?")


def _words(name):
    return len(name.replace(MARK, "").split())


def _start(text):
    return text if len(text) <= 50 else text[:47] + "..."


def check_block(message, max_options=MAX_OPTIONS):
    """Check the written-out block. Return (problems, options, rest).

    options is the option names in order, the recommendation first. rest is the
    items after the last INSTEAD line, for check_round to judge.
    """
    problems = []
    items = _items(message)
    i = 0

    def kind(at):
        return items[at][0] if at < len(items) else None

    if kind(0) == "prose" and kind(1) == "Checked:":
        if not re.search(COUNT, items[0][1].lower()):
            problems.append(
                f"{_start(items[0][1])!r} comes before the Checked line, and only "
                "a line saying how many decisions remain may"
            )
        i = 1
    if kind(i) != "Checked:":
        problems.append("the round does not open with a Checked line")
        return problems, [], items[i:]
    i += 1

    numbers = []
    while kind(i) == "point":
        numbers.append(int(re.match(r"\d+", items[i][1]).group(0)))
        i += 1
    if not 2 <= len(numbers) <= 4:
        problems.append(f"the explainer has {len(numbers)} points, not two to four")
    elif numbers != list(range(1, len(numbers) + 1)):
        problems.append(f"the explainer points are numbered {numbers}")

    if kind(i) != "RECOMMENDED:":
        problems.append("the options do not start with RECOMMENDED")
        return problems, [], items[i:]
    text = items[i][1]
    name, reason, _ = text[len("RECOMMENDED:"):].partition("REASON:")
    options = [name.strip().rstrip(".").strip()]
    if not reason:
        problems.append("the recommendation has no REASON")
    if "COST:" in text:
        problems.append(
            "the recommendation has a COST; what it gives up is its OVERTURNED IF"
        )
    i += 1

    if kind(i) == "OVERTURNED IF:":
        i += 1
    else:
        problems.append("OVERTURNED IF does not follow the recommendation")

    while kind(i) == "INSTEAD:":
        body = items[i][1][len("INSTEAD:"):]
        name, dash, _ = body.partition(" - ")
        options.append(name.strip())
        if not dash:
            problems.append(f"alternative {name.strip()!r} has no justification after ' - '")
        if "COST:" not in body:
            problems.append(f"alternative {name.strip()!r} has no COST")
        i += 1

    if len(options) < 2:
        problems.append("there is no INSTEAD line, so there is only one option")
    if len(options) > max_options:
        problems.append(f"{len(options)} options, more than {max_options}")
    return problems, options, items[i:]


def check_call(call, tool, options):
    """Check the one question-tool call against the tool's limits and the block."""
    if tool not in TOOLS:
        return [f"the call does not name a question tool the checker knows: {sorted(TOOLS)}"]
    limits = TOOLS[tool]
    questions = call.get("questions")
    if not isinstance(questions, list) or len(questions) != 1:
        count = len(questions) if isinstance(questions, list) else 0
        return [f"the call asks {count} questions, not one"]
    question = questions[0]
    problems = []

    header = question.get("header", "")
    if not 1 <= len(header) <= 12:
        problems.append(f"header {header!r} is not 1-12 characters")
    elif header.lower().startswith("option"):
        problems.append(f"header {header!r} does not name the subject")
    text = question.get("question", "")
    if not text.endswith("?") or text.count("?") != 1:
        problems.append(f"the call's question is not one question: {text!r}")
    if limits["multi_select_field"]:
        if question.get("multiSelect") is not False:
            problems.append("multiSelect is not false")
    else:
        if "multiSelect" in question:
            problems.append(f"{tool} has no multiSelect field")
        if not question.get("id"):
            problems.append(f"{tool} needs an id")

    choices = question.get("options") or []
    labels = [choice.get("label", "") for choice in choices]
    if not 2 <= len(labels) <= limits["max_options"]:
        problems.append(f"{len(labels)} options, not 2-{limits['max_options']} for {tool}")
    for label in labels:
        if not 1 <= _words(label) <= 5:
            problems.append(f"label {label!r} is {_words(label)} words, not 1-5")
    for choice in choices:
        if not choice.get("description", "").strip():
            problems.append(f"option {choice.get('label')!r} has no description")
    if any(label.strip().lower() == "other" for label in labels):
        problems.append("the call has its own Other option, and the tool adds one")
    if labels and not labels[0].endswith(MARK):
        problems.append(f"the first label does not end {MARK}")
    if any(MARK in label for label in labels[1:]):
        problems.append(f"a label after the first says {MARK}")
    names = [label.replace(MARK, "").strip() for label in labels]
    if options and names != options:
        problems.append(f"the call's labels {names} are not the block's options {options}")
    return problems


def check_round(message, tool=None, call=None):
    """Check one round, and return its problems. None means it passes.

    With a call, the question is in the call and the message asks nothing.
    Without one, the message ends with its only question.
    """
    max_options = TOOLS[tool]["max_options"] if tool in TOOLS else MAX_OPTIONS
    problems, options, rest = check_block(message, max_options)
    asked = _questions(message)

    if call is None:
        if not rest:
            problems.append("there is no question after the options")
        elif not rest[0][1].endswith("?"):
            problems.append(f"{_start(rest[0][1])!r} follows the options, not a question")
        elif len(rest) > 1:
            problems.append(f"{_start(rest[1][1])!r} follows the question")
        if asked > 1:
            problems.append(f"the message asks {asked} questions, not one")
    else:
        if rest:
            problems.append(f"{_start(rest[0][1])!r} follows the options")
        if asked:
            problems.append("the message asks a question as well as the call")
        problems += check_call(call, tool, options)
    return problems


def rounds_in_markdown(text):
    """Every round in a markdown file, as (line, message, tool, call).

    A file with no quoted block at all is one message, sent without a tool.
    HTML comments are ignored, so a saved reply can say where it came from.
    """
    text = re.sub(r"<!--.*?-->", lambda m: "\n" * m.group(0).count("\n"), text, flags=re.S)
    lines = text.splitlines()
    if not any(line.startswith(">") for line in lines):
        return [(1, text, None, None)] if text.strip() else []

    rounds = []
    i = 0
    while i < len(lines):
        if not lines[i].startswith(">"):
            i += 1
            continue
        start = i + 1
        quoted = []
        while i < len(lines) and lines[i].startswith(">"):
            quoted.append(re.sub(r"^> ?", "", lines[i]))
            i += 1
        message = "\n".join(quoted)
        if not re.search(r"^(\*\*)?RECOMMENDED:", message, re.M):
            continue

        # The call, if there is one, comes before the next quote or heading.
        tool = call = None
        paragraph, fresh = [], False
        for j in range(i, len(lines)):
            line = lines[j]
            if line.startswith((">", "#")):
                break
            if line.startswith("```json"):
                end = next(k for k in range(j + 1, len(lines)) if lines[k].startswith("```"))
                call = json.loads("\n".join(lines[j + 1:end]))
                named = [name for name in TOOLS if f"`{name}`" in " ".join(paragraph)]
                tool = named[0] if len(named) == 1 else None
                break
            if not line.strip():
                fresh = True
                continue
            if fresh:
                paragraph, fresh = [], False
            paragraph.append(line)
        rounds.append((start, message, tool, call))
    return rounds


def check_file(path):
    """Every problem in every round of a file, as 'path:line: problem'."""
    rounds = rounds_in_markdown(Path(path).read_text(encoding="utf-8"))
    if not rounds:
        return [f"{path}: no round found"]
    return [
        f"{path}:{line}: {problem}"
        for line, message, tool, call in rounds
        for problem in check_round(message, tool, call)
    ]


def main(paths):
    if not paths:
        print("usage: python3 tests/roundcheck.py FILE...", file=sys.stderr)
        return 2
    found = [problem for path in paths for problem in check_file(path)]
    for problem in found:
        print(problem)
    return 1 if found else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
