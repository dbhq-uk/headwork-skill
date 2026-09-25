"""Structural tests for the headwork skill.

headwork is instructions, not a program, so these tests assert that SKILL.md
states its rules and that both ways of asking carry the same parts. They
cannot test how a model behaves after reading the file, and they do not pretend
to. See AGENTS.md, which states that limit rather than hiding it.

The rules under test are the ones in AGENTS.md:

  1. Never ask what you can find out
  2. One question per message, then stop - rounds are NOT capped
  3. Every option carries a justification, and every alternative its cost
  3a. The recommendation says what would overturn it
  4. Both ways of asking - with a question tool and without - carry the same
     six parts, and the way is chosen by capability, not harness name
  5. Findability is not the only test - consequence is the other one

Plus the three things headwork must never grow: a scanner, write access, state.
"""

import pathlib
import re

import pytest

REPO = pathlib.Path(__file__).resolve().parents[3]
SKILL_DIR = REPO / "skills" / "headwork"
SKILL_MD = SKILL_DIR / "SKILL.md"


@pytest.fixture(scope="module")
def skill_text():
    return SKILL_MD.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def skill_lower(skill_text):
    return skill_text.lower()


def section(text, heading):
    """The body of one '## ' section, up to the next '## ' or end of file."""
    pattern = re.compile(
        r"^## " + re.escape(heading) + r"\s*$(.*?)(?=^## |\Z)",
        re.M | re.S,
    )
    match = pattern.search(text)
    assert match, f"SKILL.md has no '## {heading}' section"
    return match.group(1).lower()


def flat(text):
    """Text with every run of whitespace collapsed, so a wrapped phrase matches."""
    return " ".join(text.split())


def fenced_blocks(text):
    """Every fenced code block in text, in order, without its fences."""
    return re.findall(r"^```[^\n]*\n(.*?)^```", text, re.M | re.S)


# --- The manifest and the frontmatter ------------------------------------


def test_frontmatter_name_matches_directory(skill_text):
    match = re.match(r"^---\n(.*?)\n---", skill_text, re.S)
    assert match, "SKILL.md has no frontmatter"
    name = re.search(r"^name:\s*(\S+)", match.group(1), re.M)
    assert name, "frontmatter has no name"
    assert name.group(1) == SKILL_DIR.name


def test_description_names_the_trigger_phrases(skill_text):
    """The description is the auto-trigger. If the phrases go, it never fires.

    Whitespace is collapsed first: the description is a folded YAML block, so a
    phrase can land either side of a line break and still be one phrase.
    """
    match = re.match(r"^---\n(.*?)\n---", skill_text, re.S)
    description = " ".join(match.group(1).lower().split())
    for phrase in ("stuck", "what's next", "unblock", "decide"):
        assert phrase in description, f"description no longer triggers on {phrase!r}"


# --- Rule 1: never ask what you can find out -----------------------------


def test_look_first_rule_is_stated(skill_lower):
    assert "never ask what you can find out" in skill_lower


def test_look_first_rule_is_not_hedged(skill_lower):
    """A conditional look-first rule is not a rule."""
    for hedge in (
        "never ask what you can find out, where practical",
        "never ask what you can find out if time",
        "where possible, never ask what you can find out",
    ):
        assert hedge not in skill_lower


def test_the_checked_line_is_required(skill_lower):
    """The stated 'what I checked' line is the enforcement mechanism."""
    assert "what you checked" in skill_lower


# --- Rule 2: one question per message, then stop --------------------------


def test_one_question_per_message_is_stated(skill_lower):
    assert "one question per call" in skill_lower
    assert "no second question in the same message" in skill_lower


def test_stop_and_wait_is_stated(skill_lower):
    assert "stop and wait" in skill_lower


# --- Rule 3: justification per option, cost per alternative ---------------


def test_option_bounds_are_stated(skill_text):
    parts = section(skill_text, "The six parts")
    tool = section(skill_text, "With a question tool")
    assert "two to four options" in parts, "the six parts lost the option bound"
    assert "two to four options" in tool, "the tool path lost the option bound"


# --- Rule 3a: the recommendation says what would overturn it ---------------


def test_the_overturn_clause_is_required(skill_lower):
    """A recommendation with no stated escape is an anchor, not advice."""
    assert "what would overturn" in skill_lower
    assert "overturned if:" in skill_lower


def test_the_overturn_clause_is_in_the_block(skill_text):
    block = fenced_blocks(section(skill_text, "The six parts"))
    assert block, "'The six parts' lost its written-out block"
    assert "overturned if:" in block[0], "the block lost the OVERTURNED IF clause"


# --- Rule 4: both ways of asking carry the same parts ----------------------

# The six parts, and a marker that must appear in 'The six parts' section.
SIX_PARTS = {
    "what you checked": "what you checked",
    "bite-sized explainer": "bite-sized",
    "two to four options": "two to four options",
    "justification per option": "justification",
    "named recommendation": "recommend",
    "what would overturn it": "overturn",
}

# The written-out block carries each part as a token a reader can see.
BLOCK_TOKENS = {
    "what you checked": r"^checked: ",
    "bite-sized explainer": r"^1\. ",
    "named recommendation, with its justification": r"^recommended: .*reason: ",
    "what would overturn it": r"^overturned if: ",
    "an alternative, with its justification and cost": r"^instead: .* - .*cost: ",
}

# Each way of asking sends the block, so each carries all six parts. A new
# way of asking added per CONTRIBUTING.md goes in this list.
HARNESS_SECTIONS = [
    "With a question tool",
    "Without a question tool",
]


def test_the_six_parts_are_stated_once_up_front(skill_text):
    parts = section(skill_text, "The six parts")
    for part, marker in SIX_PARTS.items():
        assert marker in parts, f"'The six parts' no longer names {part}"


def test_the_block_carries_the_six_parts_in_order(skill_text):
    block = fenced_blocks(section(skill_text, "The six parts"))[0]
    positions = []
    for part, token in BLOCK_TOKENS.items():
        match = re.search(token, block, re.M)
        assert match, f"the block is missing {part}"
        positions.append(match.start())
    assert positions == sorted(positions), "the block's parts are out of order"


@pytest.mark.parametrize("heading", HARNESS_SECTIONS)
def test_both_paths_carry_the_same_parts(skill_text, heading):
    """The no-tool path is the one at risk - nobody develops headwork there.

    Both paths send the same block, so both carry the same six parts. A path
    that stops sending it has stopped carrying them.
    """
    body = section(skill_text, heading)
    assert "send the block" in flat(body), f"{heading!r} no longer sends the block"


def test_the_format_is_chosen_by_capability_not_harness_name(skill_text):
    body = flat(section(skill_text, "Choosing how to ask"))
    assert "not by which harness" in body
    for tool in ("askuserquestion", "request_user_input", "`question`", "ask_user"):
        assert tool in body, f"'Choosing how to ask' no longer names {tool}"
    assert "subagent" in body, "the no-tool case inside a tooled harness is gone"


@pytest.mark.parametrize(
    "path", ["skills/headwork/SKILL.md", "README.md", "install-codex.sh", "AGENTS.md"]
)
def test_nothing_says_codex_has_no_question_tool(path):
    """Codex ships request_user_input. Saying otherwise sends it a text menu
    that its own system prompt forbids."""
    text = " ".join((REPO / path).read_text(encoding="utf-8").lower().split())
    for claim in ("codex has none", "codex has no question", "codex has no ask"):
        assert claim not in text, f"{path} still says {claim!r}"


def test_the_tool_path_sets_single_select_and_the_limits(skill_text):
    """Some hosts default to multi-select, and Codex caps options at three."""
    body = flat(section(skill_text, "With a question tool"))
    assert "multiselect: false" in body
    assert "two to three in codex" in body
    assert "1-5 words" in body
    assert "12 characters or fewer" in body
    assert "(recommended)" in body
    assert "one question per call" in body


def test_the_no_tool_path_is_one_confirming_question(skill_text):
    """Not a numbered menu: Codex's own prompt forbids a text multiple choice."""
    body = section(skill_text, "Without a question tool")
    blocks = fenced_blocks(body)
    assert len(blocks) == 1, "the no-tool path should show exactly one question line"
    lines = [line for line in blocks[0].splitlines() if line.strip()]
    assert len(lines) == 1 and lines[0].rstrip().endswith("?")
    assert "do not number the options" in flat(body)


def test_an_empty_answer_and_a_request_for_more_are_covered(skill_text):
    body = flat(section(skill_text, "If the answer is empty, or asks for more"))
    assert "not a choice" in body
    assert "still ask one" in body


def test_worked_example_labels_are_one_to_five_words():
    """Both question tools ask for option labels of 1-5 words."""
    text = (SKILL_DIR / "references" / "worked-examples.md").read_text(encoding="utf-8")
    labels = re.findall(r"^\| \*\*(.+?)\*\* \|", text, re.M)
    assert labels, "no option labels found in the worked examples"
    for label in labels:
        words = label.replace("(Recommended)", "").split()
        assert 1 <= len(words) <= 5, f"label is {len(words)} words: {label!r}"


# --- Rule 5: consequence, not just findability -----------------------------


def test_the_consequence_gate_is_stated(skill_lower):
    """'I could not look it up' does not make a trivial decision worth a turn."""
    assert "not consequential enough" in skill_lower
    assert "findability is not the only test" in skill_lower


# --- Refusal is a correct result ------------------------------------------


def test_all_four_refusal_cases_survive(skill_text):
    body = section(skill_text, "Refusal is a correct result")
    assert "already decided" in body
    assert "only one option is real" in body
    assert "not consequential enough" in body
    assert "nothing live to decide" in body


# --- Rounds are unlimited, questions per message are not -------------------


def test_rounds_are_not_capped(skill_lower):
    """Dan, 18 Sep 2026: keep going for as many rounds as it takes."""
    assert "as many rounds as it takes" in skill_lower
    assert "no cap" in skill_lower


def test_the_cap_is_per_message_not_per_session(skill_lower):
    assert "questions per message" in skill_lower


# --- The three things headwork must never grow ----------------------------

STATE_PATHS = (".headwork/", "~/.dbhq/headwork", ".dbhq/headwork")


def test_no_scripts_ship_in_the_skill():
    """headwork decides; the session acts. A script here is write access."""
    assert not (SKILL_DIR / "scripts").exists(), "headwork must not grow scripts"
    stray = [p for p in SKILL_DIR.rglob("*.py") if "tests" not in p.parts]
    assert not stray, f"executable code outside tests: {stray}"


def test_the_installers_create_no_state_directory():
    """The no-state rule erodes via a run log that looks harmless in a diff."""
    for installer in ("install.sh", "install-codex.sh"):
        text = (REPO / installer).read_text(encoding="utf-8")
        for path in STATE_PATHS:
            assert path not in text, f"{installer} references state path {path}"


def test_skill_md_promises_no_state(skill_lower):
    assert "never keeps state" in skill_lower
    assert "no log" in skill_lower


def test_skill_md_refuses_to_scan(skill_lower):
    assert "never scans for work" in skill_lower


def test_skill_md_refuses_to_edit(skill_lower):
    assert "never edits anything" in skill_lower


# --- House style -----------------------------------------------------------


def test_no_em_or_en_dashes():
    # Written as escapes rather than literals so this file does not fail its
    # own check. A literal en dash in the pattern is still an en dash.
    dashes = re.compile("[\u2013\u2014]")
    offenders = []
    for path in REPO.rglob("*"):
        if path.is_dir() or path.suffix not in {".md", ".py", ".json", ".sh"}:
            continue
        if any(part in {".git", "__pycache__", ".venv"} for part in path.parts):
            continue
        if dashes.search(path.read_text(encoding="utf-8")):
            offenders.append(str(path.relative_to(REPO)))
    assert not offenders, f"house style is a plain hyphen: {offenders}"
