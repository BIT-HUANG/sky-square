import portalService
from flask_cors import *
from flask import Flask, request, jsonify, render_template, send_file, abort
import json
from portalUtils.FileSystem import FileSystemSrv
from testSkyCore.services.JiraScanServ import JiraScanServ
from qaTools.environmentCompare.services.EnvironmentCompare import EnvironmentCompare
from qaTools.jenkinsReport.services.ReportUI import QAJenkinsUIReport
from qaTools.tcmBranch.service.TcmBranch import TcmBranch
from portalUtils.Logger import Logger

portal_logger = Logger.get_logger("SKY", "Portal")

app = Flask(__name__)
CORS(app)

res_body = {
    'code': int(),
    'message': str(),
    'data': list()
}


@app.route("/skysquare/wechat_test", methods=["POST", "GET"])
def wechat_test():
    json_data_dict = request.get_json()
    portal_logger.info(json_data_dict)
    return jsonify(code=200, message='Success', data=json_data_dict)


@app.route("/skysquare/jira_test", methods=["POST"])
def jira_test():
    json_data_dict = request.get_json()
    affect_version = json_data_dict.get("affect_version")
    if not affect_version:
        portal_logger.warn('No version.')
        return jsonify(code=500, message='Please specific a affect_version.', data=[])
    try:
        JSS = JiraScanServ(affect_version)
        test_result = JSS.get_issue_list_with_affect_version()
        return jsonify(code=200, message='Success', data=test_result)
    except Exception as e:
        portal_logger.error(e)
        return jsonify(code=500, message="Fail, %s" % e, data=[])


@app.route("/skysquare/qa_tools/environment_compare", methods=["POST"])
def environment_compare():
    json_data_dict = request.get_json()
    environment = json_data_dict.get("environment")
    tcm = json_data_dict.get("tcm")
    if not environment:
        return jsonify(code=500, message='Please specific environment.', data=[])
    if tcm is False:
        try:
            EC = EnvironmentCompare(environment, '')
            compare_result = EC.environment_compare()
            return jsonify(code=200, message='Success', data=compare_result)
        except Exception as e:
            return jsonify(code=500, message="Fail, %s" % e, data=[])
    else:
        try:
            portal_logger.info(json_data_dict)
            page_title = json_data_dict.get("tcm_page_title")
            EC = EnvironmentCompare(environment, page_title)
            compare_result = EC.environment_compare_with_tcm()
            return jsonify(code=200, message='Success', data=compare_result)
        except Exception as e:
            portal_logger.info('tcm exception here')
            return jsonify(code=500, message="Fail, %s" % e, data=[])


@app.route("/skysquare/qa_tools/environment_compare/get-tcm-page", methods=["POST"])
def get_tcm_page():
    try:
        TB = TcmBranch()
        tcm_page = TB.get_tcm_page()
        return jsonify(code=200, message='Success', data=tcm_page)
    except Exception as e:
        return jsonify(code=500, message="Fail, %s" % e, data=[])


@app.route('/skysquare/data', defaults={'req_path': ''}, methods=['POST', 'GET'])
@app.route('/skysquare/data/<path:req_path>', methods=['POST', 'GET'])
def dir_listing(req_path):
    FSS = FileSystemSrv()
    result = FSS.dir_listing(req_method=request.method, req_path=req_path)
    match result['type']:
        case 'abort_404':
            return abort(404)
        case 'send_file':
            return send_file(result['data'])
        case 'post_for_data':
            return jsonify(code=200, message='Success', data=result['data'])
        case 'get_for_render':
            return render_template('FileSystem.html', files=result['data'])


@app.route('/skysquare/data-upload', methods=['POST'])
def file_upload():
    try:
        file_path = json.loads(request.form.get('data'))['file_path']
        file = request.files['file']
        FSS = FileSystemSrv()
        result = FSS.upload_file(req_file=file, req_path=file_path)
        return jsonify(code=200, message=result, data=[])
    except Exception as e:
        portal_logger.error(e)
        return jsonify(code=500, message="Fail, %s" % e, data=[])


@app.route('/skysquare/data-remove', methods=['POST'])
def file_remove():
    try:
        file_path = request.get_json()['file_path']
        FSS = FileSystemSrv()
        result = FSS.remove_file(req_path=file_path)
        return jsonify(code=200, message=result, data=[])
    except Exception as e:
        portal_logger.error(e)
        return jsonify(code=500, message="Fail, %s" % e, data=[])


@app.route('/skysquare/data-add-folder', methods=['POST'])
def file_path_add():
    try:
        file_path = request.get_json()['file_path']
        folder_name = request.get_json()['folder_name']
        FSS = FileSystemSrv()
        result = FSS.add_new_folder(req_path=file_path, folder_name=folder_name)
        return jsonify(code=200, message=result, data=[])
    except Exception as e:
        portal_logger.error(e)
        return jsonify(code=500, message="Fail, %s" % e, data=[])


@app.route('/skysquare/get-jenkins-jobs', methods=['POST'])
def get_jenkins_jobs():
    try:
        QJR = QAJenkinsUIReport()
        job_list = QJR.get_all_jobs()
        return jsonify(code=200, message="Success", data=job_list)
    except Exception as e:
        portal_logger.error(e)
        return jsonify(code=500, message="Fail, %s" % e, data=[])


@app.route('/skysquare/get-jenkins-job-builds', methods=['POST'])
def get_jenkins_job_builds():
    try:
        job_name = request.get_json()['job_name']
        QJR = QAJenkinsUIReport()
        build_list = QJR.get_all_build_by_job_name(job_name)
        return jsonify(code=200, message="Success", data=build_list)
    except Exception as e:
        portal_logger.error(e)
        return jsonify(code=500, message="Fail, %s" % e, data=[])


@app.route('/skysquare/download-jenkins-report', methods=['POST'])
def download_jenkins_report():
    try:
        job_name = request.get_json()['job_name']
        build_id = request.get_json()['build_id']
        QJR = QAJenkinsUIReport()
        result = QJR.download_jenkins_ui_report(job_name, build_id)
        portal_logger.info('Download status: ' + result)
        return jsonify(code=200, message="Success", data=[])
    except Exception as e:
        portal_logger.error(e)
        return jsonify(code=500, message="Fail, %s" % e, data=[])


@app.route('/skysquare/get-jenkins-job-parameter-list', methods=['POST'])
def get_jenkins_job_parameter_list():
    try:
        job_name = request.get_json()['job_name']
        QJR = QAJenkinsUIReport()
        result = QJR.get_job_build_parameter_single_branch(job_name)
        return jsonify(code=200, message="Success", data=result)
    except Exception as e:
        portal_logger.error(e)
        return jsonify(code=500, message="Fail, %s" % e, data=[])


@app.route('/skysquare/build-jenkins-job-with-parameter', methods=['POST'])
def build_jenkins_job_with_parameter():
    try:
        job_name = request.get_json()['job_name']
        parameter = request.get_json()['parameter']
        QJR = QAJenkinsUIReport()
        result = list()
        result.append(QJR.build_with_parameter_single_branch(job_name, parameter))
        return jsonify(code=200, message="Success", data=result)
    except Exception as e:
        portal_logger.error(e)
        return jsonify(code=500, message="Fail, %s" % e, data=[])


@app.route('/skysquare/shutdown', methods=["POST"])
def shutdown():
    if request.method == 'POST':
        shutdown_server()
        return jsonify(message='Server shutting down...')


def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with Werkzeug Server')
    func()


if __name__ == '__main__':
    CORS(app, supports_credentials=True)
    app.run(host='0.0.0.0', port=int(portalService.port_), threaded=True)
