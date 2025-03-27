from google.oauth2 import service_account
from googleapiclient.discovery import build
from src.utils.logger import Logger
from datetime import datetime

class SheetsService:
    def __init__(self, config):
        """
        Initialize Google Sheets connection
        
        :param config: Dictionary containing Sheets connection details
        """
        self.logger = Logger(__name__)
        try:
            SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
            credentials = service_account.Credentials.from_service_account_file(
                config['credentials_path'], scopes=SCOPES
            )
            self.service = build('sheets', 'v4', credentials=credentials)
            self.spreadsheet_id = config['spreadsheet_id']
        except Exception as e:
            self.logger.error(f"Google Sheets connection failed: {e}")
            raise

    def export_data(self, bug_data):
        """
        Export bug data to Google Sheets
        
        :param bug_data: List of bug dictionaries
        """
        try:
            # Prepare headers and rows
            headers = [
                'Bug Key', 'Summary', 'Status', 'Priority', 
                'Created', 'Reporter', 'Assignee', 'Labels'
            ]
            
            rows = [[
                bug['Key'], bug['Summary'], bug['Status'], 
                bug['Priority'], bug['Created'], bug['Reporter'], 
                bug['Assignee'], bug['Labels']
            ] for bug in bug_data]
            
            # Combine headers and rows
            values = [headers] + rows
            
            # Clear existing data and write new data
            body = {'values': values}
            result = self.service.spreadsheets().values().update(
                spreadsheetId=self.spreadsheet_id, 
                range='Sheet1!A1', 
                valueInputOption='RAW', 
                body=body
            ).execute()
            
            self.logger.info(f"Successfully exported {len(rows)} bugs at {datetime.now()}")
        
        except Exception as e:
            self.logger.error(f"Error exporting to Google Sheets: {e}")