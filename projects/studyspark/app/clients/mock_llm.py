"""Mock LLM client for learners without API keys."""

from dataclasses import dataclass


@dataclass
class LLMResponse:
    text: str
    model: str
    prompt_tokens: int
    completion_tokens: int


class MockLLMClient:
    """Returns predictable text for exercises and local development."""

    def __init__(self, model: str = "mock-studyspark-v1") -> None:
        self.model = model

    def chat(self, messages: list[dict[str, str]], max_tokens: int = 500) -> LLMResponse:
        user_text = next(
            (m["content"] for m in reversed(messages) if m.get("role") == "user"),
            "",
        )
        preview = user_text[:80] + ("..." if len(user_text) > 80 else "")
        answer = (
            f"[Mock StudySpark] You asked about: {preview}\n\n"
            "Replace MockLLMClient with a real provider after Day 8."
        )
        return LLMResponse(
            text=answer,
            model=self.model,
            prompt_tokens=max(1, len(user_text.split())),
            completion_tokens=max(1, len(answer.split())),
        )


def demo() -> None:
    client = MockLLMClient()
    response = client.chat(
        [
            {"role": "system", "content": "You are StudySpark, a study coach."},
            {"role": "user", "content": "Explain recursion in one paragraph."},
        ]
    )
    print(response.text)
    print(f"Tokens: {response.prompt_tokens} in / {response.completion_tokens} out")


if __name__ == "__main__":
    demo()
