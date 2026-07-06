# Day 20 - Long-Term Memory

## Introduction
Long-term memory stores useful information across many sessions so the assistant can behave more consistently over time. The challenge is not only saving memory, but deciding what should persist.

![Visual diagram](../images/week_3_retrieval.svg)

## Learning Objectives
By the end of this day, you should be able to:

- explain the difference between session and long-term memory
- understand summarization and retrieval for memory systems
- design memory expiration or refresh rules
- think about personalization without overreach
- plan a simple memory lifecycle

## Theory
Long-term memory is useful when the assistant should remember stable preferences, recurring goals, or important facts. But long-term memory must be carefully managed because stale or wrong memory can create bad experiences.

A strong design usually includes write rules, read rules, review tools, and deletion support.

### Visual Diagram
```mermaid
graph LR
    SessionData --> MemoryFilter
    MemoryFilter --> PersistentStore
    PersistentStore --> MemoryRetriever
    MemoryRetriever --> NewSession
```

## Code Examples

### Python
```python
long_term_memory = [
    "Prefers concise answers",
    "Is learning AI engineering",
]
print(long_term_memory)
```

### TypeScript
```typescript
const longTermMemory = [
  'Prefers concise answers',
  'Is learning AI engineering',
];

console.log(longTermMemory);
```

## Best Practices
- store memory only when it improves future help
- use summaries instead of raw transcripts
- let users review and correct memory
- expire or revalidate old information
- log why a memory was created

## Common Mistakes
- over-personalizing too early
- failing to correct stale memory
- merging every session into permanent storage
- hiding memory behavior from the user
- confusing preference memory with factual memory

## Exercises
- Easy: Define long-term memory.
- Medium: Explain why stale memory is dangerous.
- Hard: Design a memory review screen.
- Challenge: Create rules for promoting session data into long-term memory.

## Mini Project
Design a long-term memory system for a tutoring assistant. Include memory creation, retrieval, update, and deletion.

## Summary
Long-term memory makes assistants feel persistent, but persistence only helps when the stored information is accurate, useful, and user-controlled.

## Additional Resources
- https://mem0.ai/
- https://docs.langchain.com/
- https://modelcontextprotocol.io/
