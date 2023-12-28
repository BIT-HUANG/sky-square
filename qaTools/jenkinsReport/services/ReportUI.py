import os
from qaTools.jenkinsReport.utils.server import QAJenkinsOperation
from portalUtils.Logger import Logger
from portalUtils.FileSystem import FileSystemSrv


class QAJenkinsUIReport:
    def __init__(self):
        self.jenkins_report_logger = Logger.get_logger("SKY", "QAJenkinsUIReport")
        self.QJO = QAJenkinsOperation()
        self.FSS = FileSystemSrv()

    def get_all_jobs(self):
        job_list = self.QJO.get_all_job()
        return job_list

    def get_all_build_by_job_name(self, job_name):
        build_id_list = self.QJO.get_builds_id_of_job(job_name)
        return build_id_list

    def get_job_build_parameter_single_branch(self, job_name):
        branch_list = self.QJO.get_job_parameter(job_name)
        return branch_list

    def build_with_parameter_single_branch(self, job_name, parameter):
        build_id = self.QJO.build_with_parameter(job_name, parameter)
        return build_id

    def download_jenkins_ui_report(self, job_name, build_id):
        BASE_DIR = os.getcwd()
        jenkins_report_path = os.path.join(BASE_DIR, 'data', 'Test_Report', 'JenkinsTemp')
        if not os.path.exists(jenkins_report_path):
            os.mkdir(jenkins_report_path)
        report_url_list = self.QJO.get_artifact_info_by_name_and_build_id(job_name, build_id)
        report = report_url_list[0]
        self.QJO.download_artifacts(report['job_name'], report['build_no'], report['relative_path'], jenkins_report_path)
        report = self.FSS.dir_listing('Test_Report/UI_test/JenkinsTemp/allure-report/index.html', 'GET')
        if report:
            return 'Success'
        else:
            return 'Failed'
