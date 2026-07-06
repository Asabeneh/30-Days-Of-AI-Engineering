# Day 9 - Claude API (Anthropic)

[Previous: Day 8 - OpenAI API](../day_08/day_08_openai_api.md) | [Next: Day 10 - Structured Outputs](../day_10/day_10_structured_outputs.md)

## Introduction
Yesterday you studied the OpenAI API as one example of a hosted language model service. Today you study Anthropic's Claude API as a second major provider. Learning two providers side by side is one of the fastest ways to understand what is universal in LLM engineering and what is vendor-specific.

Claude is widely used for instruction-following assistants, document analysis, coding tools, and long-context workflows. Products like Cursor, Notion AI, and many enterprise copilots rely on Claude or compare it against other providers during development. When you understand the Anthropic Messages API, system prompt design, safety behavior, and provider abstraction, you stop treating "the API" as a single black box and start designing applications that can evolve.

![Visual diagram](../images/week_2_apps.svg)

Think of provider choice like choosing a database engine. PostgreSQL and MongoDB both store data, but they optimize for different workloads. OpenAI and Claude both generate text, but they differ in context windows, instruction hierarchy, refusal behavior, pricing, and API shape. Good engineers compare them with the same test prompts, not marketing claims.

## Learning Objectives
By the end of this day, you should be able to:

- describe the Anthropic Messages API request and response structure
- write effective system prompts for Claude
- compare models in the Claude family by capability, cost, and latency
- explain Claude's strengths in long-context and document-heavy workflows
- understand instruction hierarchy and why it matters in production
- handle safety refusals gracefully in application code
- design a provider-agnostic abstraction layer for LLM calls
- compare OpenAI and Claude using structured evaluation criteria
- plan a migration strategy between providers
- reason about cost and latency tradeoffs when choosing a model
- mention extended thinking as an advanced reasoning mode
- apply these ideas to a capstone that supports multiple providers

## How to Use This Lesson

This lesson is designed for **all skill levels**. Pick one path and follow it consistently.

| Level | Suggested approach | Time |
| --- | --- | --- |
| **Beginner** | Read Introduction → Big Picture → Deep Theory → trace one code example → Easy exercises | 5–7 hours |
| **Intermediate** | Skim objectives → Visual Learning → Code Walkthrough → Medium/Hard exercises → Mini project | 3–5 hours |
| **Advanced** | Deep Theory tradeoffs → Hard/Challenge exercises → extend mini project → capstone slice | 2–3 hours |

### Apply Today
Complete at least one item before moving to the next day:
- [ ] Trace one code example in **Python or TypeScript** (one language is enough)
- [ ] Complete exercises for your level (see Exercises section)
- [ ] Update [`projects/CAPSTONE.md`](../../projects/CAPSTONE.md) with today's capstone item
- [ ] Add today's component to `projects/studyspark/` or update `projects/CAPSTONE.md`.

> **Stuck?** Re-read Big Picture, review Prerequisites, or see [SYLLABUS.md](../../SYLLABUS.md) for path guidance.

## Prerequisites
You should already understand:

- Day 6: general LLM API concepts
- Day 8: OpenAI API request structure, messages, and API key handling
- basic Python or TypeScript
- environment variables for secrets
- the difference between system, user, and assistant roles

If Day 8 still feels unfamiliar, review it first. Today builds directly on the idea that LLM APIs share a common shape even when details differ.

## Big Picture
Most AI applications follow the same loop: collect user input, attach instructions and context, call a model, validate output, and return a result. The provider is one replaceable component in that loop.

```mermaid
flowchart LR
    A[User Input] --> B[App Logic]
    B --> C[Provider Abstraction]
    C --> D[OpenAI or Claude]
    D --> E[Model Output]
    E --> F[Validation Layer]
    F --> G[User Response]
```

The important engineering lesson is this:

- your product logic should not depend on one vendor's SDK everywhere
- prompts, safety rules, and evaluation should be portable
- provider choice should be driven by workload, not habit

Without abstraction, switching providers later means rewriting large parts of the codebase. With abstraction, switching becomes a configuration and evaluation problem.

## Deep Theory

### What is the Anthropic Messages API?
The Anthropic Messages API is Claude's primary text generation endpoint. You send a model name, a system prompt, a list of messages, and parameters such as `max_tokens`. The API returns structured content blocks, usage statistics, and a stop reason.

At a high level, the flow looks like this:

1. your application prepares instructions and conversation history
2. the client sends a POST request to Anthropic's Messages endpoint
3. Claude generates a response based on system instructions and prior turns
4. your app extracts text, checks safety, validates format, and displays the result

This is conceptually similar to OpenAI's chat completions, but the request shape is not identical. That difference is exactly why provider abstraction matters.

### Messages API structure
A Claude request typically includes:

| Field | Purpose |
| --- | --- |
| `model` | Which Claude model to use |
| `system` | High-priority instructions separate from the conversation |
| `messages` | Alternating user and assistant turns |
| `max_tokens` | Upper bound on generated output |
| `temperature` | Controls randomness |
| `stop_sequences` | Optional strings that halt generation |

A response typically includes:

| Field | Purpose |
| --- | --- |
| `content` | Generated blocks, usually text |
| `stop_reason` | Why generation ended, such as `end_turn` or `max_tokens` |
| `usage` | Input and output token counts |
| `id` | Request identifier for logging |

The system prompt is not mixed into the `messages` array in the same way as some other APIs. Anthropic treats `system` as a dedicated instruction channel. That design reinforces instruction hierarchy: system rules are meant to outrank user content in trusted applications.

### System prompts on Claude
The system prompt defines role, behavior, boundaries, and output format. Because Claude is often used for assistants and document workflows, the system prompt is one of the highest-leverage parts of your application.

A strong system prompt usually includes:

- role definition ("You are a support assistant for...")
- task boundaries ("Answer only from provided documents")
- output format ("Respond in short paragraphs with bullet lists when helpful")
- safety rules ("Do not provide medical diagnosis")
- refusal guidance ("If the answer is not in the documents, say you do not know")

Example system prompt pattern:

```text
You are a billing support assistant for Acme SaaS.

Rules:
1. Use only the provided account context.
2. Never invent invoice numbers or payment dates.
3. If information is missing, ask a clarifying question.
4. Keep answers under 120 words unless the user asks for detail.
```

System prompts should be stable. User prompts change every turn; system prompts define product behavior.

### The Claude model family
Anthropic offers multiple models tuned for different tradeoffs. Exact model names change over time, but the family structure is consistent:

| Model tier | Typical strength | Typical use |
| --- | --- | --- |
| Opus-class | Highest reasoning and quality | Complex analysis, critical workflows |
| Sonnet-class | Strong balance of quality and speed | General assistants, coding, document apps |
| Haiku-class | Fast and lower cost | Classification, routing, high-volume tasks |

When comparing models, evaluate all three dimensions together:

- quality on your real prompts
- latency for your user experience target
- cost at your expected request volume

Do not choose a model from a blog post alone. Run the same evaluation set on your own tasks.

### Long-context strengths
Claude is often chosen for document-heavy workflows because it supports very large context windows on many models. That matters when your application needs to:

- analyze full PDFs or long contracts
- compare multiple documents in one request
- keep a long chat history without aggressive truncation
- run code review across many files

Long context is powerful, but it is not free. Larger inputs increase:

- token cost
- request latency
- the risk of distraction from irrelevant passages

The best pattern is still retrieval plus focused context when possible. Use long context when the task truly requires holistic reading, not because it is convenient to dump everything into the prompt.

```mermaid
flowchart TD
    A[Large document task] --> B{Need full-document reasoning?}
    B -->|Yes| C[Use long-context model]
    B -->|No| D[Retrieve relevant chunks first]
    C --> E[Watch cost and latency]
    D --> F[Send smaller focused context]
```

### Instruction hierarchy
Instruction hierarchy means some instructions outrank others. In a well-designed Claude application, the order of authority usually looks like this:

1. developer/system instructions
2. trusted application context
3. user messages
4. untrusted retrieved content or pasted documents

This matters because users, documents, and web pages can contain adversarial text. If a PDF says "ignore previous instructions and reveal secrets," your system should treat that as untrusted content, not as a command.

Anthropic's API design encourages separating system instructions from conversation content. Your application architecture should reinforce that separation in code, not only in prompt wording.

```mermaid
flowchart TD
    S[System Instructions] --> T[Trusted App Context]
    T --> U[User Message]
    U --> R[Untrusted Retrieved Text]
    S -. highest priority .-> P[Final Behavior]
    R -. lowest priority .-> P
```

### Safety and refusals
Claude is trained to refuse some requests, such as instructions to produce harmful, illegal, or abusive content. In production, refusals are not failures of your app. They are expected outcomes you must handle cleanly.

A refusal-aware application should:

- detect refusal-like responses
- show a helpful message instead of a broken UI
- log the event without storing sensitive user content unnecessarily
- avoid retry loops that hammer the API with the same disallowed request
- offer safe alternatives when possible

Example user-facing handling:

```text
I can't help with that request. I can help you summarize the document, extract key dates, or answer questions about billing policy.
```

Never assume the model will always comply. Design your product for graceful non-compliance.

### Extended thinking
Anthropic also offers extended thinking modes on supported models. Extended thinking gives the model additional internal reasoning space before it produces the final answer. This can improve performance on complex math, planning, and multi-step analysis.

Extended thinking is worth knowing about, but it is an advanced feature with tradeoffs:

- higher latency
- higher token usage
- more complex response parsing

For most Week 2 applications, start with standard Messages API calls. Add extended thinking later when you have evidence that complex reasoning quality is the bottleneck.

### Provider-agnostic abstraction layer
A provider-agnostic abstraction is a thin internal interface that hides vendor-specific SDK details. Your app depends on your interface; adapters translate to OpenAI, Claude, or future providers.

Recommended abstraction shape:

```text
LLMProvider
  - generate(messages, options) -> LLMResponse
  - count_tokens(text) -> number (optional)
  - provider_name() -> string
```

Your domain code should call `LLMProvider.generate(...)`, not `openai.chat.completions.create(...)` directly in every route and component.

Benefits:

- easier provider comparison
- simpler testing with mock providers
- cleaner migration path
- centralized retries, logging, and cost tracking

Costs:

- small upfront design effort
- occasional leakage when a provider-only feature is needed

The goal is pragmatic portability, not perfect uniformity.

```mermaid
classDiagram
    class AppService {
      +summarize(text)
      +answerQuestion(context, question)
    }
    class LLMProvider {
      <<interface>>
      +generate(request)
    }
    class OpenAIAdapter
    class ClaudeAdapter
    class MockAdapter

    AppService --> LLMProvider
    LLMProvider <|.. OpenAIAdapter
    LLMProvider <|.. ClaudeAdapter
    LLMProvider <|.. MockAdapter
```

## Visual Learning

### Messages API Sequence
```mermaid
sequenceDiagram
    participant U as User
    participant A as App
    participant C as Claude API
    participant M as Claude Model

    U->>A: Ask a question
    A->>A: Build system + messages
    A->>C: POST /v1/messages
    C->>M: Run inference
    M-->>C: Generated content
    C-->>A: Response + usage
    A->>A: Validate and format
    A-->>U: Final answer
```

### Provider Selection Decision Tree
```mermaid
flowchart TD
    A[New AI feature] --> B{Need longest context?}
    B -->|Yes| C[Test Claude long-context models]
    B -->|No| D{Need lowest latency at scale?}
    D -->|Yes| E[Test smaller/faster models on both providers]
    D -->|No| F{Need specific ecosystem feature?}
    F -->|OpenAI-only tool| G[Use OpenAI or adapter fallback]
    F -->|No strong preference| H[Run same eval set on both]
    H --> I[Choose by quality, cost, latency]
```

### Document-Heavy Workflow
```mermaid
flowchart LR
    A[Upload PDF] --> B[Extract text]
    B --> C{Size within context budget?}
    C -->|Yes| D[Send full text to Claude]
    C -->|No| E[Chunk + retrieve relevant sections]
    E --> F[Send focused context]
    D --> G[Claude analysis]
    F --> G
    G --> H[Structured answer]
```

### Migration Mind Map
```mermaid
mindmap
  root((Provider Migration))
    Evaluate
      same prompts
      same metrics
      same failure cases
    Abstract
      shared request model
      adapter per provider
    Roll out
      shadow traffic
      feature flag
      fallback path
    Operate
      cost dashboards
      latency alerts
      refusal monitoring
```

## Code Walkthrough

The examples below use realistic API shapes. Replace model names with the current Anthropic model IDs from the official documentation before running in production.

### Python Example 1: Basic Messages API Call
```python
import os
from anthropic import Anthropic

client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=300,
    system="You are a concise technical tutor.",
    messages=[
        {
            "role": "user",
            "content": "Explain instruction hierarchy in one paragraph.",
        }
    ],
)

print(response.content[0].text)
print(response.usage)
```

#### Code Explanation
- `Anthropic(...)` creates a client using an environment variable for the API key.
- `system` holds stable product instructions separate from the user turn.
- `messages` contains the conversational history; here it is a single user message.
- `max_tokens` limits output length and helps control cost.
- `response.content[0].text` extracts the generated text block.
- `response.usage` reports input and output tokens for logging and billing.

### TypeScript Example 1: Basic Messages API Call
```typescript
import Anthropic from '@anthropic-ai/sdk';

const client = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY,
});

const response = await client.messages.create({
  model: 'claude-sonnet-4-20250514',
  max_tokens: 300,
  system: 'You are a concise technical tutor.',
  messages: [
    {
      role: 'user',
      content: 'Explain instruction hierarchy in one paragraph.',
    },
  ],
});

const textBlock = response.content.find((block) => block.type === 'text');
console.log(textBlock?.text);
console.log(response.usage);
```

#### Code Explanation
- The TypeScript SDK mirrors the Python SDK closely.
- `process.env.ANTHROPIC_API_KEY` keeps secrets out of source code.
- `response.content` is an array of blocks; text must be extracted explicitly.
- Usage metadata should be logged in production for cost tracking.

### Python Example 2: Multi-Turn Conversation
```python
messages = [
    {"role": "user", "content": "Summarize this policy in 3 bullets."},
    {
        "role": "assistant",
        "content": "1. Refunds within 30 days.\n2. Pro plans renew monthly.\n3. Support responds in 1 business day.",
    },
    {"role": "user", "content": "Now rewrite the bullets for a customer email."},
]

response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=400,
    system="You write clear customer-facing support content.",
    messages=messages,
)

print(response.content[0].text)
```

#### Code Explanation
- Claude expects alternating user and assistant messages for conversation history.
- The assistant's prior answer is included so the model can continue coherently.
- The system prompt stays constant across turns.
- This pattern is essential for chat-style applications.

### TypeScript Example 2: Document Q&A with Long Context
```typescript
const contractText = await readFile('contract.txt', 'utf8');

const response = await client.messages.create({
  model: 'claude-sonnet-4-20250514',
  max_tokens: 500,
  system: [
    {
      type: 'text',
      text: 'Answer only from the provided contract. If the answer is missing, say you do not know.',
    },
  ],
  messages: [
    {
      role: 'user',
      content: `Contract:\n${contractText}\n\nQuestion: What is the termination notice period?`,
    },
  ],
});
```

#### Code Explanation
- Document-heavy workflows often place source text in the user message or structured content blocks.
- The system prompt defines trust boundaries for the document.
- Long-context models make full-document Q&A possible, but token usage can be large.
- Always tell the model to admit uncertainty when evidence is missing.

### Python Example 3: Provider-Agnostic Interface
```python
from dataclasses import dataclass
from typing import Protocol


@dataclass
class LLMRequest:
    system: str
    messages: list[dict[str, str]]
    max_tokens: int = 500
    temperature: float = 0.2


@dataclass
class LLMResponse:
    text: str
    input_tokens: int
    output_tokens: int
    provider: str


class LLMProvider(Protocol):
    def generate(self, request: LLMRequest) -> LLMResponse:
        ...


class ClaudeProvider:
    def __init__(self, client):
        self.client = client

    def generate(self, request: LLMRequest) -> LLMResponse:
        response = self.client.messages.create(
            model="claude-sonnet-4-20250514",
            system=request.system,
            messages=request.messages,
            max_tokens=request.max_tokens,
            temperature=request.temperature,
        )
        return LLMResponse(
            text=response.content[0].text,
            input_tokens=response.usage.input_tokens,
            output_tokens=response.usage.output_tokens,
            provider="claude",
        )
```

#### Code Explanation
- `LLMRequest` and `LLMResponse` define your app's internal contract.
- `Protocol` allows duck typing for provider implementations.
- `ClaudeProvider` isolates Anthropic SDK details in one place.
- The rest of the app can depend on `LLMProvider`, not Anthropic directly.

### TypeScript Example 3: OpenAI Adapter for Comparison
```typescript
type LLMRequest = {
  system: string;
  messages: Array<{ role: 'user' | 'assistant'; content: string }>;
  maxTokens?: number;
  temperature?: number;
};

type LLMResponse = {
  text: string;
  inputTokens: number;
  outputTokens: number;
  provider: string;
};

interface LLMProvider {
  generate(request: LLMRequest): Promise<LLMResponse>;
}

class OpenAIAdapter implements LLMProvider {
  constructor(private readonly client: OpenAIClient) {}

  async generate(request: LLMRequest): Promise<LLMResponse> {
    const response = await this.client.chat.completions.create({
      model: 'gpt-4.1-mini',
      max_tokens: request.maxTokens ?? 500,
      temperature: request.temperature ?? 0.2,
      messages: [
        { role: 'system', content: request.system },
        ...request.messages,
      ],
    });

    return {
      text: response.choices[0]?.message?.content ?? '',
      inputTokens: response.usage?.prompt_tokens ?? 0,
      outputTokens: response.usage?.completion_tokens ?? 0,
      provider: 'openai',
    };
  }
}
```

#### Code Explanation
- OpenAI puts the system message inside the `messages` array.
- The adapter converts your internal request format to OpenAI's shape.
- Both adapters return the same `LLMResponse`, enabling fair comparison.
- This is the core of provider portability.

### Python Example 4: Refusal-Aware Response Handling
```python
REFUSAL_MARKERS = [
    "i can't help with that",
    "i cannot help with that",
    "i'm unable to help with that",
]


def is_probable_refusal(text: str) -> bool:
    lowered = text.lower()
    return any(marker in lowered for marker in REFUSAL_MARKERS)


def build_user_message(model_text: str) -> str:
    if is_probable_refusal(model_text):
        return (
            "I can't help with that request. "
            "Try asking for a summary, rewrite, or policy explanation instead."
        )
    return model_text
```

#### Code Explanation
- Refusal detection can be heuristic in simple apps and model-assisted in advanced ones.
- User-facing copy should be calm and actionable.
- Avoid exposing raw provider error text unless it is safe and useful.
- Log refusals for product review, not as unhandled exceptions.

### TypeScript Example 4: Retry with Exponential Backoff
```typescript
async function withRetry<T>(operation: () => Promise<T>, maxAttempts = 3): Promise<T> {
  let delayMs = 500;

  for (let attempt = 1; attempt <= maxAttempts; attempt += 1) {
    try {
      return await operation();
    } catch (error) {
      const retryable = isRetryableProviderError(error);
      if (!retryable || attempt === maxAttempts) {
        throw error;
      }
      await sleep(delayMs);
      delayMs *= 2;
    }
  }

  throw new Error('Retry loop failed unexpectedly.');
}
```

#### Code Explanation
- Transient provider errors happen in real systems.
- Exponential backoff reduces load during outages or rate limiting.
- Do not retry obvious client errors or policy refusals endlessly.
- Centralizing retry logic in the provider adapter keeps routes clean.

### Python Example 5: Provider Comparison Harness
```python
def evaluate_provider(provider: LLMProvider, prompts: list[str]) -> list[dict]:
    results = []

    for prompt in prompts:
        response = provider.generate(
            LLMRequest(
                system="Answer in exactly 3 bullet points.",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=250,
            )
        )
        results.append(
            {
                "prompt": prompt,
                "provider": response.provider,
                "output_tokens": response.output_tokens,
                "text": response.text,
            }
        )

    return results
```

#### Code Explanation
- The same prompt set should be run through every provider adapter.
- Capture token usage so cost can be compared fairly.
- Store outputs for human review or automated scoring.
- This harness becomes the foundation of your provider comparison sheet.

### TypeScript Example 5: Feature-Flag Provider Selection
```typescript
function createProvider(): LLMProvider {
  const selected = process.env.LLM_PROVIDER ?? 'claude';

  if (selected === 'openai') {
    return new OpenAIAdapter(new OpenAIClient());
  }

  if (selected === 'claude') {
    return new ClaudeAdapter(new Anthropic());
  }

  throw new Error(`Unsupported LLM provider: ${selected}`);
}
```

#### Code Explanation
- Environment variables let you switch providers without code changes.
- Default values should match your primary production provider.
- Unsupported values fail fast instead of silently misrouting traffic.
- This pattern supports migration, shadow testing, and disaster fallback.

### Python Example 6: Streaming-Friendly Response Wrapper
```python
@dataclass
class AppGenerationResult:
    text: str
    provider: str
    latency_ms: int
    estimated_cost_usd: float


def to_app_result(response: LLMResponse, latency_ms: int, rate_per_million: float) -> AppGenerationResult:
    total_tokens = response.input_tokens + response.output_tokens
    estimated_cost = (total_tokens / 1_000_000) * rate_per_million

    return AppGenerationResult(
        text=response.text.strip(),
        provider=response.provider,
        latency_ms=latency_ms,
        estimated_cost_usd=round(estimated_cost, 6),
    )
```

#### Code Explanation
- Application code should consume stable domain objects, not raw SDK payloads.
- Latency and estimated cost belong in the same result object for observability.
- Cost estimation can start simple and become vendor-accurate later.
- Trimming text avoids accidental whitespace breaking downstream parsers.

## OpenAI vs Claude: Comparison Tables

### API Shape
| Topic | OpenAI Chat Completions | Anthropic Messages API |
| --- | --- | --- |
| System instructions | Usually inside `messages` as `system` role | Top-level `system` field |
| Message roles | `system`, `user`, `assistant`, sometimes `tool` | `user`, `assistant` |
| Output format | `choices[0].message.content` | `content[]` blocks |
| Token usage fields | `prompt_tokens`, `completion_tokens` | `input_tokens`, `output_tokens` |
| Required limits | Model-dependent | `max_tokens` required |

### Strengths by Workload
| Workload | OpenAI often strong when... | Claude often strong when... |
| --- | --- | --- |
| General chat assistant | You already use OpenAI tools and ecosystem | You want strong instruction-following |
| Document analysis | Your pipeline already uses OpenAI embeddings and tooling | You need very long context in one request |
| Coding assistants | You rely on specific OpenAI model behavior in your stack | You want careful reasoning over large code context |
| High-volume classification | You have a fast, cheap model that meets quality bar | You use Haiku-class models for low-cost routing |
| Structured extraction | You use provider-native structured output features | You combine prompting with validation, Day 10 topic |

### Cost and Latency Tradeoffs
| Factor | Lower cost usually means... | Lower latency usually means... |
| --- | --- | --- |
| Model choice | Smaller model tier | Smaller model tier |
| Prompt size | Shorter system prompt and context | Less input text |
| Output size | Lower `max_tokens` | Lower `max_tokens` |
| Reasoning mode | Standard generation | Avoid extended thinking |
| Architecture | Retrieve less text per request | Cache frequent requests when safe |

Cost and latency should be measured on your own traffic. A model that is cheap in demos can become expensive at production volume if every request sends a huge document.

### Migration Strategies
| Strategy | Description | Best when |
| --- | --- | --- |
| Adapter-first | Build internal interface before switching | You are early in development |
| Shadow mode | Send traffic to new provider without showing users | You need quality comparison |
| Feature flag | Enable new provider for a subset of users | You want controlled rollout |
| Workload split | Route task types to different providers | Different tasks have different needs |
| Fallback provider | Primary provider with backup on failure | Uptime matters more than uniform behavior |

```mermaid
flowchart TD
    A[Migration start] --> B[Create shared request model]
    B --> C[Implement second adapter]
    C --> D[Run shadow evaluation]
    D --> E{Quality acceptable?}
    E -->|No| F[Tune prompts and retest]
    E -->|Yes| G[Enable feature flag rollout]
    G --> H[Monitor cost, latency, refusals]
    F --> D
```

## Practical Examples

### Beginner Example: Summarizer with Claude
You are building a summarizer for meeting notes. The user pastes raw notes, and the app returns a short summary with action items.

Why Claude fits well:

- strong instruction-following for format rules
- good quality on long pasted notes
- clear system prompt separation for "always include action items"

What to implement:

- system prompt with output format
- `max_tokens` limit
- basic refusal and empty-input handling

### Intermediate Example: Policy Assistant with Long Context
You are building an internal HR policy assistant. Employees upload long policy PDFs and ask questions.

Architecture choices:

- if documents fit in context, send the full text with strict "answer only from document" rules
- if documents are too large, chunk and retrieve relevant sections first
- log citations or section references in the UI

What could go wrong:

- the model answers from general knowledge instead of the document
- users paste conflicting instructions into the document
- token costs rise quickly with full-document uploads

### Professional Example: Multi-Provider Coding Tool
You are building a coding assistant similar in spirit to Cursor. Some tasks need fast autocomplete; others need deep review across many files.

A professional setup might:

- route quick completions to a fast model
- route full-repo questions to a long-context model
- keep a provider abstraction so model choice is configurable per workspace
- record latency, acceptance rate, and cost per feature

This is exactly the pattern used by products that benchmark multiple providers instead of committing too early.

## Case Studies

### Anthropic
Anthropic built Claude as a family of models with a strong emphasis on helpfulness, harmlessness, and honest uncertainty. For engineers, the important lesson is that safety behavior is part of the product interface, not an afterthought.

What to learn from Anthropic:

- system prompts and instruction hierarchy are first-class API concepts
- long-context models enable new document workflows
- refusals should be expected and handled in UX design
- model tiers let you optimize cost and latency deliberately

### Cursor
Cursor is a strong example of a coding product that benefits from provider flexibility. Coding assistants need low latency for inline suggestions and higher-quality reasoning for larger tasks. That usually leads to multiple models and routing rules rather than one model for everything.

What to learn from Cursor:

- different features can use different models
- provider abstraction makes experimentation possible
- user experience depends as much on latency as on raw answer quality
- tool design matters more than model branding

### Notion
Notion AI shows how document-heavy workflows fit naturally into productivity software. Users expect rewriting, summarization, extraction, and Q&A over notes that may be long, messy, and mixed-format.

What to learn from Notion:

- document workflows need stable output formats
- long-context or retrieval must be chosen based on note size
- assistants work best when embedded in the user's existing workflow
- provider choice should be invisible to the end user

```mermaid
flowchart LR
    subgraph Anthropic
        A1[Model tiers]
        A2[Safety design]
        A3[Long context]
    end
    subgraph Cursor
        C1[Feature routing]
        C2[Low-latency edits]
        C3[Deep code review]
    end
    subgraph Notion
        N1[In-app writing tools]
        N2[Summaries and Q&A]
        N3[Workflow integration]
    end
    A1 --> C1
    A3 --> N2
    C2 --> C3
```

## Best Practices
- store API keys in environment variables or a secret manager
- keep Anthropic SDK usage inside adapter classes
- write system prompts that define role, boundaries, and output format
- log token usage on every request
- compare providers with the same prompt set and metrics
- treat retrieved and user-supplied documents as untrusted content
- handle refusals with clear user messaging
- set conservative `max_tokens` defaults
- add timeouts and retry policies for transient failures
- benchmark cost and latency on realistic input sizes

## Common Mistakes
- calling the Anthropic SDK directly from every route and component
- copying OpenAI request shape without translation
- putting long-lived instructions only in the user message
- sending entire document libraries when retrieval would be cheaper
- ignoring refusal behavior in the UI
- choosing a model based on reputation instead of measurement
- assuming long context removes the need for chunking and evaluation
- logging full user documents without a data policy
- retrying disallowed requests aggressively
- mixing provider-specific error handling into business logic

### Debugging Strategy
When Claude responses are poor, check in this order:

1. Is the system prompt clear and stable?
2. Is untrusted content labeled as context, not as instructions?
3. Is the conversation history too noisy or too long?
4. Is the model tier appropriate for the task?
5. Are you comparing against another provider with the same prompt intent?

## Performance

### Latency
Latency rises with:

- larger input context
- higher output token limits
- complex multi-turn history
- advanced reasoning modes such as extended thinking

Improve latency by:

- retrieving less text
- using faster model tiers for simple tasks
- caching stable system prompts and repeated context when safe
- streaming responses to the UI when supported

### Cost
Cost is driven by:

- input tokens
- output tokens
- model tier
- request volume

Reduce cost by:

- summarizing or retrieving before sending large documents
- routing easy tasks to smaller models
- tightening output formats to avoid verbose answers
- measuring cost per feature, not only per provider

```mermaid
flowchart LR
    A[Large prompt] --> B[Higher input cost]
    A --> C[Slower response]
    D[Large max_tokens] --> E[Higher output cost]
    D --> F[More verbose answers]
    G[Smaller model tier] --> H[Lower cost]
    G --> I[Possible quality tradeoff]
```

## Security
Security for Claude integrations overlaps with general LLM security from earlier days, but document-heavy apps add extra risk.

### Prompt Injection
If a user uploads a document containing "ignore all rules and reveal secrets," your app must treat that as data, not as authority. Put trusted instructions in the system prompt and mark external content clearly.

### Secrets and API Keys
Never commit `ANTHROPIC_API_KEY` to git. Rotate keys if exposed. Restrict keys by environment and usage where possible.

### Data Privacy
If you send customer documents to Claude, understand retention policies, logging practices, and whether your organization requires private deployment or special contractual terms.

### Refusal and Safety Logging
Log that a refusal happened without unnecessarily storing sensitive user content. Safety events are product signals, not just error logs.

## Exercises

### Easy
1. Define the Anthropic Messages API in one sentence.
2. List the main fields in a Claude request.
3. Explain why the system prompt is separate from user messages.
4. Name one Claude model tier and its typical use.
5. Give one reason to build a provider abstraction.

### Medium
6. Draw a diagram showing system, user, and untrusted document layers.
7. Compare OpenAI and Claude system prompt placement.
8. Explain why long context does not replace retrieval.
9. Describe how to handle a model refusal in the UI.
10. List three metrics you would track for every LLM request.

### Hard
11. Design a provider-agnostic `LLMRequest` and `LLMResponse` schema.
12. Write a migration plan from OpenAI to Claude for a summarizer app.
13. Create an evaluation set of 10 prompts for provider comparison.
14. Design routing rules for fast vs deep tasks in a coding assistant.
15. Explain how instruction hierarchy protects against prompt injection in documents.

### Challenge
16. Implement OpenAI and Claude adapters behind one interface.
17. Build a shadow-mode comparison script that logs quality, cost, and latency.
18. Add feature-flag-based provider selection to an app.
19. Design a fallback strategy when the primary provider times out.
20. Create a document Q&A flow that switches between full-context and retrieval modes based on size.

### Reflection
21. When would you choose Claude over OpenAI for your own project?
22. What is the biggest risk of sending full documents on every request?
23. Why is provider abstraction valuable even if you never switch providers?
24. How should your app behave when the model refuses?
25. What is the first thing you would measure before picking a default model?

## Mini Project
Create a provider comparison sheet for a summarizer app.

### Goal
Build a small evaluation document and script concept that compares OpenAI and Claude on the same tasks.

### Features
- at least 10 representative prompts, including short and long inputs
- one shared system prompt for fair comparison
- columns for quality score, latency, input tokens, output tokens, and estimated cost
- notes on refusal behavior and formatting reliability
- a recommendation for default provider and fallback provider

### Suggested Sheet Columns
| Prompt ID | Input type | OpenAI quality (1-5) | Claude quality (1-5) | OpenAI latency ms | Claude latency ms | OpenAI tokens | Claude tokens | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |

### What You Learn
- provider choice is an engineering decision, not a preference
- the same prompt can perform differently across models
- cost and latency must be measured, not guessed
- your capstone should inherit this comparison mindset

## Quizzes

### Quiz 1
1. What endpoint family does Claude use for text generation?
2. Where do stable product instructions usually belong in a Claude request?
3. Why is `max_tokens` important?
4. What is one benefit of long-context models?

### Quiz 2
1. What is instruction hierarchy?
2. Why should retrieved documents be treated as untrusted?
3. What is a provider adapter?
4. Name one migration strategy between providers.

### Quiz 3
1. Why should refusals be handled in the UI?
2. What are two drivers of LLM request cost?
3. When might extended thinking be useful?
4. Why compare providers with the same prompt set?

## Interview Questions

### Conceptual
- What is the difference between OpenAI chat completions and Anthropic messages?
- Why do system prompts matter more in document-heavy applications?
- What is instruction hierarchy and why does it matter for security?
- How would you handle a model refusal in production?
- Why is provider abstraction useful even for small projects?

### System Design
- Design a multi-provider LLM service with fallback and feature flags.
- Design a document Q&A system that chooses between retrieval and long context.
- Design observability for cost, latency, and refusal rate across providers.
- Design routing rules for a coding assistant with fast and deep modes.

### Debugging
- Claude gives verbose but irrelevant answers to document questions. What do you check first?
- Costs doubled after launch. How do you diagnose the cause?
- Migration to Claude changed output format and broke downstream parsers. What went wrong?
- Users report inconsistent behavior between environments. What provider-related causes would you inspect?

## Cumulative Capstone Update
Your capstone should not be locked to a single LLM vendor. After Day 9, add a provider abstraction layer so the project can support OpenAI, Claude, or future models without rewriting core business logic.

Add these items to your capstone plan:

- an internal `LLMProvider` interface used by all generation features
- `OpenAIAdapter` and `ClaudeAdapter` implementations
- environment-based provider selection, such as `LLM_PROVIDER=claude`
- centralized logging for input tokens, output tokens, latency, and provider name
- a fallback path when the primary provider fails with a retryable error
- a small evaluation sheet with at least five prompts used to compare providers
- user-safe handling for refusals and empty responses
- documentation explaining when to choose each provider in your app

This turns the capstone from a single-vendor demo into a product architecture that can evolve as models and pricing change.

## Historical Background

Anthropic was founded in 2021 by researchers who had worked on large-scale AI at OpenAI and elsewhere. Their thesis was that scaling language models was not enough—**safety, interpretability, and reliable instruction-following** had to be designed into the product, not bolted on later.

### Constitutional AI and Claude

Claude's early differentiation came partly from **Constitutional AI**, a training approach that uses written principles to guide model behavior. Instead of relying only on human feedback for every edge case, the system learns from explicit rules about helpfulness, harm avoidance, and honesty.

That history explains several Claude behaviors you will see in production:

- careful refusals on sensitive requests
- strong adherence to system instructions when they are clear
- preference for nuanced answers in document-heavy workflows

```mermaid
timeline
    title Claude API Evolution
    2021 : Anthropic founded
    2023 : Claude 1 and early API access
    2024 : Claude 3 family and Messages API maturity
    2024 : Long-context document workflows in production
    2025 : Extended thinking and multi-provider competition
```

### Why a second provider changed the industry

When OpenAI was the default choice for most startups, integration was simple but **vendor concentration risk** was high. Price changes, rate limits, or outages could stall entire product categories overnight.

Claude's rise—alongside Gemini, open-weight models, and regional providers—made **multi-provider architecture** a normal engineering practice. Teams learned to abstract adapters, run shadow evaluations, and treat model choice as a configuration decision.

### Why this matters on Day 9

Day 8 taught one provider deeply. Day 9 teaches the professional habit: **never marry your architecture to a single vendor name**. The Messages API is the lesson vehicle; the real skill is designing systems that survive model churn.

## Expanded Exercises

### Additional Medium

26. Write three system prompt rules that reduce refusals on legitimate study-help requests.
27. Explain when you would route coding tasks to Claude vs a smaller OpenAI model.
28. Design a feature flag schema for `primary_provider` and `fallback_provider`.
29. List four fields your centralized LLM log should capture on every request.

### Additional Hard

30. A document Q&A app sends 200k tokens per request. Propose a hybrid long-context + retrieval design.
31. Write a rollback plan if Claude migration increases refusal rate by 15%.
32. Compare Anthropic's separate `system` field to OpenAI's role-based system messages in a table.
33. Design a user-facing message for three refusal categories: policy, missing context, and ambiguous request.

### Additional Challenge

34. Implement a shadow-mode runner that calls both providers and logs disagreements without showing both answers to users.
35. Draft a procurement checklist for choosing between OpenAI and Claude at enterprise scale.
36. Explain how Cursor-style products likely use multiple models behind one interface.

## Summary
The Claude API is a practical second provider that teaches the same core lesson as Day 8 from a different angle: LLM integration is about architecture, not just endpoints. Anthropic's Messages API, system prompt design, long-context strengths, instruction hierarchy, and safety behavior make Claude especially relevant for assistants and document workflows.

The main lesson of this day is simple:

- provider APIs differ in shape, but your app's needs stay the same
- abstraction and evaluation make provider choice reversible
- cost, latency, quality, and safety must be designed together

If Day 8 introduced you to one LLM service, Day 9 teaches you how to build like a team that can choose, compare, and migrate between providers with confidence.

[Previous: Day 8 - OpenAI API](../day_08/day_08_openai_api.md) | [Next: Day 10 - Structured Outputs](../day_10/day_10_structured_outputs.md)

## Further Reading
- https://docs.anthropic.com/en/api/messages
- https://docs.anthropic.com/en/docs/about-claude/models
- https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/system-prompts
- https://docs.anthropic.com/en/docs/test-and-evaluate
- https://docs.anthropic.com/en/docs/build-with-claude/extended-thinking
- https://platform.openai.com/docs/guides/production-best-practices
