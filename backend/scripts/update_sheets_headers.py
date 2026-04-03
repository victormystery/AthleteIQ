"""
Utility script to update Google Sheets headers with ML prediction columns
Run this once after setting up Google Sheets integration
"""
import sys
import os

# Add the parent directory to the path so we can import app modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.google_sheets_service import get_sheets_service


def main():
    """Update Google Sheets headers to include ML prediction columns"""
    print("=" * 80)
    print("Google Sheets Header Update Utility")
    print("=" * 80)
    print()
    
    print("This will add the following columns to your Google Sheet:")
    print("  • Top Career Prediction")
    print("  • Prediction Confidence")
    print("  • User Email")
    print()
    
    # Get sheets service
    sheets_service = get_sheets_service()
    
    if not sheets_service.is_initialized():
        print("❌ Error: Google Sheets client not initialized")
        print()
        print("Please ensure:")
        print("  1. GOOGLE_SHEETS_CREDENTIALS_PATH is set in your .env file")
        print("  2. The credentials file exists at the specified path")
        print("  3. You have enabled Google Sheets API in Google Cloud Console")
        print()
        return 1
    
    print("✅ Google Sheets client initialized successfully")
    print()
    print(f"📊 Spreadsheet ID: {sheets_service.spreadsheet_id}")
    print(f"📄 Worksheet: {sheets_service.worksheet_name}")
    print()
    
    # Ask for confirmation
    response = input("Do you want to proceed? (y/n): ")
    if response.lower() != 'y':
        print("❌ Cancelled")
        return 0
    
    print()
    print("Updating headers...")
    
    # Update headers
    result = sheets_service.update_spreadsheet_headers()
    
    if result:
        print("✅ Headers updated successfully!")
        print()
        print("You can now start submitting questionnaires.")
        print("The ML predictions will be automatically saved to Google Sheets.")
        return 0
    else:
        print("❌ Failed to update headers")
        print("Check the logs for more details")
        return 1


if __name__ == "__main__":
    exit(main())
