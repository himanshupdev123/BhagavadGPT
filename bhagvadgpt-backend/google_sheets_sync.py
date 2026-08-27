"""
Google Sheets synchronization module for BhagvadGPT.
Allows collaborative editing of verse tags and relationships through Google Sheets.
"""

import os
import time
from pathlib import Path
from typing import Dict, List, Optional
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class GoogleSheetsSync:
    """
    Synchronize verse tags and relationships from Google Sheets.
    Falls back to local files if Google Sheets is unavailable.
    """
    
    def __init__(self, credentials_path='bhagvadgpt_okf/service-account.json'):
        self.credentials_path = credentials_path
        self.sheet_id = os.getenv('GOOGLE_SHEET_ID')
        self.service = None
        self.last_sync = 0
        self.sync_interval = int(os.getenv('GOOGLE_SHEETS_SYNC_INTERVAL', '3600'))
        self._auth_attempted = False
        
        # Don't authenticate immediately - will authenticate on first use
        if not self.sheet_id:
            print("ℹ️ GOOGLE_SHEET_ID not set. Using local files only.")
        if not os.path.exists(credentials_path):
            print(f"ℹ️ Credentials file not found: {credentials_path}. Using local files only.")
    
    def _authenticate(self):
        """Authenticate with Google Sheets API"""
        try:
            print("🔐 Authenticating with Google Sheets...")
            creds = service_account.Credentials.from_service_account_file(
                self.credentials_path,
                scopes=['https://www.googleapis.com/auth/spreadsheets.readonly']
            )
            # Build service - this might take a few seconds on first run
            self.service = build('sheets', 'v4', credentials=creds, cache_discovery=False)
            print("✅ Google Sheets API connected")
        except Exception as e:
            print(f"⚠️ Google Sheets authentication failed: {e}")
            print("   Falling back to local files only.")
            self.service = None
    
    def is_available(self) -> bool:
        """Check if Google Sheets sync is available"""
        # Lazy authentication on first availability check
        if not self._auth_attempted and self.sheet_id and os.path.exists(self.credentials_path):
            self._authenticate()
            self._auth_attempted = True
        return self.service is not None and self.sheet_id is not None
    
    def should_sync(self) -> bool:
        """Check if enough time has passed to sync again"""
        return (time.time() - self.last_sync) > self.sync_interval
    
    def fetch_tags(self) -> Optional[Dict[str, List[str]]]:
        """
        Fetch tags from Google Sheets 'Tags' tab.
        
        Returns:
            Dictionary mapping verse references to lists of tags.
            Format: {"chapter_2/verse_47": ["anxiety", "fear", ...]}
            Returns None if fetch fails.
        """
        if not self.is_available():
            return None
        
        try:
            sheet = self.service.spreadsheets()
            result = sheet.values().get(
                spreadsheetId=self.sheet_id,
                range='Tags!A2:AY1000',  # Skip header, get up to 1000 rows, 50 tag columns
                valueRenderOption='FORMATTED_VALUE'
            ).execute()
            
            rows = result.get('values', [])
            tags_dict = {}
            
            for row in rows:
                if not row or not row[0].strip():  # Skip empty rows
                    continue
                
                verse_ref = row[0].strip()  # e.g., "2.47"
                
                # Validate format
                if '.' not in verse_ref:
                    print(f"⚠️ Invalid verse format in sheet: {verse_ref}")
                    continue
                
                try:
                    chapter, verse = verse_ref.split('.')
                    full_ref = f"chapter_{chapter}/verse_{verse}"
                    
                    # Extract tags from columns B through AY (indices 1-50)
                    tags = []
                    if len(row) > 1:
                        tags = [tag.strip() for tag in row[1:51] if tag.strip()]
                    
                    # Always add to dict, even if tags are empty (to clear them)
                    tags_dict[full_ref] = tags
                
                except ValueError:
                    print(f"⚠️ Could not parse verse reference: {verse_ref}")
                    continue
            
            print(f"📥 Fetched tags for {len(tags_dict)} verses from Google Sheets")
            return tags_dict
            
        except HttpError as e:
            print(f"❌ HTTP error fetching tags from Google Sheets: {e}")
            return None
        except Exception as e:
            print(f"❌ Error fetching tags from Google Sheets: {e}")
            return None
    
    def fetch_related(self) -> Optional[Dict[str, List[str]]]:
        """
        Fetch related verses from Google Sheets 'Related' tab.
        
        Returns:
            Dictionary mapping verse references to lists of related verses.
            Format: {"chapter_2/verse_47": ["chapter_2/verse_38", ...]}
            Returns None if fetch fails.
        """
        if not self.is_available():
            return None
        
        try:
            sheet = self.service.spreadsheets()
            result = sheet.values().get(
                spreadsheetId=self.sheet_id,
                range='Related!A2:F1000',  # Skip header row, get verse + 5 related columns
                valueRenderOption='FORMATTED_VALUE'
            ).execute()
            
            rows = result.get('values', [])
            related_dict = {}
            
            for row in rows:
                if not row or not row[0].strip():  # Skip empty rows
                    continue
                
                verse_ref = row[0].strip()  # e.g., "2.47"
                
                # Validate format
                if '.' not in verse_ref:
                    continue
                
                try:
                    chapter, verse = verse_ref.split('.')
                    full_ref = f"chapter_{chapter}/verse_{verse}"
                    
                    # Extract related verse refs from columns B through F (indices 1-5)
                    related_refs = []
                    if len(row) > 1:
                        for rel_ref in row[1:6]:
                            rel_ref = rel_ref.strip()
                            if not rel_ref or '.' not in rel_ref:
                                continue
                            
                            rel_chapter, rel_verse = rel_ref.split('.')
                            full_rel_ref = f"chapter_{rel_chapter}/verse_{rel_verse}"
                            related_refs.append(full_rel_ref)
                    
                    # Always add to dict, even if empty (to clear them)
                    related_dict[full_ref] = related_refs
                
                except ValueError:
                    print(f"⚠️ Could not parse verse reference: {verse_ref}")
                    continue
            
            print(f"📥 Fetched relationships for {len(related_dict)} verses from Google Sheets")
            return related_dict
            
        except HttpError as e:
            print(f"❌ HTTP error fetching related verses: {e}")
            return None
        except Exception as e:
            print(f"❌ Error fetching related verses: {e}")
            return None
    
    def fetch_priority_index(self) -> Optional[Dict[str, List[str]]]:
        """
        Fetch priority index from Google Sheets 'PriorityIndex' tab.
        
        Returns:
            Dictionary mapping tag names to ordered lists of verse references.
            Format: {"anger": ["chapter_2/verse_63", "chapter_3/verse_37", ...]}
            Returns None if fetch fails.
        """
        if not self.is_available():
            return None
        
        try:
            sheet = self.service.spreadsheets()
            result = sheet.values().get(
                spreadsheetId=self.sheet_id,
                range='PriorityIndex!A2:P200',  # Tag col + up to 15 priority verse cols
                valueRenderOption='FORMATTED_VALUE'
            ).execute()
            
            rows = result.get('values', [])
            priority_index = {}
            
            for row in rows:
                if not row or not row[0].strip():
                    continue
                
                # Strip trailing colon from tag name (e.g., "anger:" → "anger")
                tag = row[0].strip().rstrip(':').strip().lower()
                if not tag:
                    continue
                
                # Extract verse refs from columns B onward
                verse_refs = []
                for cell in row[1:]:
                    cell = cell.strip()
                    if not cell:
                        continue
                    # Parse "2.47" → "chapter_2/verse_47"
                    if '.' in cell:
                        try:
                            parts = cell.split('.')
                            chapter = parts[0].strip()
                            verse = parts[1].strip()
                            verse_refs.append(f"chapter_{chapter}/verse_{verse}")
                        except (ValueError, IndexError):
                            print(f"⚠️ Could not parse verse ref in PriorityIndex: {cell}")
                
                if verse_refs:
                    priority_index[tag] = verse_refs
            
            print(f"📥 Fetched priority index for {len(priority_index)} tags from Google Sheets")
            return priority_index
            
        except HttpError as e:
            print(f"❌ HTTP error fetching priority index: {e}")
            return None
        except Exception as e:
            print(f"❌ Error fetching priority index: {e}")
            return None

    def sync(self) -> bool:
        """
        Perform a full sync from Google Sheets.
        
        Returns:
            True if sync was successful, False otherwise.
        """
        if not self.is_available():
            return False
        
        print("🔄 Syncing from Google Sheets...")
        
        tags_dict = self.fetch_tags()
        related_dict = self.fetch_related()
        
        self.last_sync = time.time()
        
        # Return True if at least one fetch succeeded
        return tags_dict is not None or related_dict is not None


# Singleton instance
_sync_instance: Optional[GoogleSheetsSync] = None


def get_sync_instance() -> GoogleSheetsSync:
    """Get or create the singleton GoogleSheetsSync instance"""
    global _sync_instance
    if _sync_instance is None:
        _sync_instance = GoogleSheetsSync()
    return _sync_instance
