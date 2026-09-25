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

The shape of a round - the block, the options, one question - is checked by
roundcheck.py, over the block in SKILL.md, every worked example and every saved
transcript. See test_roundcheck.py.
"""

import pathlib
import re

import pytest

REPO = pathlib.Path(__file__).resolve().parents[1]
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


def description(skill_text):
    """The frontmatter description, lower case, whitespace collapsed.

    The description is a folded YAML block, so a phrase can land either side of
    a line break and still be one phrase.
    """
    match = re.match(r"^---\n(.*?)\n---", skill_text, re.S)
    return flat(match.group(1).lower())


def test_description_names_the_trigger_phrases(skill_text):
    """The description is the auto-trigger. If the phrases go, it never fires."""
    for phrase in ("stuck between", "unblock", "decide"):
        assert phrase in description(skill_text), f"description no longer triggers on {phrase!r}"


def test_description_does_not_claim_other_skills_triggers(skill_text):
    """"what's next" asks for a backlog read, which headwork never does, and a
    bare "stuck" is claimed by debugging and board skills. Stuck is only ours
    when it is stuck between choices."""
    text = description(skill_text)
    assert "what's next" not in text
    assert "what comes next" not in text
    for match in re.finditer(r"stuck\b(.{0,12})", text):
        assert match.group(1).lstrip().startswith(("between", "on which")), (
            f"'stuck' used outside decision phrasing: {match.group(0)!r}"
        )


@pytest.mark.parametrize("path", ["README.md", "install.sh"])
def test_nothing_says_it_fires_on_what_comes_next(path):
    text = flat((REPO / path).read_text(encoding="utf-8").lower())
    assert "what comes next" not in text, f"{path} still says it fires on what comes next"


def test_when_not_to_use_routes_elsewhere(skill_text):
    body = section(skill_text, "When not to use")
    for skill in (
        "superpowers:brainstorming",
        "mattpocock/skills",
        "groupwork",
        "deskwork",
        "life-manager",
        "systematic-debugging",
        "paseo-committee",
    ):
        assert skill in body, f"'When not to use' no longer names {skill}"


# --- Rule 1: never ask what you can find out -----------------------------


def test_look_first_rule_is_stated(skill_lower):
    assert "never ask what you can find out" in skill_lower


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


# --- Rule 4: both ways of asking carry the same parts ----------------------

# Each way of asking sends the block, so each carries all six parts. A new
# way of asking added per CONTRIBUTING.md goes in this list.
HARNESS_SECTIONS = [
    "With a question tool",
    "Without a question tool",
]


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
    body = flat(section(skill_text, "Taking the answer"))
    assert "not a choice" in body
    assert "still ask one" in body


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


def test_the_session_acts_on_the_answer_before_the_next_round(skill_text):
    """Read literally, "hand the answer back" and "never edits" could mean the
    agent never acts, or asks the next question before doing the work."""
    body = section(skill_text, "A round, exactly")
    step = re.search(r"^6\. (.*?)(?=^\S|\Z)", body, re.M | re.S)
    assert step, "'A round, exactly' has no step 6"
    step = flat(step.group(1))
    assert "carry out the chosen option" in step
    assert "before any next round" in step
    assert "only if another decision blocks" in step


def test_the_session_has_a_done_condition(skill_lower):
    """Uncapped is not endless: an agent can always find one more question."""
    text = flat(skill_lower)
    assert "done when the work can take its next action without another decision" in text
    assert "one line per decision" in text
    assert "recap lives in the conversation, not in a file" in text


def test_every_kind_of_answer_is_covered(skill_text):
    body = flat(section(skill_text, "Taking the answer"))
    for case in ("against the recommendation", '"just pick"', '"other" answer', "no answer"):
        assert case in body, f"'Taking the answer' no longer covers {case}"
    assert "do not argue it again" in body


def test_a_worked_example_runs_several_rounds_and_ends_in_a_recap():
    text = (SKILL_DIR / "references" / "worked-examples.md").read_text(encoding="utf-8")
    sessions = [s for s in re.split(r"^## ", text, flags=re.M) if "Decided:" in s]
    assert sessions, "no worked example ends with a recap"
    session = sessions[0]
    assert len(re.findall(r"^> RECOMMENDED: ", session, re.M)) >= 2, "the recap example is one round"
    assert re.search(r"^> .*\b(left|remain)", session, re.M), "no line says how many remain"


def test_the_cap_is_per_message_not_per_session(skill_lower):
    assert "questions per message" in skill_lower


# --- The three things headwork must never grow ----------------------------

STATE_PATHS = (".headwork/", "~/.dbhq/headwork", ".dbhq/headwork")


def test_the_skill_is_markdown_only():
    """headwork decides; the session acts. A script here is write access, and
    the installers copy or link this whole directory, so anything in it ships."""
    stray = [
        str(p.relative_to(REPO))
        for p in SKILL_DIR.rglob("*")
        if p.is_file() and p.suffix != ".md" and "__pycache__" not in p.parts
    ]
    assert not stray, f"the skill directory must hold markdown only: {stray}"


def repo_files(*suffixes):
    """Every file in the repository with one of these suffixes."""
    skip = {".git", "__pycache__", ".venv", ".pytest_cache", ".ruff_cache"}
    return [
        p
        for p in sorted(REPO.rglob("*"))
        if p.is_file() and p.suffix in suffixes and not skip.intersection(p.parts)
    ]


def test_security_md_names_everything_that_runs():
    """SECURITY.md once said no scripts ship, while two installers and a test
    suite did. Every script has to be named, by file or by its folder."""
    text = (REPO / "SECURITY.md").read_text(encoding="utf-8")
    for path in repo_files(".sh", ".py"):
        rel = path.relative_to(REPO)
        named = f"`{rel.name}`" in text or f"`{rel.parts[0]}/`" in text
        assert named, f"SECURITY.md does not say that {rel} ships"


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


# --- The files agree with each other ----------------------------------------

NUMBER_WORDS = ("one", "two", "three", "four", "five", "six", "seven", "eight", "nine")


def test_every_count_of_the_parts_is_right(skill_text):
    """install-codex.sh kept the old count after a sixth part was added."""
    body = section(skill_text, "The six parts")
    count = len(re.findall(r"^\d+\. ", body.split("```")[0], re.M))
    for path in repo_files(".md", ".sh", ".py", ".json"):
        text = flat(path.read_text(encoding="utf-8").lower())
        for word in re.findall(r"\b(" + "|".join(NUMBER_WORDS) + r") parts\b", text):
            assert NUMBER_WORDS.index(word) + 1 == count, (
                f"{path.relative_to(REPO)} says {word} parts; SKILL.md lists {count}"
            )


def test_agents_md_names_the_right_refusal_case(skill_text):
    """AGENTS.md gave the consequence rule the wrong number among the refusal
    cases. It is the third, and a wrong number sends a reader to another one."""
    agents = flat((REPO / "AGENTS.md").read_text(encoding="utf-8").lower())
    said = re.search(r"this is the (\w+) refusal case", agents)
    assert said, "AGENTS.md no longer points rule 5 at its refusal case"
    ordinals = ("first", "second", "third", "fourth", "fifth", "sixth")
    cases = re.findall(r"^- \*\*(.+?)\*\*", section(skill_text, "Refusal is a correct result"), re.M)
    actual = next(i for i, case in enumerate(cases) if "not consequential enough" in case)
    assert said.group(1) == ordinals[actual], (
        f"AGENTS.md says {said.group(1)}; it is the {ordinals[actual]} case in SKILL.md"
    )


def test_only_the_alternatives_carry_a_cost(skill_text):
    """AGENTS.md said the recommendation names its cost too. SKILL.md and the
    worked examples put a COST on the alternatives only."""
    block = fenced_blocks(section(skill_text, "The six parts"))[0]
    recommended = re.search(r"^recommended: .*$", block, re.M).group(0)
    assert "cost:" not in recommended, "the block puts a COST on the recommendation"
    agents = (REPO / "AGENTS.md").read_text(encoding="utf-8")
    rule = re.search(r"^### 3\. (.*?)(?=^### )", agents, re.M | re.S)
    assert rule, "AGENTS.md has no rule 3"
    rule = flat(rule.group(1).lower())
    assert "no `cost:` line" in rule, "AGENTS.md rule 3 no longer says the recommendation has no cost"
    assert "names what it costs" not in rule


# --- The comparison with grill-me -----------------------------------------

GRILL_ME = "https://github.com/mattpocock/skills"

# Claims that were true of a copy, or never true, and must not come back.
STALE_COMPARISON = (
    "choosing between them is your job",
    "got there first",
    "does not contain the word",
    "contains the word \"recommend\"",
    "grill-me asks one question at a time",
)

# The five differences, as each file states them.
FIVE_DIFFERENCES = (
    "overturned if:",
    "cost:",
    "one question per message",
    "cheap",
    "blocking",
)


@pytest.mark.parametrize("path", ["README.md", "AGENTS.md"])
def test_the_grill_me_comparison_is_against_the_real_one(path):
    """grill-me lives in mattpocock/skills, and it now recommends an answer."""
    text = flat((REPO / path).read_text(encoding="utf-8")).lower()
    assert GRILL_ME in text, f"{path} does not link mattpocock/skills as grill-me"
    for claim in STALE_COMPARISON:
        assert claim not in text, f"{path} still says {claim!r}"
    for difference in FIVE_DIFFERENCES:
        assert difference in text, f"{path} no longer names {difference!r}"


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
