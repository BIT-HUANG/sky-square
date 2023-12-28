import io

import jenkins
import requests
import zipfile
from requests.auth import HTTPBasicAuth
from portalUtils.Logger import Logger
from qaTools.config import BaseConfig as BC


class QAJenkinsOperation:
    def __init__(self):
        self.jenkins_report_logger = Logger.get_logger("SKY", "JenkinsReportServ")
        self.server = jenkins.Jenkins(
            url=BC.QA_JENKINS_URL, username=BC.QA_JENKINS_USERNAME, password=BC.QA_JENKINS_PASSWORD)

    def get_all_job(self):
        job_list = list()
        try:
            jobs = self.server.get_all_jobs()
        except Exception as e:
            return e
        for job in jobs:
            job_list.append(job['fullname'])
        return job_list

    def get_builds_id_of_job(self, job_name):
        build_list = list()
        try:
            builds_info = self.server.get_job_info(job_name, depth=1)['builds']
        except Exception as e:
            return e
        for build in builds_info:
            artifacts = build['artifacts']
            build_item = {
                'job': job_name,
                'build': str(build['number']),
                'building': build['building'],
                'progress': build['inProgress'],
                'result': build['result'],
                'duration': build['duration'],
                'artifacts': len(artifacts)
            }
            build_list.append(build_item)
        return build_list

    def get_artifact_info_by_name_and_build_id(self, job_name, build_id):
        artifact_list = list()
        try:
            artifacts = self.server.get_build_info(job_name, build_id)['artifacts']
        except Exception as e:
            return e
        if len(artifacts):
            for artifact in artifacts:
                if artifact_list != {}:
                    artifact_list.append(
                        {'job_name': job_name,
                         'build_no': build_id,
                         'relative_path': artifact['relativePath']})
        return artifact_list

    def download_artifacts(self, job_name, build_id, relative_path, extract_path):
        download_url = BC.QA_JENKINS_URL + '/job/' + job_name + '/' + build_id + '/artifact/' + relative_path
        response = requests.get(url=download_url, auth=HTTPBasicAuth(BC.QA_JENKINS_USERNAME, BC.QA_JENKINS_PASSWORD))
        print(type(response))
        try:
            with zipfile.ZipFile(io.BytesIO(response.content)) as myzip:
                myzip.extractall(extract_path)
            self.jenkins_report_logger.info('这是一个压缩包')
        except zipfile.BadZipFile:
            self.jenkins_report_logger.warn('这不是一个压缩包')

    def get_job_parameter(self, job_name):
        try:
            job_info = self.server.get_job_info(job_name, depth=1)
            branch_list = job_info['property'][0]['parameterDefinitions'][0]['allValueItems']['values']
            parameterDefinitions = job_info['property'][0]['parameterDefinitions']
            parameter_list = list()
            for definition in parameterDefinitions:
                para_key = definition['name']
                para_value = list()
                all_value_items_values = definition['allValueItems']['values']
                for value in all_value_items_values:
                    para_value.append(value['value'])
                parameter_list.append({'parameter_key': para_key, 'parameter_value': para_value})
        except Exception as e:
            return e
        return parameter_list

    def build_with_parameter(self, job_name, parameter):
        try:
            build_result = self.server.build_job(name=job_name, parameters=parameter)
        except Exception as e:
            return e
        return build_result


# QJO = QAJenkinsOperation()
# result = QJO.get_artifact_info_by_name_and_build_id('QA_automated_testing', 8)
# result = QJO.get_all_job()
# result = QJO.get_builds_id_of_job('QA_automated_testing')
# result = QJO.get_job_parameter('QA_automated_testing')
# para = {'branch': 'v1.0.0.1'}
# result = QJO.build_with_parameter('QA_automated_testing', para)
# QJO.download_artifacts('QA_automated_testing', '8', 'allure-report.zip')
# print(result)
