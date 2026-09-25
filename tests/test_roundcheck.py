"""Tests for the round checker, and the checker run over every saved round.

The fixtures below are one good round and the ways it goes wrong. Each broken
round must fail, and fail for the right reason, or the checker is only
checking that it can parse.
"""

import copy
import pathlib
import re

import pytest

import roundcheck

REPO = pathlib.Path(__file__).resolve().parents[1]
SKILL_DIR = REPO / "skills" / "headwork"
EXAMPLES = SKILL_DIR / "references" / "worked-examples.md"
TRANSCRIPTS = sorted((REPO / "tests" / "transcripts").glob("*.md"))

BLOCK = """\
Checked: `cli.py`, the README and the release tags - `--out` has shipped in
every release since 1.0.

1. Removing a flag breaks every script that passes it.
2. An alias costs a few lines and no major release.

RECOMMENDED: Keep a warning alias. REASON: it ships in a minor release and
breaks nobody.
OVERTURNED IF: a 3.0 is already planned - then rename outright.
INSTEAD: Rename outright - one name everywhere. COST: a major release for one
flag.
INSTEAD: Keep a silent alias - nothing nags. COST: nobody learns the new name.
"""

TEXT = BLOCK + "\nGo with a warning alias?\n"

CALL = {
    "questions": [
        {
            "question": "How should the flag be renamed?",
            "header": "Flag rename",
            "multiSelect": False,
            "options": [
                {"label": "Keep a warning alias (Recommended)", "description": "No break."},
                {"label": "Rename outright", "description": "One name, in a major release."},
                {"label": "Keep a silent alias", "description": "Nothing nags."},
            ],
        }
    ]
}

CODEX_CALL = copy.deepcopy(CALL)
del CODEX_CALL["questions"][0]["multiSelect"]
CODEX_CALL["questions"][0]["id"] = "flag_rename"

FOURTH = "INSTEAD: Drop the flag - less to maintain. COST: breaks every script.\n"


def call_with(change):
    call = copy.deepcopy(CALL)
    change(call["questions"][0])
    return call


# --- Rounds that pass --------------------------------------------------------


def test_a_good_round_without_a_tool_passes():
    assert roundcheck.check_round(TEXT) == []


def test_a_good_round_with_askuserquestion_passes():
    assert roundcheck.check_round(BLOCK, "AskUserQuestion", CALL) == []


def test_a_good_round_with_request_user_input_passes():
    assert roundcheck.check_round(BLOCK, "request_user_input", CODEX_CALL) == []


def test_a_line_saying_how_many_remain_may_come_first():
    assert roundcheck.check_round("Two decisions left.\n\n" + TEXT) == []
    assert roundcheck.check_round("3 are open. This one blocks the rest.\n\n" + TEXT) == []


def test_without_a_tool_an_option_name_may_be_long():
    """Only a tool's label is capped at five words. In the text form the name
    is not a label, and SKILL.md sets it no limit."""
    long = TEXT.replace("Rename outright -", "Rename the flag outright in 3.0 -")
    assert roundcheck.check_round(long) == []


def test_bold_tokens_pass():
    """Markup is not structure. A model that bolds the tokens has kept the rule."""
    bold = TEXT.replace("RECOMMENDED:", "**RECOMMENDED:**").replace("COST:", "**COST:**")
    assert roundcheck.check_round(bold) == []


def test_a_question_run_on_to_the_last_option_is_still_found():
    assert roundcheck.check_round(BLOCK + "Go with a warning alias?\n") == []


# --- Rounds that fail, and why -----------------------------------------------

BROKEN_TEXT = {
    "a second question": (
        TEXT + "\nShould I update the changelog as well?\n",
        "not one",
    ),
    "an offer after the question": (
        TEXT + "\nLet me know if you want me to start on the tests.\n",
        "follows the question",
    ),
    "a question in the explainer": (
        TEXT.replace("2. An alias costs", "2. Do you want an alias? It costs"),
        "not one",
    ),
    "an alternative with no COST": (
        TEXT.replace(" COST: nobody learns the new name.", ""),
        "'Keep a silent alias' has no COST",
    ),
    "an alternative with no justification": (
        TEXT.replace("Rename outright - one name everywhere.", "Rename outright."),
        "no justification",
    ),
    "no Checked line": (
        TEXT.split("\n\n", 1)[1],
        "does not open with a Checked line",
    ),
    "a preamble that is not a count": (
        "Good question.\n\n" + TEXT,
        "comes before the Checked line",
    ),
    "one explainer point": (
        TEXT.replace("2. An alias costs a few lines and no major release.\n", ""),
        "1 points",
    ),
    "the recommendation not first": (
        TEXT.replace("RECOMMENDED:", "INSTEAD: Rename first - x. COST: y.\nRECOMMENDED:", 1),
        "do not start with RECOMMENDED",
    ),
    "no REASON": (
        TEXT.replace("REASON:", "because"),
        "no REASON",
    ),
    "a COST on the recommendation": (
        TEXT.replace("breaks nobody.", "breaks nobody. COST: a few lines."),
        "the recommendation has a COST",
    ),
    "no OVERTURNED IF": (
        TEXT.replace("OVERTURNED IF: a 3.0 is already planned - then rename outright.\n", ""),
        "OVERTURNED IF does not follow",
    ),
    "only one option": (
        re.sub(r"INSTEAD:.*?(?=\nGo with)", "", TEXT, flags=re.S),
        "only one option",
    ),
    "five options": (
        TEXT.replace("\nGo with", FOURTH + FOURTH.replace("Drop", "Hide") + "\nGo with"),
        "5 options, more than 4",
    ),
    "no question at all": (
        BLOCK,
        "no question after the options",
    ),
}


@pytest.mark.parametrize("message, reason", BROKEN_TEXT.values(), ids=list(BROKEN_TEXT))
def test_a_broken_round_without_a_tool_fails(message, reason):
    problems = roundcheck.check_round(message)
    assert any(reason in problem for problem in problems), problems


BROKEN_CALLS = {
    "a question in the message as well": (
        TEXT, "AskUserQuestion", CALL, "as well as the call",
    ),
    "two questions in the call": (
        BLOCK, "AskUserQuestion",
        {"questions": CALL["questions"] * 2},
        "asks 2 questions, not one",
    ),
    "multiSelect true": (
        BLOCK, "AskUserQuestion",
        call_with(lambda q: q.update(multiSelect=True)),
        "multiSelect is not false",
    ),
    "multiSelect left out": (
        BLOCK, "AskUserQuestion",
        call_with(lambda q: q.pop("multiSelect")),
        "multiSelect is not false",
    ),
    "a label that is not in the block": (
        BLOCK, "AskUserQuestion",
        call_with(lambda q: q["options"][1].update(label="Rename it")),
        "not the block's options",
    ),
    "no (Recommended) on the first label": (
        BLOCK, "AskUserQuestion",
        call_with(lambda q: q["options"][0].update(label="Keep a warning alias")),
        "does not end (Recommended)",
    ),
    "a long header": (
        BLOCK, "AskUserQuestion",
        call_with(lambda q: q.update(header="Renaming the flag")),
        "not 1-12 characters",
    ),
    "an Other option": (
        BLOCK, "AskUserQuestion",
        call_with(lambda q: q["options"].append({"label": "Other", "description": "x"})),
        "own Other option",
    ),
    "a label of six words": (
        BLOCK.replace("Rename outright -", "Rename it outright in one go -"),
        "AskUserQuestion",
        call_with(lambda q: q["options"][1].update(label="Rename it outright in one go")),
        "is 6 words",
    ),
    "a tool the checker does not know": (
        BLOCK, None, CALL, "does not name a question tool",
    ),
    "four options for Codex": (
        BLOCK + FOURTH, "request_user_input",
        {"questions": [dict(CODEX_CALL["questions"][0], options=CALL["questions"][0]["options"]
                            + [{"label": "Drop the flag", "description": "x"}])]},
        "4 options, more than 3",
    ),
    "multiSelect sent to Codex": (
        BLOCK, "request_user_input", CALL, "has no multiSelect field",
    ),
}


@pytest.mark.parametrize(
    "message, tool, call, reason", BROKEN_CALLS.values(), ids=list(BROKEN_CALLS)
)
def test_a_broken_round_with_a_tool_fails(message, tool, call, reason):
    problems = roundcheck.check_round(message, tool, call)
    assert any(reason in problem for problem in problems), problems


# --- The checker over everything saved ---------------------------------------


def test_the_block_in_skill_md_is_a_valid_round():
    """The block SKILL.md teaches and the grammar the checker enforces agree."""
    text = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
    block = re.search(r"^```\n(Checked: .*?)^```", text, re.M | re.S)
    assert block, "SKILL.md has no written-out block starting with Checked:"
    problems, options, rest = roundcheck.check_block(block.group(1))
    assert problems == [] and rest == []


def test_every_worked_example_round_passes():
    rounds = roundcheck.rounds_in_markdown(EXAMPLES.read_text(encoding="utf-8"))
    assert len(rounds) >= 3, "the worked examples lost their rounds"
    assert any(call for _, _, _, call in rounds), "no worked example uses a question tool"
    assert roundcheck.check_file(EXAMPLES) == []


def test_the_anti_pattern_fails():
    """The worked examples end on what headwork exists to stop. It must fail."""
    text = EXAMPLES.read_text(encoding="utf-8").split("## The anti-pattern")[1]
    quoted = [re.sub(r"^> ?", "", line) for line in text.splitlines() if line.startswith(">")]
    problems = roundcheck.check_round("\n".join(quoted))
    assert any("Checked line" in problem for problem in problems)
    assert any("questions, not one" in problem for problem in problems)


def test_there_are_saved_transcripts():
    assert TRANSCRIPTS, "tests/transcripts/ holds no saved replies"


@pytest.mark.parametrize("path", TRANSCRIPTS, ids=[p.name for p in TRANSCRIPTS])
def test_every_saved_transcript_passes(path):
    assert roundcheck.check_file(path) == []


def test_the_command_line_exits_non_zero_on_a_bad_round(tmp_path, capsys):
    good = tmp_path / "good.md"
    good.write_text("<!-- a saved reply -->\n" + TEXT, encoding="utf-8")
    bad = tmp_path / "bad.md"
    bad.write_text(TEXT + "\nAnd one more thing?\n", encoding="utf-8")
    assert roundcheck.main([str(good)]) == 0
    assert roundcheck.main([str(bad)]) == 1
    assert "bad.md:1:" in capsys.readouterr().out


def test_evals_are_not_run_in_ci():
    """evals/ is for occasional runs by hand, against a real model."""
    assert (REPO / "evals").is_dir(), "evals/ is missing"
    workflow = (REPO / ".github" / "workflows" / "validate.yml").read_text(encoding="utf-8")
    assert "evals" not in workflow
