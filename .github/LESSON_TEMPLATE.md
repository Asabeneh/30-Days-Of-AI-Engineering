# Lesson Template

Copy this structure when creating or expanding any day. All 30 lessons should match this skeleton for consistency.

## Required Header

```markdown
# Day N - Topic Title

[Previous: Day N-1 - Title](../day_XX/file.md) | [Next: Day N+1 - Title](../day_XX/file.md)

## Introduction
(Why today exists; connect to yesterday and tomorrow)

![Visual diagram](../images/week_X_name.svg)

## Learning Objectives
(6–10 measurable outcomes)

## How to Use This Lesson

| Level | Suggested approach | Time |
| --- | --- | --- |
| **Beginner** | Introduction → Big Picture → Deep Theory → one code example → Easy exercises | X–Y hours |
| **Intermediate** | Visual Learning → Code Walkthrough → Medium/Hard exercises → Mini project | X–Y hours |
| **Advanced** | Tradeoffs + alternatives → Challenge exercises → capstone code | X–Y hours |

### Apply Today
- [ ] Trace one code example (Python or TypeScript)
- [ ] Complete exercises for your level
- [ ] Update `projects/CAPSTONE.md`
- [ ] (Day-specific apply item)

## Prerequisites
(Link prior days; say what to review if stuck)
```

## Required Body Sections

1. **Big Picture** — one mental model + diagram
2. **Deep Theory** — definition, why, problem, mechanics, advantages, limitations, alternatives
3. **Historical Background** — when topic warrants it
4. **Visual Learning** — 8+ Mermaid diagrams for expanded days
5. **Code Walkthrough** — 10+ examples with line explanations (Python + TypeScript)
6. **Practical Examples** — Beginner, Intermediate, Advanced, Production, Company
7. **Best Practices**
8. **Common Mistakes** (+ debugging strategy)
9. **Performance** (when relevant)
10. **Security** (when relevant)
11. **Exercises** — Easy (5), Medium (5), Hard (5), Challenge (5), Reflection (5+)
12. **Quizzes** — with answers (expanded days)
13. **Interview Questions** (expanded days)
14. **Mini Project** — goal, features, folder structure, steps, what you learn
15. **Cumulative Capstone Update** — bullet list tied to `projects/CAPSTONE.md`
16. **Summary**
17. **Further Reading** — primary sources only

## Depth Targets

| Metric | Target |
| --- | --- |
| Words | 5,000–7,000 |
| Diagrams | 8–15 |
| Code examples | 10–20 |
| Tables | 5–10 |
| Exercises | 25–40 |

## Learner-Level Rules

- **Never assume** prior AI knowledge in Week 1.
- **Always explain WHY** before HOW.
- **One apply action** per day minimum (code, spec, or capstone checkbox).
- **Beginner path** must be completable without API keys where possible.
- **Same section order** every day so learners build habit.

## Naming Conventions

- Use `## Cumulative Capstone Update` (not "Capstone Update")
- Use `## Further Reading` (not "Additional Resources")
- Capstone product name: **StudySpark**
- Week 3 knowledge feature: extends StudySpark with RAG over notes/curriculum
