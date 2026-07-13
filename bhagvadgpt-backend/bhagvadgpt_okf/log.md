# Change Log

This file tracks the evolution of the Bhagavad Gita OKF knowledge base.

## 2026-07-13

**Enhancement**: OKF v0.1 specification full compliance
- Added frontmatter fields to all 700 verses: created, updated, resource, chapter, verse_number, speaker
- Added Citations section to all verse bodies for attribution
- Resource URIs follow format: `bhagavad-gita://chapter/X/verse/Y`
- Speaker identification: Krishna (most verses), Arjuna (Chapter 1), Sanjaya (narration)
- Backend updated to load and expose new metadata fields

**Enhancement**: Implemented knowledge graph traversal via related field
- Backend now automatically includes related verses in search results
- Added 1-2 related verses per query for richer context
- Related verses marked with "(Related Context)" label
- Context enrichment: 30-50% more verses per query

**Enhancement**: Added OKF v0.1 compliance features
- Created root index.md with bundle overview
- Added this log.md for change tracking
- Created chapter-level index.md files for all 18 chapters
- Enhanced frontmatter with OKF-compliant fields

**Update**: Project cleanup and reorganization
- Organized codebase into docs/, tests/, scripts/ folders
- Created comprehensive README files for each folder
- Moved 40+ files into logical structure
- Cleaned root directory to 6 essential files

**Update**: Enhanced tags for 676 verses with user-query-aligned language
- Added semantic variations (e.g., "anxiety" → "worried", "stressed", "nervous")
- Improved tag coverage from basic themes to user language
- Average tags per verse increased to 11.7
- Tags now better match real user queries from testing

**Update**: Populated related field for 297 verses
- Added 893 total graph connections between verses
- Connections based on complementary themes, progressions, and contrasts
- Related field enables knowledge graph traversal
- Average 1.3 connections per verse

## 2026-07-12

**Creation**: Migrated entire knowledge base from ChromaDB to OKF format
- Converted all 700 verses to markdown files with YAML frontmatter
- Organized into chapter_X/verse_Y.md structure
- Extracted and populated tags from modern_themes field
- 618 verses had initial tags from migration

**Creation**: Established OKF directory structure
- Created 18 chapter directories (chapter_1 through chapter_18)
- Each chapter contains its respective verses as markdown files
- YAML frontmatter includes: type, title, description, tags, related
- Markdown body includes: Sanskrit, Translation, Meaning, Modern Applications

**Implementation**: Built in-memory knowledge graph system
- Created BhagvadOKFGraph class for fast verse retrieval
- Implemented tag-based semantic search
- Average search time: <100ms for 700 verses
- Memory footprint: ~57MB total

**Implementation**: Token optimization for LLM context
- Reduced context from 10 verses to 3 primary verses
- Condensed format: Sanskrit + Translation + 3 lines of Meaning
- Successfully staying under 8000 token limit
- Token usage: typically 500-900 words per query

## 2026-07-11

**Migration**: Prepared for ChromaDB to OKF migration
- Backed up existing ChromaDB vector database
- Extracted all 700 verses from database
- Analyzed verse structure and metadata
- Planned OKF markdown file structure

## Before 2026-07-11

**Legacy**: ChromaDB-based system
- Vector database with 700 verses
- Embedding-based semantic search
- No explicit tag system
- No related field connections
- Limited to similarity search only

---

## Version History

- **v1.0.0** (2026-07-12): Initial OKF migration with 700 verses
- **v1.1.0** (2026-07-13): Enhanced tags and related field connections
- **v1.2.0** (2026-07-13): Knowledge graph traversal implementation
- **v1.3.0** (2026-07-13): OKF v0.1 full specification compliance

---

*For questions about this knowledge base, see the root [index.md](index.md)*
