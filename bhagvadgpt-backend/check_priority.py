from dotenv import load_dotenv
load_dotenv()
from google_sheets_sync import GoogleSheetsSync

sync = GoogleSheetsSync()
if sync.is_available():
    pi = sync.fetch_priority_index()
    if pi:
        print(f"Total tags in priority index: {len(pi)}")
        for tag, verses in pi.items():
            if len(verses) >= 3:
                print(f"  {tag}: {len(verses)} shlokas -> {verses[:5]}")
    else:
        print("No priority index data returned")
else:
    print("Sync not available")
