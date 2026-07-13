"""
Detailed test to show related field traversal in action
"""

from pathlib import Path
import sys

# Add parent directory to path to import main module
sys.path.insert(0, str(Path(__file__).parent.parent))

from main import okf_graph

print("=" * 70)
print("TESTING RELATED FIELD KNOWLEDGE GRAPH TRAVERSAL")
print("=" * 70)

# Test query about detachment/karma (should match verse 2.47)
test_query = "anxiety about results detachment karma work"
print(f"\nQuery: '{test_query}'")
print("(This query contains words that should match verse 2.47)\n")

# Search with related verses
result = okf_graph.search(test_query, top_k=2, include_related=True)

# Parse and display results
print("=" * 70)
print("SEARCH RESULTS:")
print("=" * 70)

sections = result.split("---")
for i, section in enumerate(sections, 1):
    if section.strip():
        lines = section.strip().split('\n')
        title_line = lines[0] if lines else ""
        
        print(f"\n{i}. {title_line}")
        
        # Show a snippet of the content
        if len(lines) > 5:
            print("   " + '\n   '.join(lines[1:4]))
        
        # Check if this is a related verse
        if "(Related Context)" in title_line:
            print("   ⚡ This verse was added via knowledge graph traversal!")

print("\n" + "=" * 70)

# Now let's verify the related field of verse 2.47
print("\nVERIFYING RELATED FIELD OF VERSE 2.47:")
print("=" * 70)

verse_2_47 = okf_graph.get_verse_by_reference("chapter_2/verse_47")
if verse_2_47:
    print(f"\nTitle: {verse_2_47['title']}")
    print(f"Related verses: {verse_2_47['related']}")
    
    print("\n\nChecking if related verses exist:")
    for ref in verse_2_47['related']:
        related_verse = okf_graph.get_verse_by_reference(ref)
        if related_verse:
            print(f"  ✅ {ref} → {related_verse['title']}")
        else:
            print(f"  ❌ {ref} → NOT FOUND")

print("\n" + "=" * 70)
print("CONCLUSION:")
print("=" * 70)
print("The related field allows the system to automatically include")
print("contextually connected verses that complement the primary matches.")
print("This creates a richer, more comprehensive answer from the Gita.")
print("=" * 70)
