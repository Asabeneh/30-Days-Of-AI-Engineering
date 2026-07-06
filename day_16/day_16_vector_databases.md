# Day 16 - Vector Databases

[Previous: Day 15 - Embeddings](../day_15/day_15_embeddings.md) | [Next: Day 17 - RAG](../day_17/day_17_rag.md)

## Introduction
Yesterday we learned that embeddings turn meaning into numbers. Today we answer the next question: where do we store those numbers, how do we search them, and how do we do it fast enough for real applications?

A vector database is a system that stores vectors, indexes them, filters them with metadata, and returns the most similar matches for a query. This is the retrieval engine behind semantic search, knowledge assistants, recommendation systems, and most RAG pipelines.

![Visual diagram](../images/week_3_retrieval.svg)

Think of it like a very large library with two kinds of labels:

- the normal library labels such as title, author, date, and category
- the meaning labels, which are embeddings that capture what the content is about

A regular database is good at exact matches. A vector database is good at meaning-based matches. In production, we often need both.

## Learning Objectives
By the end of this day, you should be able to:

- explain what a vector database is and why it exists
- describe brute-force search and approximate nearest neighbor search
- understand how indexes like HNSW and IVF help speed up retrieval
- use metadata filters to narrow search results
- compare local and hosted vector stores
- choose a vector database for a small or medium AI project
- explain when vector search is the right tool and when it is not

## How to Use This Lesson

This lesson is designed for **all skill levels**. Pick one path and follow it consistently.

| Level | Suggested approach | Time |
| --- | --- | --- |
| **Beginner** | Read Introduction → Big Picture → Deep Theory → trace one code example → Easy exercises | 5–7 hours |
| **Intermediate** | Skim objectives → Visual Learning → Code Walkthrough → Medium/Hard exercises → Mini project | 3–5 hours |
| **Advanced** | Deep Theory tradeoffs → Hard/Challenge exercises → extend mini project → capstone slice | 2–4 hours |

### Apply Today
Complete at least one item before moving to the next day:
- [ ] Trace one code example in **Python or TypeScript** (one language is enough)
- [ ] Complete exercises for your level (see Exercises section)
- [ ] Update [`projects/CAPSTONE.md`](../../projects/CAPSTONE.md) with today's capstone item
- [ ] Update the retrieval or memory section in `projects/CAPSTONE.md`.

> **Stuck?** Re-read Big Picture, review Prerequisites, or see [SYLLABUS.md](../../SYLLABUS.md) for path guidance.

## Prerequisites
You should already understand:

- Day 15: Embeddings
- basic Python or TypeScript syntax
- the idea of similarity search
- why chunking matters in retrieval systems

If any of those feel new, go back and review Day 15 first. Vector databases make much more sense after you understand embeddings.

## Big Picture
Vector databases sit between content ingestion and answer generation.

```mermaid
flowchart LR
    A[Documents] --> B[Chunking]
    B --> C[Embeddings]
    C --> D[Vector Database]
    E[User Query] --> F[Query Embedding]
    F --> D
    D --> G[Top Matches]
    G --> H[RAG or Search Result]
```

The important idea is this:

- embeddings convert text into vectors
- the vector database stores and searches those vectors
- retrieval systems use the matches to ground answers, rank content, or recommend items

Without a vector database, you can still compute similarities, but only by scanning everything one by one. That becomes too slow as your collection grows.

## Deep Theory

### What problem does a vector database solve?
Suppose you have 10,000 support articles. A user asks, “How do I reset my billing account after a failed payment?”

A keyword search may miss the answer if the article uses different words like “payment retry” or “account recovery.” A vector search can still find it because the query and the article may be close in meaning.

Now imagine doing that for 1 million chunks. If you compare the query vector with every stored vector, the search will eventually become too slow.

That is the core reason vector databases exist:

1. store vectors efficiently
2. search them quickly
3. combine meaning with metadata rules
4. scale beyond tiny demos

### How vector search works internally
At a high level, the process is:

1. create an embedding for each document chunk
2. store the vector plus metadata
3. create an embedding for the user query
4. compare the query vector with stored vectors using a similarity metric
5. return the best matches

The similarity metric is usually one of these:

| Metric | What it measures | Common use |
| --- | --- | --- |
| Cosine similarity | Angle between vectors | Semantic search |
| Dot product | Alignment and magnitude | Retrieval and ranking |
| Euclidean distance | Straight-line distance | Some clustering and nearest-neighbor tasks |

Cosine similarity is popular because it focuses on direction rather than raw vector length. In embeddings, direction often matters more than magnitude.

### Why not just scan everything?
Brute-force search checks every vector. That is simple, accurate, and easy to understand. The problem is speed.

If you have $N$ vectors, brute-force search is roughly $O(N)$ per query. That means the cost grows linearly as your collection grows.

Vector databases usually use approximate nearest neighbor indexes to reduce search time. The result is not always mathematically perfect, but it is usually good enough and dramatically faster.

### Approximate Nearest Neighbor search
ANN search trades a little accuracy for a lot of speed.

Instead of comparing the query with every vector, the database uses an index that narrows the search space. Common approaches include:

- HNSW, which builds a graph of nearby vectors
- IVF, which clusters vectors and searches only the most relevant clusters
- PQ, which compresses vectors to reduce memory use

The right index depends on your scale, latency needs, and accuracy goals.

### HNSW in simple terms
HNSW means Hierarchical Navigable Small World.

The idea is to create a graph where each vector is connected to nearby vectors. To find a good match, the system starts from a useful entry point and walks through the graph toward better neighbors.

```mermaid
flowchart TD
    A[Start from entry node] --> B[Check nearby neighbors]
    B --> C{Closer match found?}
    C -- Yes --> D[Move toward better region]
    C -- No --> E[Return best current candidates]
    D --> B
```

Why it helps:

- it avoids checking every vector
- it works well for dynamic datasets
- it often gives strong recall with good speed

### IVF in simple terms
IVF means Inverted File Index.

It groups vectors into clusters first. When a query arrives, the system searches only the most relevant clusters.

This is like asking a librarian to check only the right shelf area instead of the whole building.

### Compression and quantization
Large vector collections can consume a lot of memory. Compression techniques reduce storage cost by representing vectors more compactly.

That helps when:

- your dataset is very large
- memory is expensive
- you need higher throughput

The tradeoff is usually a small drop in precision.

### Metadata is not optional
Vectors alone are not enough.

Metadata lets you ask questions like:

- only search documents from 2025
- only search content tagged as finance
- only search chunks from one customer account
- only search results the current user is allowed to see

This is why the best systems treat vector search and metadata filtering as one combined retrieval strategy.

### When should you use a vector database?
Use one when you need any of these:

- semantic search
- RAG
- recommendation or similarity matching
- deduplication by meaning
- clustering and organization of content
- multimodal retrieval such as image or audio similarity

### When should you not use one?
Do not use one when:

- you only need exact lookups by ID
- your dataset is tiny and brute force is simpler
- a normal SQL query already solves the problem
- you need strict transactional reporting, not similarity search

Vector search is powerful, but it is not a replacement for every database.

### Advantages
- semantic search works better than keyword search for many tasks
- retrieval can scale to large collections
- metadata filtering adds business control
- many databases support hybrid search and filters
- vector stores fit naturally into RAG systems

### Limitations
- approximate search can miss some results
- vector quality depends on embedding quality
- poor chunking leads to poor retrieval
- indexes add complexity
- storage and query costs can rise with scale

### Alternatives
- PostgreSQL with pgvector for teams that already use Postgres
- FAISS for local or research setups
- Elasticsearch or OpenSearch for hybrid keyword and vector search
- Chroma for small prototypes and local development
- Qdrant, Weaviate, Pinecone, and Milvus for more production-focused retrieval

### Best fit by scenario
| Scenario | Better choice |
| --- | --- |
| Quick prototype | Chroma or FAISS |
| Existing SQL stack | PostgreSQL with pgvector |
| Strong filtering and production retrieval | Qdrant or Weaviate |
| Managed cloud service | Pinecone |
| Hybrid keyword plus vector search | OpenSearch or Elasticsearch |

## Visual Learning

### Retrieval Pipeline
```mermaid
sequenceDiagram
    participant U as User
    participant A as App
    participant E as Embedding Model
    participant V as Vector DB

    U->>A: Ask a question
    A->>E: Embed query
    E-->>A: Query vector
    A->>V: Search similar vectors with filters
    V-->>A: Top matching chunks
    A-->>U: Show results or send context to LLM
```

### Decision Tree
```mermaid
flowchart TD
    S[Do you need meaning-based search?] -->|No| N[Use a normal database or search engine]
    S -->|Yes| T[Do you need real-time scale?]
    T -->|No| F[FAISS or local vector store]
    T -->|Yes| P[Production vector database]
    P --> Q[Add metadata filters and evaluation]
```

### Mental Model
```mermaid
mindmap
  root((Vector Database))
    Store vectors
    Search by similarity
    Filter by metadata
    Scale retrieval
    Support RAG
    Reduce search time
```

## Code Walkthrough

The examples below are intentionally simple. The goal is to understand the moving parts, not to hide them behind a framework.

### Python Example: Local Vector Search with Metadata
```python
from math import sqrt


def cosine_similarity(vector_a, vector_b):
    """Return cosine similarity between two equal-length vectors."""
    dot_product = sum(a * b for a, b in zip(vector_a, vector_b))
    magnitude_a = sqrt(sum(a * a for a in vector_a))
    magnitude_b = sqrt(sum(b * b for b in vector_b))

    if magnitude_a == 0 or magnitude_b == 0:
        return 0.0

    return dot_product / (magnitude_a * magnitude_b)


documents = [
    {
        "id": "doc-1",
        "text": "How to reset your billing password.",
        "vector": [0.92, 0.10, 0.18],
        "metadata": {"topic": "billing", "source": "help-center"},
    },
    {
        "id": "doc-2",
        "text": "How to update your email address.",
        "vector": [0.15, 0.88, 0.12],
        "metadata": {"topic": "account", "source": "help-center"},
    },
    {
        "id": "doc-3",
        "text": "How to retry a failed payment.",
        "vector": [0.88, 0.12, 0.20],
        "metadata": {"topic": "billing", "source": "faq"},
    },
]

query_vector = [0.90, 0.11, 0.21]
topic_filter = "billing"

matches = []

for document in documents:
    if document["metadata"]["topic"] != topic_filter:
        continue

    score = cosine_similarity(query_vector, document["vector"])
    matches.append({"id": document["id"], "text": document["text"], "score": score})

matches.sort(key=lambda item: item["score"], reverse=True)

print("Top matches:")
for match in matches:
    print(f"{match['id']}: {match['score']:.3f} - {match['text']}")
```

#### Code Explanation
- `cosine_similarity` measures how close two vectors point in the same direction.
- `documents` acts like a tiny vector collection.
- each item has an `id`, a `text` field, a `vector`, and `metadata`.
- `query_vector` represents the user question after embedding.
- `topic_filter` shows how metadata filters narrow search before ranking.
- the `for` loop skips documents that do not match the filter.
- `score` computes semantic closeness.
- `matches.sort(...)` puts the most relevant result first.
- the final loop prints the ranked search result.

This is the logic a vector database automates for you at scale.

### TypeScript Example: Query Preparation and Ranking
```typescript
type DocumentItem = {
  id: string;
  text: string;
  vector: number[];
  metadata: {
    topic: string;
    source: string;
  };
};

function cosineSimilarity(vectorA: number[], vectorB: number[]): number {
  let dotProduct = 0;
  let magnitudeA = 0;
  let magnitudeB = 0;

  for (let index = 0; index < vectorA.length; index += 1) {
    dotProduct += vectorA[index] * vectorB[index];
    magnitudeA += vectorA[index] * vectorA[index];
    magnitudeB += vectorB[index] * vectorB[index];
  }

  if (magnitudeA === 0 || magnitudeB === 0) {
    return 0;
  }

  return dotProduct / (Math.sqrt(magnitudeA) * Math.sqrt(magnitudeB));
}

const documents: DocumentItem[] = [
  {
    id: 'doc-1',
    text: 'How to reset your billing password.',
    vector: [0.92, 0.1, 0.18],
    metadata: { topic: 'billing', source: 'help-center' },
  },
  {
    id: 'doc-2',
    text: 'How to update your email address.',
    vector: [0.15, 0.88, 0.12],
    metadata: { topic: 'account', source: 'help-center' },
  },
];

const queryVector = [0.9, 0.11, 0.21];
const results = documents
  .filter((document) => document.metadata.topic === 'billing')
  .map((document) => ({
    id: document.id,
    text: document.text,
    score: cosineSimilarity(queryVector, document.vector),
  }))
  .sort((left, right) => right.score - left.score);

console.log(results);
```

#### Code Explanation
- `DocumentItem` defines the shape of one stored item.
- `cosineSimilarity` is the ranking function.
- `documents` simulates a small in-memory collection.
- `filter(...)` applies metadata constraints first.
- `map(...)` computes similarity scores for the remaining items.
- `sort(...)` ranks the most relevant result first.

In a real app, the vector database does the filtering, ranking, and index lookup for you.

## Practical Examples

### Beginner Example
You are building a study notes search app for a class. The user types “exam schedule for week 4.” The system embeds the query, searches the note embeddings, and returns the most similar note chunks.

Why this helps:

- students do not need exact wording
- notes can be searched by meaning
- the app becomes much more useful than keyword search alone

### Intermediate Example
You are building a customer support assistant. Each ticket is stored with metadata such as product line, language, and creation date.

When a user asks a question, you first filter by language and product, then rank the most relevant vector matches. This reduces noise and improves answer quality.

### Professional Example
You are building a legal research assistant for an enterprise. The system must:

- store millions of chunks
- enforce access control per user group
- support fast retrieval with low latency
- keep source references for every answer
- evaluate recall and precision regularly

In this case, the vector database is not a nice extra. It is part of the core product architecture.

### Real-World Company Example
A SaaS company may store help articles, product docs, release notes, and support history in a vector database. Their assistant can then answer questions like:

- “How do I connect SSO?”
- “Why was my invoice rejected?”
- “What changed in the latest API version?”

The system uses semantic search to find relevant context, then a language model to generate a helpful response.

## Best Practices
- chunk content before embedding it
- store stable IDs for every chunk
- keep metadata clean and consistent
- choose the simplest index that meets your latency target
- test retrieval with real user questions, not only toy examples
- separate retrieval evaluation from generation evaluation
- store source references so answers can be traced back
- cache frequent queries when the data does not change often
- version your embedding model and index settings
- monitor recall, latency, and cost together

## Common Mistakes
- treating vector search like magic search
- skipping metadata design
- using one giant chunk for everything
- choosing a database before understanding the workload
- forgetting to re-embed content after changing the embedding model
- ignoring access control and data privacy
- asking the model to compensate for weak retrieval
- not checking whether the top result is actually useful

### Debugging Strategy
When retrieval quality is bad, check the system in this order:

1. Are the chunks clean and meaningful?
2. Are the embeddings from the right model?
3. Are metadata filters too strict or too loose?
4. Is the index configured for the right scale?
5. Are you evaluating with real user queries?

This order matters because the problem is often not the database itself. It is usually the data going into it.

## Performance

Vector databases are often judged by four numbers:

- latency
- cost
- memory use
- retrieval quality

### Latency
Latency is the time between the user query and the returned matches.

You can improve latency by:

- using an ANN index
- reducing collection size with filters
- caching common queries
- storing vectors with the right dimension
- avoiding unnecessary post-processing

### Cost
Cost grows when:

- you store many vectors
- you re-embed content often
- you use a managed service at large scale
- your index is memory heavy

The cheapest system is not always the best system. The right question is whether the retrieval quality justifies the cost.

### Memory
Vector collections can grow fast.

If you store millions of chunks, memory becomes a major concern. That is why systems use compression, sharding, and compact indexes.

### Scalability
To scale retrieval, teams often:

- shard by tenant or domain
- keep hot data in faster storage
- use hybrid search to reduce noise
- add separate indexes for different collections
- batch ingestion jobs instead of writing one vector at a time

### Token Optimization
Vector databases help reduce token waste downstream.

Instead of sending an entire document to the model, you retrieve only the most relevant chunks. That lowers context size, speeds up generation, and cuts API cost.

## Security

Security matters in retrieval systems because they often handle private content.

### Prompt Injection
If retrieved documents contain malicious instructions, the language model may follow them unless your system is careful.

Protect against this by:

- separating retrieved facts from instructions
- using system prompts that define trust boundaries
- sanitizing untrusted text
- limiting what the model can do with retrieved content

### Secrets and API Keys
Do not store secrets in vector content.

If a secret gets embedded and indexed, it can become searchable in ways you did not intend.

### Authentication and Authorization
Users should only retrieve data they are allowed to access.

Metadata filters are often used to enforce tenant or role-based access. That is useful, but it is not enough by itself. Access control should also exist at the application and service layer.

### Data Privacy
If you index customer data, personal information, or internal documents, make sure your retention and deletion policies are clear.

### Hallucinations and Model Safety
Even with a great vector database, the final answer can still be wrong if the language model overstates what it found.

To reduce that risk:

- show sources
- keep the generation prompt grounded
- ask the model to say when it is unsure
- evaluate answers against source documents

## Exercises

### Easy
Explain what a vector database stores and why it is useful.

### Medium
Describe how metadata filters improve retrieval quality.

### Hard
Compare brute-force search, HNSW, and IVF in simple words.

### Challenge
Design a vector retrieval schema for a company knowledge base. Include chunk IDs, metadata fields, filters, and source tracking.

### Reflection Questions
- When is vector search better than keyword search?
- When is keyword search still the better choice?
- What happens if your chunks are too large?
- What happens if your metadata is messy?
- Why is ANN search a tradeoff rather than a perfect solution?

## Mini Project
Build the retrieval layer for a study assistant called NoteFinder.

### Goal
Create a small system that stores note chunks, tags them with metadata, and returns the most relevant chunks for a user question.

### Features
- ingest study notes from a folder
- split notes into chunks
- create or mock embeddings for each chunk
- store vectors with metadata such as subject, date, and source file
- search by query vector
- filter by subject
- return the top 3 results with scores

### Suggested Folder Structure
```text
notefinder/
├── app/
│   ├── ingest.py
│   ├── embeddings.py
│   ├── retrieval.py
│   └── main.py
├── data/
│   └── notes/
├── tests/
│   └── test_retrieval.py
└── README.md
```

### Project Steps
1. read note files from `data/notes`
2. split them into chunks of a reasonable size
3. generate embeddings for each chunk
4. store each chunk with metadata
5. build a search function that ranks similar chunks
6. add a filter for subject or course
7. test the system with real student questions

### What You Learn
- how retrieval pipelines are assembled
- why metadata matters
- how search quality depends on data quality
- how vector search prepares you for RAG in Day 17

## Historical Background
Vector databases did not appear because engineers wanted another buzzword. They appeared because classic search systems were not enough once AI applications started needing meaning-based retrieval over large collections.

### From exact match to semantic match
Traditional databases and search engines are excellent at exact values. If you know the identifier, the title, or the keyword, they can find the record very quickly.

The problem is that people do not always ask precise questions. They ask in natural language, using paraphrases, synonyms, and incomplete descriptions. A semantic retrieval system must understand intent, not just words.

Embeddings gave engineers a way to represent meaning numerically. Vector databases gave them a practical way to store and search those representations at scale.

### Why the field evolved this way
The evolution went roughly like this:

1. search by exact words
2. add ranking and stemming
3. add embeddings for meaning
4. add vector indexes for speed
5. add metadata filters and hybrid search for production use

That sequence matters. Each step solved a problem that the previous step could not handle well enough.

```mermaid
timeline
    title Retrieval Evolution
    1990s : Keyword search and inverted indexes
    2010s : Word and sentence embeddings
    2017 : Transformer-based contextual embeddings
    2020s : Vector databases and RAG systems
```

## More Comparison Tables

### Retrieval Approaches
| Approach | What it optimizes for | Strength | Weakness |
| --- | --- | --- | --- |
| Exact lookup | Precision | Very reliable | Cannot handle paraphrase |
| Keyword search | Word overlap | Simple and fast | Misses semantic matches |
| Vector search | Meaning similarity | Handles synonyms and paraphrases | Approximate and harder to explain |
| Hybrid search | Words plus meaning | Strong balanced retrieval | More tuning required |

### Database Choice
| Choice | Best for | Pros | Cons |
| --- | --- | --- | --- |
| pgvector | SQL teams | Familiar stack, easy filtering | Not ideal for every large-scale use case |
| FAISS | Local experiments | Fast, lightweight, simple | Not a full production database |
| Chroma | Learning and prototypes | Easy developer experience | Smaller ecosystem than some alternatives |
| Qdrant | Filtering and production retrieval | Strong search features | Requires deployment and ops |
| Pinecone | Managed production retrieval | Low ops overhead | Service cost |
| Weaviate | Flexible schema and hybrid search | Rich capabilities | More architecture decisions |

### Retrieval Quality Factors
| Factor | Good outcome | Bad outcome |
| --- | --- | --- |
| Chunk size | Enough context without overload | Too broad or too fragmented |
| Embedding model | Captures meaning well | Poor semantic separation |
| Metadata | Clean and structured | Hard to filter and debug |
| Index type | Fast and accurate enough | Slow or low recall |
| Query design | Focused intent | Vague and noisy retrieval |

## More Practical Examples

### Beginner Example: Search class notes by meaning
A student searches for “what does the lesson say about context length?” even though the notes use the phrase “context window.”

The vector database still returns the right chunk because the concepts are close in embedding space.

Why it works:

- the query and the notes share semantic meaning
- paraphrases do not break the search
- metadata can restrict the search to the correct week or topic

### Intermediate Example: Support ticket retrieval
A customer support platform stores previous tickets as chunks with metadata such as product, region, and language.

When a new ticket arrives, the system searches for similar past issues. That helps support agents answer faster and more consistently.

What could go wrong:

- tickets may contain multiple topics mixed together
- old data may be irrelevant if the product changed
- poor metadata can return the wrong product version

### Advanced Example: Multimodal product search
A shopping app wants to search by text query, example image, or both.

The app stores text embeddings for product descriptions and image embeddings for product photos. The vector database retrieves similar items from both spaces.

Why professionals care:

- users can search in a natural way
- product discovery improves
- the same retrieval architecture supports more than one modality

### Production Example: Enterprise policy assistant
An enterprise assistant answers policy questions from handbooks, contracts, and internal docs.

The retrieval service must combine:

- vector search for semantic recall
- metadata filters for department and access control
- logging for audits
- reranking for precision

This is where vector databases stop being a prototype tool and become part of the company’s information infrastructure.

### Real Company Example: Knowledge platforms
Products like Notion, GitHub, and other knowledge-centric systems all benefit from semantic retrieval. Users write content in inconsistent ways, but the system still needs to find the right page, note, issue, or doc.

The common pattern is the same:

- store chunks
- embed them
- filter by metadata
- retrieve by similarity
- present the most useful result quickly

## More Visual Learning

### Layered Architecture
```mermaid
graph TB
    U[User Interface] --> Q[Query Builder]
    Q --> E[Embedding Service]
    E --> F[Filter Engine]
    F --> V[Vector Index]
    V --> R[Ranking Layer]
    R --> A[Answer Builder]
```

### Retrieval Decision Tree
```mermaid
flowchart TD
    A[What kind of search do you need?] --> B{Exact value?}
    B -->|Yes| C[Use SQL or keyword lookup]
    B -->|No| D{Need meaning?}
    D -->|Yes| E{Need scale?}
    E -->|No| F[Use local vector store]
    E -->|Yes| G[Use production vector database]
    D -->|No| H[Use a regular search engine]
```

### Retrieval Data Flow
```mermaid
flowchart LR
    A[Raw content] --> B[Clean and chunk]
    B --> C[Embed chunks]
    C --> D[Store vectors]
    D --> E[Build ANN index]
    F[User question] --> G[Embed query]
    G --> H[Apply filters]
    H --> I[Search index]
    I --> J[Return top matches]
```

## Additional Code Examples

### Python Example: Brute-force search for tiny datasets
```python
def brute_force_search(query_vector, documents):
    scored = []

    for document in documents:
        score = cosine_similarity(query_vector, document["vector"])
        scored.append((score, document["text"]))

    return sorted(scored, reverse=True)


small_documents = [
    {"text": "Reset your password.", "vector": [0.9, 0.1, 0.2]},
    {"text": "Update your billing email.", "vector": [0.2, 0.8, 0.1]},
]

print(brute_force_search([0.88, 0.12, 0.2], small_documents))
```

### Why this example matters
- brute force is simple and trustworthy for very small collections
- it shows the exact logic that ANN later approximates
- it helps learners see why vector databases exist in the first place

### TypeScript Example: Metadata filter builder
```typescript
type Filters = {
  topic?: string;
  source?: string;
  accessLevel?: string;
};

function buildFilters(filters: Filters): string {
  const parts: string[] = [];

  if (filters.topic) {
    parts.push(`topic = '${filters.topic}'`);
  }

  if (filters.source) {
    parts.push(`source = '${filters.source}'`);
  }

  if (filters.accessLevel) {
    parts.push(`access_level = '${filters.accessLevel}'`);
  }

  return parts.join(' AND ');
}

console.log(buildFilters({ topic: 'billing', accessLevel: 'internal' }));
```

### Why this example matters
- it makes filters explicit and debuggable
- it mirrors how real retrieval APIs accept structured filter objects
- it shows why metadata design should happen early

### Pseudocode Example: Re-embedding a collection
```text
1. Export existing content and metadata
2. Generate embeddings with the new model
3. Write the new vectors to a shadow index
4. Compare old and new retrieval quality
5. Swap traffic only after validation passes
```

### Why this example matters
- embedding upgrades are common in production
- rebuilding safely prevents service disruption
- shadow testing reduces the chance of a bad rollout

### SQL Example: Querying content with metadata plus vector rank
```sql
SELECT id, topic, source
FROM notes
WHERE access_level = 'internal'
ORDER BY embedding <=> '[0.90, 0.11, 0.21]'
LIMIT 5;
```

### Why this example matters
- it shows how structured data and vectors can work together
- many teams prefer keeping retrieval close to their existing database stack
- SQL remains valuable even in vector-heavy systems

### Python Example: Upserting a chunk with metadata
```python
chunk = {
  "id": "lesson-16-chunk-01",
  "text": "Vector databases store embeddings and metadata.",
  "vector": [0.91, 0.10, 0.19],
  "metadata": {
    "lesson": "day_16",
    "topic": "vector-databases",
    "source": "course-notes",
  },
}

print(chunk)
```

### Why this example matters
- every vector record should keep traceable metadata
- stable IDs make updates and deletes easier
- source tracking helps with debugging and citations

### TypeScript Example: Hybrid scoring idea
```typescript
type SearchHit = {
  id: string;
  keywordScore: number;
  vectorScore: number;
};

function combineScores(hit: SearchHit): number {
  const keywordWeight = 0.4;
  const vectorWeight = 0.6;

  return (hit.keywordScore * keywordWeight) + (hit.vectorScore * vectorWeight);
}

const rankedHits = [
  { id: 'a', keywordScore: 0.9, vectorScore: 0.7 },
  { id: 'b', keywordScore: 0.3, vectorScore: 0.95 },
].map((hit) => ({ ...hit, finalScore: combineScores(hit) }));

console.log(rankedHits);
```

### Why this example matters
- hybrid ranking is often stronger than either signal alone
- businesses can tune the balance between exact terms and semantic meaning
- a combined score is easier to reason about in production

### Python Example: Reranking top candidates
```python
def rerank_candidates(candidates):
  return sorted(candidates, key=lambda item: (item["priority"], item["score"]), reverse=True)


top_candidates = [
  {"id": "x", "priority": 2, "score": 0.81},
  {"id": "y", "priority": 1, "score": 0.95},
  {"id": "z", "priority": 3, "score": 0.72},
]

print(rerank_candidates(top_candidates))
```

### Why this example matters
- reranking lets you apply business logic after semantic retrieval
- the top semantic match is not always the best answer
- production systems often use multiple scoring layers

## Tradeoffs and Tuning

### Latency vs Recall
```mermaid
flowchart LR
  A[More aggressive index pruning] --> B[Lower latency]
  A --> C[Lower recall]
  D[More exhaustive search] --> E[Higher recall]
  D --> F[Higher latency]
```

### Storage vs Quality
```mermaid
flowchart LR
  A[Smaller vectors or compression] --> B[Lower memory cost]
  A --> C[Possible quality drop]
  D[Full precision storage] --> E[Better quality]
  D --> F[Higher memory cost]
```

### Retrieval Pipeline Tuning
```mermaid
flowchart TD
  A[Bad result] --> B{Is the query clear?}
  B -->|No| C[Improve prompting or normalization]
  B -->|Yes| D{Are chunks good?}
  D -->|No| E[Re-chunk the source]
  D -->|Yes| F{Is metadata correct?}
  F -->|No| G[Fix filters and labels]
  F -->|Yes| H[Adjust index and reranking]
```

## Production Troubleshooting Checklist

When retrieval quality feels weak, use this checklist:

1. confirm the embedding model matches the collection
2. verify chunk sizes and overlap settings
3. test with and without metadata filters
4. inspect top-k results manually
5. compare brute-force search against ANN search on a sample set
6. check whether the query is too broad or too vague
7. confirm that stale data was re-embedded after updates

This checklist is useful because the bug is often one layer earlier than the symptom.

## Common Production Patterns

### Pattern 1: Two-stage retrieval
First the system retrieves a broad candidate set. Then it reranks those candidates using a stronger model or a more precise filter.

Why it works:

- the first stage is fast
- the second stage improves quality
- the system gets both scale and precision

### Pattern 2: Tenant-isolated indexes
Each customer or workspace gets its own partition or index.

Why it works:

- access control is simpler
- noisy cross-tenant results are reduced
- operational debugging becomes easier

### Pattern 3: Hybrid retrieval
Combine keyword search with vector search.

Why it works:

- exact terms still matter for names, codes, and identifiers
- semantic search handles paraphrases
- the final ranking becomes more robust

## Interview Questions

### Conceptual
- What is the difference between embeddings and a vector database?
- Why do approximate nearest neighbor indexes exist?
- When would you use keyword search instead of vector search?
- Why does metadata design affect retrieval quality?
- What is the biggest risk of blindly trusting retrieved chunks?

### System Design
- Design a semantic search system for internal docs.
- Design a retrieval layer for a support assistant.
- Design a multi-tenant vector database strategy.
- Design a hybrid search architecture for a large enterprise.

### Debugging
- How do you diagnose bad retrieval when the embedding model is known to be good?
- How do you check whether chunking is hurting relevance?
- How do you know whether the index or the data is the real problem?

## Quizzes

### Quiz 1
1. What does a vector database return?
2. Why is cosine similarity common in semantic search?
3. What does metadata filtering improve?
4. Why is brute-force search not enough at scale?

### Quiz 2
1. What is the main tradeoff in ANN search?
2. What is the purpose of HNSW?
3. What is the purpose of IVF?
4. Why does compression matter?

### Quiz 3
1. Why is hybrid search often used in production?
2. Why should you evaluate retrieval separately from generation?
3. What happens if your chunks are too large?
4. What happens if your metadata is inconsistent?

## Expanded Exercises

### Easy
1. Define a vector database in one sentence.
2. Explain why semantic search is useful.
3. Give one example of metadata.
4. Name one vector database alternative.
5. State one reason not to use vector search.

### Medium
6. Draw a diagram showing how a query becomes a vector and then a search result.
7. Compare cosine similarity and Euclidean distance.
8. Explain why ANN search is faster than brute force.
9. Describe how metadata filters improve precision.
10. Explain why re-embedding is necessary after a model upgrade.

### Hard
11. Design a schema for a knowledge base with topic, source, and access level.
12. Compare pgvector, Qdrant, and Pinecone for a startup.
13. Explain how to evaluate retrieval quality using real user queries.
14. Design a reranking layer on top of a vector database.
15. Describe how to support deletion requests in a vector index.

### Challenge
16. Build a hybrid search prototype with keyword and vector ranking.
17. Add observability metrics for latency, cost, and recall.
18. Design a multi-tenant retrieval service.
19. Create a shadow index migration strategy for an embedding model upgrade.
20. Propose a caching plan for repeated search queries.

### Reflection
21. When does vector search feel magical, and when does it feel unreliable?
22. What is the most important design decision in a retrieval system?
23. Which is harder to improve: retrieval quality or generation quality?
24. Why do real products need both embeddings and metadata?
25. What is the first thing you would test if retrieval results looked wrong?

## Cumulative Capstone Update
The capstone should now include a retrieval layer that can support semantic search, source citations, and access-aware filtering.

Add these items to your capstone plan:

- a vector store for course or project knowledge
- metadata for lesson, topic, source, and visibility
- a query endpoint that returns top-k matches
- a filtering strategy for user scope or project scope
- a retrieval evaluation checklist
- logging for query inputs and returned chunks

This turns the capstone from a simple AI demo into a real knowledge application.

## Summary
Vector databases make semantic search fast, scalable, and useful in real products. They store embeddings, search by similarity, and combine vectors with metadata filters so AI systems can retrieve the right information at the right time.

The main lesson of this day is simple:

- embeddings give us meaning
- vector databases give us retrieval
- retrieval gives AI applications the context they need

If Day 15 was about turning text into vectors, Day 16 is about turning vectors into a working search system.

[Previous: Day 15 - Embeddings](../day_15/day_15_embeddings.md) | [Next: Day 17 - RAG](../day_17/day_17_rag.md)

## Further Reading
- https://docs.trychroma.com/
- https://qdrant.tech/documentation/
- https://www.pinecone.io/learn/
- https://weaviate.io/developers/weaviate
- https://github.com/facebookresearch/faiss
- https://www.postgresql.org/docs/current/pgvector.html
