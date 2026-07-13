# OKF Knowledge Graph - Related Field Traversal

## Overview

The BhagvadGPT backend now implements **knowledge graph traversal** using the `related` field in OKF (Open Knowledge Format) verse files. This feature automatically enriches search results by including contextually connected verses that complement the primary matches.

## How It Works

### 1. Tag-Based Primary Search
When a user asks a question, the system first performs tag-based search to find verses that match the query's keywords and themes.

```
User Query: "feeling anxious about work results"
        ↓
Tag Matching: ["anxiety", "worried", "work", "results"]
        ↓
Primary Matches: 
  - Chapter 2, Verse 47 (score: 12)
  - Chapter 3, Verse 19 (score: 8)
```

### 2. Knowledge Graph Traversal
For each primary match, the system reads the `related` field and fetches 1 additional verse that provides complementary wisdom.

```
Primary: Chapter 2, Verse 47
         ↓
Related Field: [chapter_2/verse_38, chapter_2/verse_37, ...]
         ↓
Fetch: Chapter 2, Verse 38 (Related Context)
```

### 3. Enriched Context
The final response includes both primary matches AND related verses, providing:
- **Direct answers** (primary matches)
- **Supporting context** (related verses)
- **Deeper understanding** (graph traversal)

## Implementation

### Data Structure

Each OKF verse file includes a `related` field in the YAML frontmatter:

```yaml
---
type: shloka
title: Chapter 2, Verse 47
tags:
- anxiety about results
- detachment from outcomes
- karma
related:
- chapter_2/verse_38
- chapter_2/verse_37
- chapter_2/verse_39
- chapter_2/verse_48
- chapter_2/verse_50
---
```

### Code Architecture

The `BhagvadOKFGraph` class handles both search and traversal:

```python
class BhagvadOKFGraph:
    def __init__(self, okf_dir="bhagvadgpt_okf"):
        self.nodes = []           # All 700 verses
        self.verse_index = {}     # Quick lookup by reference
        
    def search(self, query, top_k=3, include_related=True):
        # 1. Find primary matches by tag scoring
        # 2. For each primary match, fetch 1 related verse
        # 3. Return combined context (condensed for token limits)
```

### Search Method Flow

```
search(query, top_k=3, include_related=True)
    │
    ├─> Score all verses by tag matches
    │
    ├─> Select top_k primary matches
    │
    ├─> IF include_related:
    │   └─> For each primary match:
    │       └─> Read related field
    │       └─> Fetch 1 related verse via verse_index
    │       └─> Mark as "(Related Context)"
    │
    └─> Format all verses (condensed)
        └─> Return context string
```

## Benefits

### 1. Richer Answers
- Primary matches directly address the question
- Related verses provide supporting wisdom
- Users get multi-dimensional understanding

### 2. Better Token Efficiency
- Related verses use condensed format (2 lines of meaning vs 3)
- Only 1 related verse per primary match
- Total context stays under 8000 token limit

### 3. Knowledge Discovery
- Users discover verses they didn't explicitly search for
- Graph connections reveal thematic relationships
- Enables serendipitous learning

## Performance

Current system statistics:
- **700 verses** loaded in memory
- **676 verses** (96.6%) have tags
- **297 verses** (42.4%) have related connections
- **893 total connections** in the graph
- **11.7 average tags** per verse
- **1.3 average connections** per verse

## Example

### Query: "anxiety about results"

**Without Related Verses:**
```
Chapter 2, Verse 47
Chapter 3, Verse 19
Total: 2 verses
```

**With Related Verses (Graph Traversal):**
```
Chapter 2, Verse 47
Chapter 3, Verse 19
Chapter 2, Verse 38 (Related Context)
Chapter 3, Verse 7 (Related Context)
Total: 4 verses (50% more context)
```

## Token Management

To stay under the 8000 token limit:
1. Primary verses: Full Sanskrit + Translation + 3 lines of Meaning
2. Related verses: Full Sanskrit + Translation + 2 lines of Meaning
3. Maximum: 3 primary + 3 related = 6 total verses
4. Typical: 2 primary + 1-2 related = 3-4 total verses

## Testing

Run the test suite to verify functionality:

```bash
# Test related field traversal
python test_related_traversal.py

# Detailed traversal demonstration
python test_related_detailed.py

# Complete system test
python test_okf_complete.py
```

## Future Enhancements

Potential improvements:
1. **Multi-hop traversal**: Follow related→related connections
2. **Weighted relationships**: Different types of connections (complementary, contrasting, progressive)
3. **User preferences**: Allow users to request more/fewer related verses
4. **Dynamic selection**: Choose which related verse based on query context
5. **Bidirectional links**: Automatic reverse connections

## Related Documentation

- [OKF Format Specification](./OKF_FORMAT.md)
- [Tag Enhancement Guide](./TAG_ENHANCEMENT.md)
- [Token Limit Management](./TOKEN_LIMIT_FIX.md)
