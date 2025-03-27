import schedule
import time
from src.config.settings import Settings
from src.services.jira_service import JiraService
from src.services.sheets_service import SheetsService
from src.utils.logger import Logger

class BugExporter:
    def __init__(self, settings):
        """
        Initialize Bug Exporter with services
        
        :param settings: Settings instance
        """
        self.logger = Logger(__name__)
        
        # Initialize services
        self.jira_service = JiraService(settings.jira_config)
        self.sheets_service = SheetsService(settings.sheets_config)
        
        # Export configuration
        self.export_config = settings.export_config

    def run_export(self):
        """
        Retrieve bug data and export to Google Sheets
        """
        try:
            # Retrieve bugs from Jira
            bug_data = self.jira_service.get_bugs(
                self.export_config['jql_query']
            )
            
            # Export to Google Sheets
            self.sheets_service.export_data(bug_data)
        
        except Exception as e:
            self.logger.error(f"Export process failed: {e}")