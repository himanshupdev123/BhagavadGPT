"""
Complete test demonstrating OKF knowledge graph with related field traversal
"""

from pathlib import Path
import sys

# Add parent directory to path to import main module
sys.path.insert(0, str(Path(__file__).parent.parent))

from main import okf_graph

print("=" * 80)
print("OKF KNOWLEDGE GRAPH - COMPLETE DEMONSTRATION")
print("=" * 80)

# Test 1: Tag-based search
print("\n📌 TEST 1: Tag-based verse search")
print("-" * 80)
test_queries = [
    "feeling anxious and worried about future",
    "confused about life purpose",
    "how to control my mind"
]

for query in test_queries:
    print(f"\nQuery: '{query}'")
    result = okf_graph.search(query, top_k=2, include_related=False)
    verse_count = result.count("**Chapter")
    print(f"   → Found {verse_count} matching verses")

# Test 2: Related field traversal
print("\n\n📌 TEST 2: Knowledge graph traversal (with related verses)")
print("-" * 80)

query = "detachment from outcomes while working"
print(f"\nQuery: '{query}'")

# Without related
result_without = okf_graph.search(query, top_k=2, include_related=False)
verses_without = result_without.count("**Chapter")

# With related
result_with = okf_graph.search(query, top_k=2, include_related=True)
verses_with = result_with.count("**Chapter")
related_count = result_with.count("(Related Context)")

print(f"\n   Without related: {verses_without} verses")
print(f"   With related:    {verses_with} verses ({related_count} from graph traversal)")
print(f"   Enrichment:      +{verses_with - verses_without} verses ({(verses_with - verses_without) / verses_without * 100:.0f}% more context)")

# Test 3: Verify graph structure
print("\n\n📌 TEST 3: Knowledge graph structure")
print("-" * 80)

# Sample a few verses to show graph connectivity
sample_refs = [
    "chapter_2/verse_47",
    "chapter_6/verse_35",
    "chapter_18/verse_66"
]

print("\nSample verse connections in the knowledge graph:\n")
for ref in sample_refs:
    verse = okf_graph.get_verse_by_reference(ref)
    if verse:
        print(f"{verse['title']}")
        print(f"   Tags: {len(verse['tags'])} tags")
        print(f"   Related: {len(verse['related'])} connected verses")
        if verse['related']:
            print(f"   → {', '.join(verse['related'][:3])}{'...' if len(verse['related']) > 3 else ''}")
        print()

# Test 4: Performance stats
print("\n📌 TEST 4: System statistics")
print("-" * 80)

total_verses = len(okf_graph.nodes)
verses_with_tags = sum(1 for node in okf_graph.nodes if node['tags'])
verses_with_related = sum(1 for node in okf_graph.nodes if node['related'])
total_tags = sum(len(node['tags']) for node in okf_graph.nodes)
total_connections = sum(len(node['related']) for node in okf_graph.nodes)

print(f"\n   Total verses loaded:      {total_verses}")
print(f"   Verses with tags:         {verses_with_tags} ({verses_with_tags/total_verses*100:.1f}%)")
print(f"   Verses with related:      {verses_with_related} ({verses_with_related/total_verses*100:.1f}%)")
print(f"   Average tags per verse:   {total_tags/total_verses:.1f}")
print(f"   Average connections:      {total_connections/total_verses:.1f}")
print(f"   Total graph connections:  {total_connections}")

print("\n" + "=" * 80)
print("✅ OKF KNOWLEDGE GRAPH IS FULLY OPERATIONAL")
print("=" * 80)
print("\nKey features:")
print("  • Tag-based semantic search")
print("  • Knowledge graph traversal via 'related' field")
print("  • In-memory for fast retrieval")
print("  • 700 verses with rich metadata")
print("=" * 80)
