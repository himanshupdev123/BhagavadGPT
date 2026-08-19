#!/usr/bin/env python3
"""
Manual Google Sheets sync trigger.
Uses direct module access instead of HTTP endpoints.
Useful after you edit tags in the Google Sheet.
"""

import sys
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from dotenv import load_dotenv
load_dotenv()

print("=" * 60)
print("Manual Google Sheets Sync Trigger")
print("=" * 60)

# Import the sync module
from google_sheets_sync import GoogleSheetsSync

print("\n📊 Initializing Google Sheets sync...")

try:
    # Create sync instance
    sync = GoogleSheetsSync()
    
    # Check availability (triggers authentication)
    is_available = sync.is_available()
    
    if not is_available:
        print("\n❌ Google Sheets sync not available!")
        print("   Reasons could be:")
        print("   - GOOGLE_SHEET_ID not set in .env")
        print("   - service-account.json not found")
        print("   - Authentication failed")
        sys.exit(1)
    
    print(f"\n✅ Google Sheets sync is available")
    print(f"   Sheet ID: {sync.sheet_id}")
    print(f"   Sync interval: {sync.sync_interval // 60} minutes")
    
    # Perform sync
    print("\n🔄 Triggering manual sync...")
    success = sync.sync()
    
    if success:
        print(f"\n✅ SYNC SUCCESSFUL!")
        print(f"   Last sync timestamp: {sync.last_sync}")
        
        # Show what was synced
        tags_count = 0
        related_count = 0
        
        # Fetch to show stats
        tags_dict = sync.fetch_tags()
        related_dict = sync.fetch_related()
        
        if tags_dict:
            tags_count = len(tags_dict)
        if related_dict:
            related_count = len(related_dict)
            
        print(f"   Tags synced: {tags_count} verses")
        print(f"   Relationships synced: {related_count} verses")
        print("\n   Your changes from Google Sheets are now synced!")
        print("   The running backend will pick them up on next automatic sync.")
            
    else:
        print(f"\n❌ Sync failed!")
        sys.exit(1)
        
except ModuleNotFoundError as e:
    print(f"\n❌ Missing dependencies: {e}")
    print("   Run: pip install -r requirements.txt")
    sys.exit(1)
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "=" * 60)
print("✅ Manual sync completed successfully!")
print("The backend will continue to auto-sync every 30 minutes.")
print("=" * 60)
