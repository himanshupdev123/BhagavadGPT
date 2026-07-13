# Knowledge Graph Traversal - Visual Flow

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    BhagvadGPT Backend                           │
│                                                                 │
│  ┌───────────────────────────────────────────────────────┐    │
│  │           BhagvadOKFGraph (In-Memory)                 │    │
│  │                                                        │    │
│  │  ┌──────────────┐      ┌──────────────┐             │    │
│  │  │   nodes[]    │      │ verse_index  │             │    │
│  │  │              │      │              │             │    │
│  │  │  700 verses  │◄────►│  Fast lookup │             │    │
│  │  │              │      │  by reference│             │    │
│  │  └──────────────┘      └──────────────┘             │    │
│  │                                                        │    │
│  │  Each node contains:                                  │    │
│  │  • id: "verse_47"                                     │    │
│  │  • chapter: "chapter_2"                               │    │
│  │  • reference: "chapter_2/verse_47"                    │    │
│  │  • title: "Chapter 2, Verse 47"                       │    │
│  │  • tags: ["anxiety", "detachment", ...]               │    │
│  │  • related: ["chapter_2/verse_38", ...]               │    │
│  │  • content: Full markdown text                        │    │
│  └───────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
```

## Search Flow with Graph Traversal

```
User Query: "feeling anxious about work results"
    │
    ▼
┌─────────────────────────────────────────────────────────┐
│ STEP 1: Extract Query Terms                            │
│                                                         │
│ Terms: ["feeling", "anxious", "work", "results"]       │
└─────────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────────┐
│ STEP 2: Score All 700 Verses by Tag Matching           │
│                                                         │
│ Chapter 2, Verse 47:  Score 15 ✓                       │
│   Tags: ["anxiety about results", "worried", ...]      │
│                                                         │
│ Chapter 2, Verse 49:  Score 12 ✓                       │
│   Tags: ["anxiety", "mental peace", ...]               │
│                                                         │
│ Chapter 6, Verse 35:  Score 8 ✓                        │
│   Tags: ["mind control", "restless", ...]              │
│                                                         │
│ Chapter 3, Verse 19:  Score 5                          │
│ ...                                                     │
└─────────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────────┐
│ STEP 3: Select Top K Primary Matches (K=2)             │
│                                                         │
│ PRIMARY:                                                │
│ 1. Chapter 2, Verse 47 (score: 15)                     │
│ 2. Chapter 2, Verse 49 (score: 12)                     │
└─────────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────────┐
│ STEP 4: Knowledge Graph Traversal                      │
│         (if include_related=True)                       │
│                                                         │
│ For Verse 47:                                           │
│   related: ["chapter_2/verse_38", ...]                 │
│   ↓                                                     │
│   Fetch: chapter_2/verse_38 via verse_index            │
│   Add: Chapter 2, Verse 38 (Related Context) ⚡        │
│                                                         │
│ For Verse 49:                                           │
│   related: ["chapter_12/verse_6", ...]                 │
│   ↓                                                     │
│   Fetch: chapter_12/verse_6 via verse_index            │
│   Add: Chapter 12, Verse 6 (Related Context) ⚡        │
└─────────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────────┐
│ STEP 5: Format Context (Token-Efficient)               │
│                                                         │
│ PRIMARY VERSES (full content):                          │
│ • Sanskrit + Translation + 3 lines of Meaning          │
│                                                         │
│ RELATED VERSES (condensed):                             │
│ • Sanskrit + Translation + 2 lines of Meaning          │
│ • Marked with "(Related Context)" label                │
└─────────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────────┐
│ STEP 6: Return Combined Context                        │
│                                                         │
│ Total: 4 verses                                         │
│ • 2 primary (direct matches)                            │
│ • 2 related (graph traversal)                           │
│                                                         │
│ Size: ~5KB (~750 words)                                 │
│ Status: Under 8000 token limit ✓                       │
└─────────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────────┐
│ STEP 7: Send to LLM for Final Response                 │
│                                                         │
│ Prompt Template:                                        │
│   Context: [4 verses with full content]                │
│   Question: [user query]                                │
│   Username: [user name]                                 │
│                                                         │
│ LLM generates personalized, compassionate response      │
└─────────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────────┐
│ STEP 8: Stream Response to User                        │
│                                                         │
│ "Namaste! To your situation these shlokas from the     │
│  Gita are the best answers:                            │
│                                                         │
│  **Chapter 2, Verse 47**                               │
│  [Sanskrit]                                             │
│  [Translation]                                          │
│  How this connects to your situation:                  │
│  [Personalized wisdom addressing anxiety about work]   │
│  ..."                                                   │
└─────────────────────────────────────────────────────────┘
```

## Graph Connectivity Example

```
Chapter 2, Verse 47
"You have the right to perform your actions..."

├─ related[0] → Chapter 2, Verse 38
│               "Treat success and failure equally..."
│               (Complements: Same theme, different angle)
│
├─ related[1] → Chapter 2, Verse 37
│               "If you die in battle..."
│               (Progression: Action despite uncertainty)
│
├─ related[2] → Chapter 2, Verse 39
│               "This is wisdom about action..."
│               (Foundation: Introduction to karma yoga)
│
├─ related[3] → Chapter 2, Verse 48
│               "Perform your duty with evenness of mind..."
│               (Extension: Practical application)
│
└─ related[4] → Chapter 2, Verse 50
                "A person united in wisdom..."
                (Result: Benefits of detached action)
```

## Data Flow Diagram

```
┌─────────────┐
│  OKF Files  │
│  (700 .md)  │
└──────┬──────┘
       │ Load at startup
       ▼
┌──────────────────────────┐
│  Parse YAML Frontmatter  │
│  • tags                  │
│  • related               │
│  • title                 │
└──────┬───────────────────┘
       │ Store in memory
       ▼
┌──────────────────────────┐
│   nodes[] (700 items)    │
│   verse_index{} (dict)   │
└──────┬───────────────────┘
       │ Ready for search
       ▼
┌──────────────────────────┐
│  User Query              │
└──────┬───────────────────┘
       │
       ▼
┌──────────────────────────┐
│  search(query,           │
│         top_k=3,          │
│         include_related=  │
│         True)             │
└──────┬───────────────────┘
       │
       ├─→ Tag-based scoring
       │
       ├─→ Select top K
       │
       ├─→ For each top match:
       │   ├─→ Read related field
       │   └─→ Fetch via verse_index
       │
       └─→ Format context
           │
           ▼
       ┌─────────────────────┐
       │  Context String     │
       │  (4-6 verses)       │
       └────┬────────────────┘
            │
            ▼
       ┌─────────────────────┐
       │  LLM Response       │
       └─────────────────────┘
```

## Token Budget Management

```
Token Limit: 8000 tokens
─────────────────────────────────────────────────

Prompt Template:    ~2000 tokens
System Instructions (~1500 tokens)
User Query         (~100 tokens)
Formatting         (~400 tokens)

Verse Content:      ~4000 tokens (max)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Per PRIMARY Verse:  ~800 tokens
  • Sanskrit        ~150 tokens
  • Translation     ~150 tokens
  • Meaning (3 ln)  ~500 tokens

Per RELATED Verse:  ~600 tokens
  • Sanskrit        ~150 tokens
  • Translation     ~150 tokens
  • Meaning (2 ln)  ~300 tokens

Example Configuration:
  2 primary × 800  = 1600 tokens
  2 related × 600  = 1200 tokens
  ────────────────────────────────
  Total verse data = 2800 tokens

Total Request:      ~6800 tokens ✓
Buffer:             ~1200 tokens
```

## Performance Metrics

```
┌────────────────────────────────────────┐
│         Operation          │   Time    │
├────────────────────────────┼───────────┤
│ Load 700 verses            │  1-2 sec  │
│ Tag-based search           │  <50 ms   │
│ Graph traversal (1 hop)    │  <50 ms   │
│ Format context             │  <20 ms   │
│ ────────────────────────────────────── │
│ Total search operation     │  <120 ms  │
└────────────────────────────────────────┘

┌────────────────────────────────────────┐
│         Memory Usage       │   Size    │
├────────────────────────────┼───────────┤
│ All verses in memory       │  ~50 MB   │
│ verse_index dict           │  ~5 MB    │
│ Tags                       │  ~2 MB    │
│ ────────────────────────────────────── │
│ Total memory footprint     │  ~57 MB   │
└────────────────────────────────────────┘
```

## Comparison: With vs Without Related Field

```
WITHOUT RELATED FIELD:
─────────────────────────────────────
Query: "How to overcome fear?"

Results:
1. Chapter 14, Verse 20 (Primary)
2. Chapter 18, Verse 4 (Primary)

Total: 2 verses
Context: Basic, direct answers only
─────────────────────────────────────


WITH RELATED FIELD:
─────────────────────────────────────
Query: "How to overcome fear?"

Results:
1. Chapter 14, Verse 20 (Primary)
2. Chapter 18, Verse 4 (Primary)
3. Chapter 13, Verse 13 (Related) ⚡
4. Chapter 5, Verse 23 (Related) ⚡

Total: 4 verses
Context: Rich, multi-dimensional wisdom
Enrichment: +100% more context
─────────────────────────────────────
```

## Key Advantages

```
✓ Richer Context
  └─> Users get complementary wisdom

✓ Knowledge Discovery
  └─> Find verses they didn't search for

✓ Graph-Based Learning
  └─> Leverages human-curated connections

✓ Token Efficient
  └─> Related verses use condensed format

✓ Fast Performance
  └─> In-memory lookup <100ms

✓ Scalable
  └─> Can add more connections over time
```

---

**Visual representations help understand the complex flow of tag-based search combined with knowledge graph traversal.**
