import sys
import os

# Ensure standard library path is included
sys.path.append(os.path.dirname(sys.executable))

try:
    import imghdr
except ImportError:
    print("Warning: imghdr module not found. Attempting to resolve...")

try:
    from jira import JIRA
except ImportError as e:
    print(f"Jira import error: {e}")
    print("Attempting alternative import strategies...")

from src.utils.logger import Logger

class JiraService:
    def __init__(self, config):
        """
        Initialize Jira connection with robust error handling
        
        :param config: Dictionary containing Jira connection details
        """
        self.logger = Logger(__name__)
        try:
            # Try multiple authentication methods
            try:
                self.client = JIRA(
                    server=config['server'],
                    basic_auth=(config['username'], config['token'])
                )
            except Exception as basic_auth_error:
                try:
                    # Fallback to token-based authentication
                    self.client = JIRA(
                        server=config['server'],
                        token_auth=config['token']
                    )
                except Exception as token_auth_error:
                    self.logger.error(f"Jira connection failed: {basic_auth_error}")
                    self.logger.error(f"Fallback authentication failed: {token_auth_error}")
                    raise
        except Exception as e:
            self.logger.error(f"Comprehensive Jira connection failure: {e}")
            raise

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
                    'Created': str(bug.fields.created),
                    'Reporter': bug.fields.reporter.displayName if bug.fields.reporter else 'Unassigned',
                    'Assignee': bug.fields.assignee.displayName if bug.fields.assignee else 'Unassigned'
                }
                for bug in bugs
            ]
        
        except Exception as e:
            self.logger.error(f"Error retrieving bug data: {e}")
            return []