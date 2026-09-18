"""Structural tests for the headwork skill.

headwork is instructions, not a program, so these tests assert that SKILL.md
states its rules and that the two harness paths carry the same parts. They
cannot test how a model behaves after reading the file, and they do not pretend
to. See AGENTS.md, which states that limit rather than hiding it.

The rules under test are the four in AGENTS.md:

  1. Never ask what you can find out
  2. One question per message, then stop
  3. Every option carries a justification, and every alternative its cost
  4. The two harness paths carry the same parts

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


def test_option_bounds_appear_in_both_paths(skill_text):
    box = section(skill_text, "The question box - Claude Code")
    fallback = section(skill_text, "The text fallback - Codex and any other harness")
    for path_name, body in (("box", box), ("fallback", fallback)):
        assert "two to four options" in body, f"{path_name} lost the option bound"


# --- Rule 4: the two harness paths carry the same parts -------------------

# The five parts, and a marker that must appear in each harness section. A new
# harness section added per CONTRIBUTING.md should be added to HARNESS_SECTIONS.
FIVE_PARTS = {
    "what you checked": "what you checked",
    "bite-sized explainer": "bite-sized",
    "two to four options": "two to four options",
    "justification per option": "justification",
    "named recommendation": "recommend",
}

HARNESS_SECTIONS = [
    "The question box - Claude Code",
    "The text fallback - Codex and any other harness",
]


def test_the_five_parts_are_stated_once_up_front(skill_text):
    parts = section(skill_text, "The five parts")
    for part, marker in FIVE_PARTS.items():
        assert marker in parts, f"'The five parts' no longer names {part}"


@pytest.mark.parametrize("heading", HARNESS_SECTIONS)
def test_both_paths_carry_the_same_parts(skill_text, heading):
    """The Codex path is the one at risk - nobody develops this in Codex."""
    body = section(skill_text, heading)
    missing = [part for part, marker in FIVE_PARTS.items() if marker not in body]
    assert not missing, f"{heading!r} is missing: {', '.join(missing)}"


# --- Refusal is a correct result ------------------------------------------


def test_all_three_refusal_cases_survive(skill_text):
    body = section(skill_text, "Refusal is a correct result")
    assert "already decided" in body
    assert "only one option is real" in body
    assert "nothing live to decide" in body


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
