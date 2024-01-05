from portalUtils.Logger import Logger
from qaTools.jenkinsReport.utils.server import QAJenkinsOperation
from qaTools.config import BaseConfig as BC

class QAJenkinsAPIReport:
    def __init__(self):
        self.jenkins_report_logger = Logger.get_logger("SKY", "QAJenkinsAPIReport")
        self.QJO = QAJenkinsOperation()

    def get_api_test_job(self):
        job_list = self.QJO.get_jobs_by_views('API_TEST')
        return job_list

    def get_all_build_result_by_job_name(self, job_name):
        build_list = self.QJO.get_builds_id_of_job(job_name)
        result_list = self.QJO.get_apifox_report_list_by_ui(job_name)
        for build in build_list:
            expect_report_name = build['job'] + '_' + build['build'] + '.html'
            for result in result_list:
                if expect_report_name == result['name']:
                    report_url = BC.QA_JENKINS_URL + '/job/' + job_name + '/ws/apifox-reports/' + expect_report_name
                    build['report_type'] = 1
                    build['api_report'] = result['name']
                    build['api_report_time'] = result['time']
                    build['api_report_link'] = report_url
                    break
                else:
                    build['report_type'] = 0
                    build['api_report'] = None
                    build['api_report_time'] = None
                    build['api_report_link'] = None
        return build_list

    def get_html_report(self, job_name, build_no):
        content = self.QJO.get_apifox_report_html(job_name, build_no)
        return content


# JAR = JenkinsApiReport()
# jobs_list = JAR.get_api_test_job()
# builds = JAR.get_all_build_result_by_job_name(jobs_list[0])
# print(builds)
