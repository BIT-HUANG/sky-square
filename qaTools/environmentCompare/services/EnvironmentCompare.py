from qaTools.environmentCompare.utils.server import JenkinsOperation
from qaTools.tcmBranch.utils.server import ConfluenceOperation
from portalUtils.Logger import Logger
import time


class EnvironmentCompare:
    def __init__(self, views, tcm_title):
        self.views = views
        self.tcm_title = tcm_title
        self.ec_logger = Logger.get_logger("SKY", "EnvironmentCompare")

    def environment_compare(self):
        compare_result_list = JenkinsOperation(self.views).get_env_service_build_info()
        self.ec_logger.info('env_result_list is:  ')
        self.ec_logger.info(compare_result_list)
        return compare_result_list

    def tcm_service_info(self):
        CO = ConfluenceOperation()
        tcm_result = CO.get_branch_dict_list_from_table_by_title(self.tcm_title)
        self.ec_logger.info('tcm_result is:  ')
        self.ec_logger.info(tcm_result)
        return tcm_result

    def environment_compare_with_tcm(self):
        jenkins_list = self.environment_compare()
        tcm_list = self.tcm_service_info()
        for tcm in tcm_list:
            for jenkins in jenkins_list:
                if tcm['service'] in jenkins['service']:
                    jenkins['TCM'] = tcm['tcm']
                    if jenkins['QA'] != jenkins['TCM']:
                        jenkins['QA_result'] = 1
                    if jenkins['UAT'] != jenkins['TCM']:
                        jenkins['UAT_result'] = 1
        self.ec_logger.info('tcm_compare_result is:  ')
        self.ec_logger.info(jenkins_list)
        return jenkins_list

    def deploy_service(self, deploy_list):
        result_list = list()
        for deploy in deploy_list:
            result = JenkinsOperation(self.views).deploy_service_to_env_with_tag(
                deploy['service'], deploy['environment'], deploy['tag'])
            result_list.append({'service': deploy['service'], 'result': result})
            time.sleep(1)
        return result_list


EC = EnvironmentCompare(['QA', 'UAT'], 'TCM 2023-12-28 常规发版')
result = EC.environment_compare_with_tcm()
print(result)