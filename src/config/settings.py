import os
from dotenv import load_dotenv

class Settings:
    def __init__(self):
        # Load environment variables from .env file
        load_dotenv()

    @property
    def jira_config(self):
        return {
            'server': os.getenv('JIRA_SERVER'),
            'username': os.getenv('JIRA_USERNAME'),
            'token': os.getenv('JIRA_TOKEN')
        }

    @property
    def sheets_config(self):
        return {
            'credentials_path': os.getenv('GOOGLE_SHEETS_CREDENTIALS_PATH'),
            'spreadsheet_id': os.getenv('GOOGLE_SHEETS_SPREADSHEET_ID')
        }

    @property
    def export_config(self):
        return {
            'interval_hours': int(os.getenv('EXPORT_INTERVAL_HOURS', 4)),
            'jql_query': os.getenv('JQL_QUERY', 'type = Bug AND status != Closed')
        }