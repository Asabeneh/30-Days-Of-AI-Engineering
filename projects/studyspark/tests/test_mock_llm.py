import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.clients.mock_llm import MockLLMClient


def test_mock_returns_text() -> None:
    client = MockLLMClient()
    response = client.chat([{"role": "user", "content": "What is a vector?"}])
    assert "Mock StudySpark" in response.text
    assert response.prompt_tokens > 0


if __name__ == "__main__":
    test_mock_returns_text()
    print("test_mock_returns_text: passed")
