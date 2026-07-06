# Projects

Hands-on work for the course lives here. You build **one product** across 30 days — not 30 separate demos.

## Main Project: StudySpark

| Resource | Purpose |
| --- | --- |
| [CAPSTONE.md](CAPSTONE.md) | Daily checklist — update after every lesson |
| [studyspark/](studyspark/) | Runnable Python starter (mock LLM works without API keys) |

```bash
cd projects/studyspark
pip install -r requirements.txt
python scripts/check_setup.py
```

## Suggested Larger Builds

These extend the capstone rather than replacing it:

- **Prompt Helper** (Day 7) — spec in your notes or `studyspark/docs/`
- **StudySpark shell** (Day 14) — chat + streaming + tools
- **Knowledge assistant** (Day 21) — RAG over course notes
- **Final capstone** (Day 30) — deploy and demo StudySpark

Each build should include: problem statement, user, input/output design, evaluation checklist, and deployment notes.

## Learning Path

| Level | Focus in this folder |
| --- | --- |
| Beginner | Run `check_setup.py`; update CAPSTONE.md only until Day 8 |
| Intermediate | Implement each day's capstone slice in `studyspark/app/` |
| Advanced | Add tests, logging, and CI from Week 2 onward |

See [SYLLABUS.md](../SYLLABUS.md) for full guidance.
