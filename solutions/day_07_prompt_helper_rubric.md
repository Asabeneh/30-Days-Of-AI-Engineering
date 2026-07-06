# Day 7 — Prompt Helper Rubric

Use this rubric to check your Prompt Helper spec before moving to Day 8.

## Minimum Pass (Beginner)

| Criterion | Pass? |
| --- | --- |
| Problem statement: who is the user and what vague input do they provide? | ☐ |
| At least 3 clarifying questions listed | ☐ |
| Output format defined (fields or template) | ☐ |
| One example: vague input → improved prompt | ☐ |
| Fallback when user gives one-word answers | ☐ |

## Standard (Intermediate)

| Criterion | Pass? |
| --- | --- |
| Acceptance criteria table (has audience, goal, format, etc.) | ☐ |
| At least 5 test cases with messy real-world input | ☐ |
| Tone/audience variants documented | ☐ |
| Spec could be handed to another developer | ☐ |

## Stretch (Advanced)

| Criterion | Pass? |
| --- | --- |
| Evaluation plan: how to know the helper improves prompts | ☐ |
| Edge cases: empty input, offensive input, already-clear input | ☐ |
| Link to StudySpark: helper runs before LLM call in capstone | ☐ |

## Sample Improved Prompt (Reference)

**Vague input:** "write me something about marketing"

**Clarifying answers:** small business owners, teach basics, bullet points

**Improved prompt:**
"Write a beginner-friendly marketing overview for small business owners. Goal: teach marketing basics. Format: 5 bullet points under 120 words total. Tone: practical, no jargon."
