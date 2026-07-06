# Day 10 - Structured Outputs

## Introduction
Structured outputs make the model return data in a predictable format such as JSON, tables, or schema-based objects. This is essential when an AI app needs to feed its output into code.

![Visual diagram](../images/week_2_apps.svg)

## Learning Objectives
By the end of this day, you should be able to:

- explain why structure matters more than free-form text for many applications
- design a simple JSON schema for model output
- validate model output before using it downstream
- understand where structured outputs reduce bugs
- create output shapes for extraction tasks

## Theory
Free-form answers are good for conversation, but software often needs exact fields. If your app wants `title`, `summary`, and `tags`, the model should return those fields consistently.

The more downstream automation you have, the more important structure becomes. Structured outputs reduce parsing errors, make logging easier, and simplify testing.

### Visual Diagram
```mermaid
graph LR
    Prompt --> Model
    Model --> JSON
    JSON --> Validator
    Validator --> App
```

## Code Examples

### Python
```python
import json

output = {
    "title": "AI Engineering Basics",
    "summary": "A short lesson about building practical AI software.",
    "tags": ["ai", "engineering", "llm"],
}

print(json.dumps(output, indent=2))
```

### TypeScript
```typescript
const output = {
  title: 'AI Engineering Basics',
  summary: 'A short lesson about building practical AI software.',
  tags: ['ai', 'engineering', 'llm'],
};

console.log(JSON.stringify(output, null, 2));
```

## Best Practices
- define the schema before the prompt is written
- keep fields narrow and purposeful
- validate output before writing to a database
- reject or repair malformed outputs
- use structured output for extraction and routing tasks

## Common Mistakes
- asking for JSON but not validating it
- making the schema too large
- mixing explanatory text with machine-readable fields
- relying on string parsing for critical workflows
- forgetting to handle missing fields

## Exercises
- Easy: Design a JSON schema for a movie review.
- Medium: Explain why structure helps automation.
- Hard: Define validation rules for a user profile extractor.
- Challenge: Create a repair strategy for invalid model output.

## Mini Project
Create a schema for turning a paragraph into title, summary, sentiment, and keywords. Describe how your app should handle invalid JSON.

## Summary
Structured outputs turn model answers into reliable application data. When downstream code depends on the response, structure is a requirement, not a nice-to-have.

## Additional Resources
- https://platform.openai.com/docs/guides/structured-outputs
- https://docs.anthropic.com/en/docs/build-with-claude/structured-outputs
- https://json-schema.org/
