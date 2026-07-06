"""Verify Python environment and repo layout."""

import sys
from pathlib import Path


def main() -> None:
    print(f"Python: {sys.version.split()[0]}")

    for package in ("pydantic", "dotenv"):
        try:
            __import__(package)
            print(f"  {package}: OK")
        except ImportError:
            print(f"  {package}: MISSING — run pip install -r requirements.txt")

    root = Path(__file__).resolve().parents[1]
    capstone = root.parent / "CAPSTONE.md"
    print(f"Capstone tracker: {'OK' if capstone.exists() else 'MISSING'}")

    sys.path.insert(0, str(root))
    try:
        from app.clients.mock_llm import MockLLMClient

        client = MockLLMClient()
        result = client.chat([{"role": "user", "content": "setup check"}])
        print(f"Mock LLM: OK ({result.model})")
    except Exception as exc:
        print(f"Mock LLM: FAILED — {exc}")

    print("Setup check complete.")


if __name__ == "__main__":
    main()
