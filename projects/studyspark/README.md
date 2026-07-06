# StudySpark

Starter codebase for the 30 Days of AI Engineering capstone. Grows one layer per day — see [CAPSTONE.md](../CAPSTONE.md).

## Quick Start

```bash
# From repo root
python -m venv .venv
source .venv/bin/activate   # or .venv\Scripts\activate on Windows
pip install -r projects/studyspark/requirements.txt
cp projects/studyspark/.env.example .env   # add keys when ready
python projects/studyspark/scripts/check_setup.py
```

## Learning Paths

| Level | What to do here |
| --- | --- |
| Beginner | Read files in order; run `check_setup.py`; add Day 8 client when ready |
| Intermediate | Implement each day's capstone slice in `app/` |
| Advanced | Add tests, logging, and provider abstraction early |

## Structure

```text
studyspark/
├── app/
│   ├── __init__.py
│   ├── config.py          # env-based settings
│   └── clients/
│       ├── __init__.py
│       └── mock_llm.py    # works without API keys
├── scripts/
│   └── check_setup.py
├── tests/
│   └── test_mock_llm.py
├── .env.example
├── requirements.txt
└── README.md
```

## No API Key?

Use `MockLLMClient` in `app/clients/mock_llm.py` for Week 1–2 exercises.

## Next Steps by Day

| Day | Add to project |
| --- | --- |
| 8 | `app/clients/openai_client.py` |
| 9 | `app/clients/provider.py` adapters |
| 10 | `app/schemas/` |
| 11–12 | `app/tools/` |
| 13 | streaming route |
| 15+ | `app/rag/`, `app/memory/` |

See [CAPSTONE.md](../CAPSTONE.md) for the full checklist.
