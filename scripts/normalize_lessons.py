#!/usr/bin/env python3
"""Normalize all day lessons for consistent structure and learner paths."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

WEEK_TIMES = {
    1: ("4–6 hours", "2–4 hours", "1–3 hours"),
    2: ("5–7 hours", "3–5 hours", "2–3 hours"),
    3: ("5–7 hours", "3–5 hours", "2–4 hours"),
    4: ("4–6 hours", "3–4 hours", "2–3 hours"),
}

APPLY_BY_WEEK = {
    1: "Write one sentence in your own words explaining today's main idea.",
    2: "Add today's component to `projects/studyspark/` or update `projects/CAPSTONE.md`.",
    3: "Update the retrieval or memory section in `projects/CAPSTONE.md`.",
    4: "Add today's safety, eval, or deploy item to the capstone checklist.",
}


def week_for_day(day: int) -> int:
    if day <= 7:
        return 1
    if day <= 14:
        return 2
    if day <= 21:
        return 3
    return 4


def how_to_use_block(day: int) -> str:
    week = week_for_day(day)
    b, i, a = WEEK_TIMES[week]
    apply_extra = APPLY_BY_WEEK[week]
    return f"""## How to Use This Lesson

This lesson is designed for **all skill levels**. Pick one path and follow it consistently.

| Level | Suggested approach | Time |
| --- | --- | --- |
| **Beginner** | Read Introduction → Big Picture → Deep Theory → trace one code example → Easy exercises | {b} |
| **Intermediate** | Skim objectives → Visual Learning → Code Walkthrough → Medium/Hard exercises → Mini project | {i} |
| **Advanced** | Deep Theory tradeoffs → Hard/Challenge exercises → extend mini project → capstone slice | {a} |

### Apply Today
Complete at least one item before moving to the next day:
- [ ] Trace one code example in **Python or TypeScript** (one language is enough)
- [ ] Complete exercises for your level (see Exercises section)
- [ ] Update [`projects/CAPSTONE.md`](../../projects/CAPSTONE.md) with today's capstone item
- [ ] {apply_extra}

> **Stuck?** Re-read Big Picture, review Prerequisites, or see [SYLLABUS.md](../../SYLLABUS.md) for path guidance.

"""


CAPSTONE_BY_DAY: dict[int, str] = {
    1: """## Cumulative Capstone Update

Start your capstone tracker in [`projects/CAPSTONE.md`](../../projects/CAPSTONE.md).

Add today:
- one-paragraph **problem statement** for StudySpark
- **target user** (e.g., university student preparing for exams)
- three **success criteria** for the finished product

""",
    2: """## Cumulative Capstone Update

Add to [`projects/CAPSTONE.md`](../../projects/CAPSTONE.md):
- a short note on **when to trust** vs verify LLM output in StudySpark
- two example user questions the assistant must handle well

""",
    3: """## Cumulative Capstone Update

Add to [`projects/CAPSTONE.md`](../../projects/CAPSTONE.md):
- **token budget** guidelines for StudySpark prompts (max context per request)
- chunk size notes for future note ingestion (preview of Day 15)

""",
    4: """## Cumulative Capstone Update

Add to [`projects/CAPSTONE.md`](../../projects/CAPSTONE.md):
- three **reusable prompt templates** (summarize, quiz, explain)
- one test prompt with expected output shape for each template

""",
    5: """## Cumulative Capstone Update

Add to [`projects/CAPSTONE.md`](../../projects/CAPSTONE.md):
- advanced patterns in use: chain-of-thought, few-shot, or role prompts
- failure cases and how prompts should recover

""",
    6: """## Cumulative Capstone Update

Add to [`projects/CAPSTONE.md`](../../projects/CAPSTONE.md):
- paper schema for **LLM request/response** (model, messages, settings)
- error-handling rules (timeout, empty response, rate limit)

""",
    7: """## Cumulative Capstone Update

Add to [`projects/CAPSTONE.md`](../../projects/CAPSTONE.md):
- **Prompt Helper spec** (input, clarifying questions, output format)
- link Prompt Helper as the front door before StudySpark calls the model

""",
    17: """## Cumulative Capstone Update

Add to [`projects/studyspark/`](../../projects/studyspark/) and [`projects/CAPSTONE.md`](../../projects/CAPSTONE.md):
- RAG pipeline module outline (`retrieve` → `build_prompt` → `generate`)
- citation format (source day, section, chunk id)
- fallback message when retrieval returns low scores

""",
    18: """## Cumulative Capstone Update

Add to [`projects/CAPSTONE.md`](../../projects/CAPSTONE.md):
- hybrid search strategy (when keyword vs vector wins)
- metadata filters for note subjects or course modules

""",
    19: """## Cumulative Capstone Update

Add to [`projects/CAPSTONE.md`](../../projects/CAPSTONE.md):
- session memory policy: what to remember vs forget each turn
- max messages or tokens kept in session context

""",
    20: """## Cumulative Capstone Update

Add to [`projects/CAPSTONE.md`](../../projects/CAPSTONE.md):
- long-term memory store design (preferences, goals, past topics)
- rule: memory complements RAG but does not replace citations

""",
    30: """## Cumulative Capstone Update

**Final consolidation.** Merge all daily updates into one deliverable:

1. Complete every checkbox in [`projects/CAPSTONE.md`](../../projects/CAPSTONE.md)
2. Ensure [`projects/studyspark/`](../../projects/studyspark/) runs end-to-end
3. Record a 3-minute demo script (problem → flow → evaluation → limits)
4. List three improvements you would ship in v2

""",
}


def insert_how_to_use(content: str, day: int) -> str:
    if "## How to Use This Lesson" in content:
        return content
    marker = "## Prerequisites"
    block = how_to_use_block(day)
    if marker in content:
        return content.replace(marker, block + marker, 1)
    marker2 = "## Big Picture"
    if marker2 in content:
        return content.replace(marker2, block + marker2, 1)
    return content


def normalize_headings(content: str) -> str:
    content = content.replace("## Additional Resources", "## Further Reading")
    content = re.sub(r"^## Capstone Update$", "## Cumulative Capstone Update", content, flags=re.M)
    return content


def insert_capstone(content: str, day: int) -> str:
    if day not in CAPSTONE_BY_DAY:
        return content
    if "## Cumulative Capstone Update" in content:
        return content
    block = CAPSTONE_BY_DAY[day]
    if "## Summary" in content:
        return content.replace("## Summary", block + "## Summary", 1)
    return content + "\n" + block


def process_file(path: Path, day: int) -> bool:
    original = path.read_text(encoding="utf-8")
    updated = original
    updated = normalize_headings(updated)
    updated = insert_how_to_use(updated, day)
    updated = insert_capstone(updated, day)
    if updated != original:
        path.write_text(updated, encoding="utf-8")
        return True
    return False


def main() -> None:
    changed = 0
    for day in range(1, 31):
        folder = ROOT / f"day_{day:02d}"
        files = list(folder.glob("*.md"))
        if not files:
            print(f"day_{day:02d}: MISSING")
            continue
        if process_file(files[0], day):
            changed += 1
            print(f"day_{day:02d}: updated")
        else:
            print(f"day_{day:02d}: no change")
    print(f"Done. {changed} files modified.")


if __name__ == "__main__":
    main()
