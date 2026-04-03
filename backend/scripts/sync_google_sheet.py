"""
Automated Google Sheets to CSV Sync Script
===========================================

Downloads Google Sheets data as CSV at scheduled intervals.
Maintains both timestamped backups and current version.

Usage:
    python sync_google_sheet.py [--backup-only]

Author: Career Recommender System
Date: February 2026
"""

import gspread
from google.oauth2.service_account import Credentials
from pathlib import Path
from datetime import datetime
import csv
import shutil
import argparse
import sys

# Configuration
CREDENTIALS_PATH = Path(__file__).parent.parent / "credentials" / "service-account-credentials.json"
SPREADSHEET_ID = "1tT91nRZYuYtJ6EWUa51q1OuzyUPHpox4QVb8TMqa-r0"
WORKSHEET_NAME = "Form Responses 1"

# Output paths
DATA_DIR = Path(__file__).parent.parent.parent / "student-football-analysis" / "data"
BACKUP_DIR = DATA_DIR / "backups"

# Output filenames
CURRENT_FILENAME = "Student Sports Career Pathway Questionnaire (Responses) - Form Responses 1.csv"


def setup_directories():
    """Create necessary directories if they don't exist"""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    print(f"✅ Directories ready:")
    print(f"   Data: {DATA_DIR}")
    print(f"   Backups: {BACKUP_DIR}")


def authenticate_google_sheets():
    """Authenticate with Google Sheets API using service account"""
    try:
        credentials = Credentials.from_service_account_file(
            str(CREDENTIALS_PATH),
            scopes=['https://www.googleapis.com/auth/spreadsheets.readonly']
        )
        client = gspread.authorize(credentials)
        print(f"✅ Authenticated with Google Sheets API")
        return client
    except FileNotFoundError:
        print(f"❌ Error: Credentials file not found at {CREDENTIALS_PATH}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Authentication error: {e}")
        sys.exit(1)


def download_sheet_as_csv(client, output_path):
    """
    Download Google Sheet data as CSV
    
    Args:
        client: Authenticated gspread client
        output_path: Path object for where to save CSV
        
    Returns:
        int: Number of rows downloaded
    """
    try:
        # Open spreadsheet and worksheet
        spreadsheet = client.open_by_key(SPREADSHEET_ID)
        worksheet = spreadsheet.worksheet(WORKSHEET_NAME)
        
        # Get all values
        all_values = worksheet.get_all_values()
        
        if not all_values:
            print("⚠️  Warning: Worksheet is empty")
            return 0
        
        # Write to CSV
        with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(all_values)
        
        num_rows = len(all_values)
        print(f"✅ Downloaded {num_rows} rows from Google Sheets")
        return num_rows
        
    except gspread.exceptions.WorksheetNotFound:
        print(f"❌ Error: Worksheet '{WORKSHEET_NAME}' not found")
        sys.exit(1)
    except gspread.exceptions.SpreadsheetNotFound:
        print(f"❌ Error: Spreadsheet with ID '{SPREADSHEET_ID}' not found")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Download error: {e}")
        sys.exit(1)


def create_timestamped_backup(source_path):
    """
    Create timestamped backup of CSV file
    
    Args:
        source_path: Path to source CSV file
        
    Returns:
        Path: Path to backup file
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_filename = f"questionnaire_responses_backup_{timestamp}.csv"
    backup_path = BACKUP_DIR / backup_filename
    
    shutil.copy2(source_path, backup_path)
    print(f"✅ Backup created: {backup_filename}")
    return backup_path


def cleanup_old_backups(keep_count=10):
    """
    Keep only the most recent N backups
    
    Args:
        keep_count: Number of recent backups to keep
    """
    backup_files = sorted(
        BACKUP_DIR.glob("questionnaire_responses_backup_*.csv"),
        key=lambda p: p.stat().st_mtime,
        reverse=True
    )
    
    if len(backup_files) > keep_count:
        for old_backup in backup_files[keep_count:]:
            old_backup.unlink()
            print(f"🗑️  Deleted old backup: {old_backup.name}")
        
        print(f"✅ Kept {keep_count} most recent backups")


def get_file_stats(filepath):
    """Get file modification time and size"""
    if filepath.exists():
        stats = filepath.stat()
        mod_time = datetime.fromtimestamp(stats.st_mtime).strftime("%Y-%m-%d %H:%M:%S")
        size_kb = stats.st_size / 1024
        return mod_time, size_kb
    return None, None


def main():
    """Main sync workflow"""
    parser = argparse.ArgumentParser(
        description="Sync Google Sheets data to CSV"
    )
    parser.add_argument(
        '--backup-only',
        action='store_true',
        help='Only create backup of current file without downloading new data'
    )
    args = parser.parse_args()
    
    print("=" * 60)
    print("GOOGLE SHEETS → CSV SYNC")
    print("=" * 60)
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Setup
    setup_directories()
    
    current_file = DATA_DIR / CURRENT_FILENAME
    
    # Backup mode: Just backup existing file
    if args.backup_only:
        if current_file.exists():
            create_timestamped_backup(current_file)
            cleanup_old_backups(keep_count=10)
            print("\n✅ Backup completed successfully")
        else:
            print(f"❌ No file to backup at {current_file}")
        return
    
    # Full sync mode: Download new data
    # 1. Check existing file
    if current_file.exists():
        old_mod_time, old_size = get_file_stats(current_file)
        print(f"📄 Current file: {CURRENT_FILENAME}")
        print(f"   Modified: {old_mod_time}")
        print(f"   Size: {old_size:.2f} KB")
        print()
    
    # 2. Authenticate and download
    client = authenticate_google_sheets()
    
    # Download to temporary location first
    temp_file = DATA_DIR / f"temp_{CURRENT_FILENAME}"
    num_rows = download_sheet_as_csv(client, temp_file)
    
    # 3. Compare and update
    if current_file.exists():
        # Create backup before replacing
        create_timestamped_backup(current_file)
        cleanup_old_backups(keep_count=10)
    
    # Replace current file with new download
    shutil.move(str(temp_file), str(current_file))
    
    # 4. Show new file stats
    new_mod_time, new_size = get_file_stats(current_file)
    print()
    print(f"📄 Updated file: {CURRENT_FILENAME}")
    print(f"   Modified: {new_mod_time}")
    print(f"   Size: {new_size:.2f} KB")
    print(f"   Rows: {num_rows}")
    
    print()
    print("=" * 60)
    print(f"✅ SYNC COMPLETED SUCCESSFULLY")
    print(f"Finished: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Sync interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
