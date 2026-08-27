"""Test how many verses search_by_priority_index actually returns"""
from dotenv import load_dotenv
import os, sys
load_dotenv()

# Simulate what the backend does
sys.path.insert(0, '.')
from main import okf_graph

tag = 'loneliness'
print(f"\nPriority index for '{tag}':")
if tag in okf_graph.priority_index:
    refs = okf_graph.priority_index[tag]
    print(f"  Stored refs: {len(refs)} -> {refs}")
else:
    print("  NOT in priority index!")

print(f"\nTesting search_by_priority_index with top_k=10:")
nodes = okf_graph.search_by_priority_index([tag], top_k=10)
print(f"  Returned {len(nodes)} nodes")
for n in nodes:
    print(f"    {n['reference']}")
