from atlassian import Jira
from testSkyCore.config import BaseConfig as BC


class JiraScanServ:
    def __init__(self, affect_version):
        self.affect_version = affect_version
        self.jira_server = Jira(url=BC.JIRA_BASIC_URL, username=BC.USERNAME, password=BC.ATLAS_PASSWORD)

    def get_issue_list_with_affect_version(self):
        jql_string = 'affectedVersion  = ' + self.affect_version
        jql_result = self.jira_server.jql(jql_string)
        key_list = list()
        for issue in jql_result['issues']:
            issue_dict = dict()
            issue_dict.update(
                {'key': issue['key'],
                 'type': issue['fields']['issuetype']['name'],
                 'status': issue['fields']['status']['name']})
            key_list.append(issue_dict)
        return key_list
