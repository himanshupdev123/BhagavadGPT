"""
Test script to verify related field traversal in OKF knowledge graph
"""

from pathlib import Path
import yaml
import sys

# Add parent directory to path to import main module
sys.path.insert(0, str(Path(__file__).parent.parent))

# Load a sample verse to check the structure
sample_file = Path("bhagvadgpt_okf/chapter_2/verse_47.md")

with open(sample_file, "r", encoding="utf-8") as f:
    content = f.read()
    
if content.startswith("---"):
    parts = content.split("---", 2)
    if len(parts) >= 3:
        frontmatter = yaml.safe_load(parts[1])
        
        print("=" * 60)
        print("SAMPLE VERSE STRUCTURE")
        print("=" * 60)
        print(f"\nTitle: {frontmatter.get('title')}")
        print(f"\nTags ({len(frontmatter.get('tags', []))}): {frontmatter.get('tags', [])[:5]}...")
        print(f"\nRelated verses ({len(frontmatter.get('related', []))}): {frontmatter.get('related', [])}")
        
        # Now test the search with include_related
        print("\n" + "=" * 60)
        print("TESTING SEARCH WITH RELATED VERSES")
        print("=" * 60)
        
        # Import the class
        import sys
        sys.path.insert(0, str(Path(__file__).parent.parent))
        from main import okf_graph
        
        # Test query about fear/anxiety (should match verse 2.47)
        test_query = "how to overcome fear of failure"
        print(f"\nQuery: '{test_query}'")
        print("\n" + "-" * 60)
        
        # Test without related verses
        print("\n1. WITHOUT related verses:")
        result_without = okf_graph.search(test_query, top_k=2, include_related=False)
        verses_without = result_without.count("**Chapter")
        print(f"   Total verses returned: {verses_without}")
        
        # Test with related verses
        print("\n2. WITH related verses (knowledge graph traversal):")
        result_with = okf_graph.search(test_query, top_k=2, include_related=True)
        verses_with = result_with.count("**Chapter")
        related_count = result_with.count("(Related Context)")
        print(f"   Total verses returned: {verses_with}")
        print(f"   Related verses: {related_count}")
        
        # Show which verses were included
        print("\n" + "-" * 60)
        print("VERSES INCLUDED (with related):")
        print("-" * 60)
        lines = result_with.split('\n')
        for line in lines:
            if line.startswith("**Chapter"):
                print(f"   • {line}")
        
        print("\n" + "=" * 60)
        if related_count > 0:
            print("✅ SUCCESS: Related field traversal is working!")
        else:
            print("⚠️ WARNING: No related verses were included")
        print("=" * 60)
