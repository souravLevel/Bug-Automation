import sys
import os
from datetime import datetime
from src.utils.logger import Logger

class JiraService:
    def __init__(self, config):
        """
        Initialize Jira connection with robust error handling
        
        :param config: Dictionary containing Jira connection details
        """
        self.logger = Logger(__name__)
        try:
            # Patch sys.modules to handle imghdr dependency
            # This creates an empty module object to satisfy the import
            # without needing to create a separate file
            if 'imghdr' not in sys.modules:
                import types
                sys.modules['imghdr'] = types.ModuleType('imghdr')
                sys.modules['imghdr'].what = lambda file, h=None: None
                self.logger.info("Added imghdr module patch to sys.modules")

            # Import JIRA inside the method to handle import errors gracefully
            try:
                from jira import JIRA
                self.logger.info("Successfully imported JIRA module")
            except ImportError as e:
                self.logger.error(f"Failed to import JIRA module: {e}")
                raise ImportError(f"The 'jira' package is required but could not be imported. "
                                 f"Please ensure it's installed correctly. Error: {e}")

            # Try multiple authentication methods
            try:
                self.client = JIRA(
                    server=config['server'],
                    basic_auth=(config['username'], config['token'])
                )
                self.logger.info("Successfully connected to JIRA using basic auth")
            except Exception as basic_auth_error:
                try:
                    # Fallback to token-based authentication
                    self.client = JIRA(
                        server=config['server'],
                        token_auth=config['token']
                    )
                    self.logger.info("Successfully connected to JIRA using token auth")
                except Exception as token_auth_error:
                    self.logger.error(f"Jira connection failed: {basic_auth_error}")
                    self.logger.error(f"Fallback authentication failed: {token_auth_error}")
                    raise
        except Exception as e:
            self.logger.error(f"Comprehensive Jira connection failure: {e}")
            raise

    def _format_date(self, date_string):
        """
        Format a date string from Jira to dd-mm-yyyy format
        
        :param date_string: Date string from Jira (format: YYYY-MM-DDTHH:MM:SS.000+0000)
        :return: Formatted date string (dd-mm-yyyy)
        """
        try:
            # Parse the Jira date format (ISO format with timezone)
            date_obj = datetime.strptime(date_string.split('.')[0], '%Y-%m-%dT%H:%M:%S')
            # Format to dd-mm-yyyy
            return date_obj.strftime('%d-%m-%Y')
        except Exception as e:
            self.logger.warning(f"Error formatting date '{date_string}': {e}")
            return date_string
            
    def get_bugs(self, jql_query):
        """
        Retrieve bugs from Jira based on JQL query
        
        :param jql_query: Jira Query Language string
        :return: List of bug dictionaries
        """
        try:
            bugs = self.client.search_issues(jql_query, maxResults=500)
            
            return [
                {
                    'Key': bug.key,
                    'Summary': bug.fields.summary,
                    'Status': bug.fields.status.name,
                    'Priority': bug.fields.priority.name,
                    'Created': self._format_date(bug.fields.created),
                    'Reporter': bug.fields.reporter.displayName if bug.fields.reporter else 'Unassigned',
                    'Assignee': bug.fields.assignee.displayName if bug.fields.assignee else 'Unassigned',
                    'Labels': ', '.join(bug.fields.labels) if hasattr(bug.fields, 'labels') and bug.fields.labels else ''
                }
                for bug in bugs
            ]
        
        except Exception as e:
            self.logger.error(f"Error retrieving bug data: {e}")
            return []