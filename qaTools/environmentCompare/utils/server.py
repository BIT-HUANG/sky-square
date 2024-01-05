import jenkins
from qaTools.config import BaseConfig as BC


def service_name_format(name):
    endings = ['_dev', '_qa', '_uat', '-dev', '-qa', '-uat']
    for ending in endings:
        name = name.replace(ending, '')
    return name


def job_name_format(name, env):
    if name == 'sc-scripts':
        job_name = name + '-' + env.lower()
    else:
        job_name = name + '_' + env.lower()
    return job_name


class JenkinsOperation:
    def __init__(self, views):
        self.server = jenkins.Jenkins(url=BC.JENKINS_URL, username=BC.USERNAME, password=BC.JENKINS_PASSWORD)
        self.views = views

    def get_last_successful_build_info_of_job(self, job_name):
        try:
            last_build_info = self.server.get_build_info(job_name, 'lastSuccessfulBuild')
        except:
            return 'No Build Info'
        for action in last_build_info['actions']:
            if action != {} and action['_class'] == 'hudson.plugins.git.util.BuildData':
                return action['lastBuiltRevision']['branch'][0]['name']
            else:
                continue

    def get_all_jobs(self):
        job_name_set = set()
        for view in self.views:
            view_jobs_list = self.server.get_jobs(view_name=view)
            for view_job in view_jobs_list:
                if view_job['color'] != 'aborted':
                    job_name_set.add(service_name_format(view_job['name']))
        return list(job_name_set)

    def get_env_service_build_info(self):
        build_info_list = list()
        service_list = self.get_all_jobs()
        for service in service_list:
            job_build_dict = {'service': service}
            for env in self.views:
                job_env_name = job_name_format(service, env)
                build_info = self.get_last_successful_build_info_of_job(job_env_name)
                job_build_dict[env] = build_info
            build_info_list.append(job_build_dict)
        return build_info_list

    def deploy_service_to_env_with_tag(self, service, env, tag):
        try:
            job_name = service + '_' + env
            para = {'TAG': tag}
            build_result = self.server.build_job(name=job_name, parameters=para)
        except Exception as e:
            return e
        return build_result
