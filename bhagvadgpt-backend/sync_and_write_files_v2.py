"""
Sync from Google Sheets and write changes to markdown files - COMBINED UPDATE
"""
import os
from dotenv import load_dotenv
import yaml
from pathlib import Path
from datetime import datetime
from google_sheets_sync import GoogleSheetsSync

# Load environment variables
load_dotenv()

# Initialize sync
sync = GoogleSheetsSync()

if not sync.is_available():
    print("❌ Google Sheets sync not available")
    exit(1)

print("✅ Google Sheets sync is available")
print(f"   Sheet ID: {sync.sheet_id}\n")

# Fetch data
print("📥 Fetching data from Google Sheets...")
tags_dict = sync.fetch_tags()
related_dict = sync.fetch_related()

print(f"   Tags: {len(tags_dict) if tags_dict else 0} verses")
print(f"   Relationships: {len(related_dict) if related_dict else 0} verses\n")

# Combine updates - build a map of all verses that need updating
updates_map = {}

if tags_dict:
    for verse_ref, tags in tags_dict.items():
        if verse_ref not in updates_map:
            updates_map[verse_ref] = {}
        updates_map[verse_ref]['tags'] = tags

if related_dict:
    for verse_ref, related in related_dict.items():
        if verse_ref not in updates_map:
            updates_map[verse_ref] = {}
        updates_map[verse_ref]['related'] = related

# Update files once per verse
knowledge_base_dir = Path("bhagvadgpt_okf")
files_updated = 0

print("📝 Updating markdown files...")
today = datetime.now().strftime('%Y-%m-%d')

for verse_ref, updates in updates_map.items():
    verse_path = knowledge_base_dir / f"{verse_ref}.md"
    if not verse_path.exists():
        print(f"⚠️ File not found: {verse_path}")
        continue
    
    try:
        # Read file
        with open(verse_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Parse frontmatter
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                frontmatter = parts[1]
                body = parts[2]
                
                # Update frontmatter
                fm_data = yaml.safe_load(frontmatter)
                
                # Apply all updates for this verse
                if 'tags' in updates:
                    fm_data['tags'] = updates['tags']
                if 'related' in updates:
                    fm_data['related'] = updates['related']
                
                # Update timestamp
                fm_data['updated'] = today
                
                # Write back
                new_frontmatter = yaml.dump(fm_data, default_flow_style=False, allow_unicode=True, sort_keys=False)
                new_content = f"---\n{new_frontmatter}---{body}"
                
                with open(verse_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                
                files_updated += 1
                
                # Show progress for specific verses
                if verse_ref in ['chapter_2/verse_5', 'chapter_1/verse_1']:
                    print(f"   ✓ Updated {verse_ref}")
    except Exception as e:
        print(f"⚠️ Error updating {verse_path}: {e}")

print(f"\n✅ Sync complete!")
print(f"   {files_updated} markdown files updated")
print(f"   Updated timestamp: {today}")
print(f"\n💾 All changes have been written to markdown files")
