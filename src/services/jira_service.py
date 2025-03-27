from jira import JIRA
from src.utils.logger import Logger

class JiraService:
    def __init__(self, config):
        """
        Initialize Jira connection
        
        :param config: Dictionary containing Jira connection details
        """
        self.logger = Logger(__name__)
        try:
            self.client = JIRA(
                server=config['server'],
                basic_auth=(config['username'], config['token'])
            )
        except Exception as e:
            self.logger.error(f"Jira connection failed: {e}")
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
                    'Created': bug.fields.created,
                    'Reporter': bug.fields.reporter.displayName if bug.fields.reporter else 'Unassigned',
                    'Assignee': bug.fields.assignee.displayName if bug.fields.assignee else 'Unassigned'
                }
                for bug in bugs
            ]
        
        except Exception as e:
            self.logger.error(f"Error retrieving bug data: {e}")
            return []