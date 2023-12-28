import os
import shutil
import zipfile
from portalUtils.Logger import Logger
from sortedcontainers import SortedDict
from collections import OrderedDict


class FileSystemSrv:
    def __init__(self):
        self.filesys_logger = Logger.get_logger("SKY", "FileSys")

    def dir_listing(self, req_path, req_method):
        BASE_DIR = os.getcwd()
        format_path = req_path
        if os.name == 'nt':
            format_path = req_path.replace('/', '\\')
        # Joining the base and the requested path
        abs_path = os.path.join(BASE_DIR, 'data', format_path)
        if os.name == 'nt':
            parent_path_index = format_path.rfind('\\')
            if parent_path_index != -1:
                parent_path = format_path[:parent_path_index]
            else:
                parent_path = ''
        else:
            parent_path_index = format_path.rfind('/')
            if parent_path_index != -1:
                parent_path = format_path[:parent_path_index]
            else:
                parent_path = ''
        # Return 404 if path doesn't exist
        if not os.path.exists(abs_path):
            self.filesys_logger.error('path not exist: ' + abs_path)
            return {'type': 'abort_404', 'data': ''}

        # Check if path is a file and serve
        if os.path.isfile(abs_path):
            return {'type': 'send_file', 'data': abs_path}

        # Show directory contents
        d = SortedDict(dict((x, os.path.join(req_path, x).replace('\\', '/')) for x in os.listdir(abs_path)))
        parent_path_tuple = ('<<<', parent_path)
        d_temp_list = list(d.items())
        d_temp_list.append(parent_path_tuple)
        files = OrderedDict(reversed(d_temp_list))
        file_list_for_post = list()
        for k, v in files.items():
            path_type = str()
            temp_file_path = os.path.join(BASE_DIR, 'data', v)
            temp_path = temp_file_path
            if os.name == 'nt':
                temp_path = temp_file_path.replace('/', '\\')
            if os.path.isfile(temp_path):
                path_type = 'file'
            if os.path.isdir(temp_path):
                path_type = 'dir'
            file_list_for_post.append({'file_name': k, 'file_path': v, 'type': path_type})
        if req_method == 'POST':
            return {'type': 'post_for_data', 'data': file_list_for_post}
        else:
            return {'type': 'get_for_render', 'data': files}

    def upload_file(self, req_file, req_path):
        self.filesys_logger.info('path: ' + req_path)
        BASE_DIR = os.getcwd()
        format_path = req_path
        if os.name == 'nt':
            format_path = req_path.replace('/', '\\')
        abs_path = os.path.join(BASE_DIR, 'data', format_path)
        extract_path = os.path.join(abs_path, os.path.splitext(req_file.filename)[0])
        if req_file.filename.endswith('.zip'):
            try:
                with zipfile.ZipFile(req_file, 'r') as zip_ref:
                    zip_ref.extractall(extract_path)
                    return 'Success'
            except zipfile.BadZipFile:
                self.filesys_logger.error("Error: Invalid zip file.")
                return 'Fail'
        else:
            req_file.save(os.path.join(abs_path, req_file.filename))
        return 'Success'

    def remove_file(self, req_path):
        if req_path == '':
            return {'type': 'Fail', 'data': 'Can not Remove.'}
        else:
            BASE_DIR = os.getcwd()
            format_path = req_path

            if os.name == 'nt':
                format_path = req_path.replace('/', '\\')
            abs_path = os.path.join(BASE_DIR, 'data', format_path)
            if os.name == 'nt':
                parent_path_index = format_path.rfind('\\')
                if parent_path_index != -1:
                    parent_path = format_path[:parent_path_index]
                else:
                    parent_path = ''
            else:
                parent_path_index = format_path.rfind('/')
                if parent_path_index != -1:
                    parent_path = format_path[:parent_path_index]
                else:
                    parent_path = ''
            try:
                if os.path.isfile(abs_path):
                    os.remove(abs_path)
                else:
                    shutil.rmtree(abs_path)
                return {'type': 'Success', 'data': abs_path + ' Removed.', 'parent': parent_path}
            except OSError as e:
                self.filesys_logger.error("Failed to remove file or dir.")
                return {'type': 'Fail', 'data': str(e)}

    def add_new_folder(self, folder_name, req_path):
        BASE_DIR = os.getcwd()
        format_path = req_path
        if os.name == 'nt':
            format_path = req_path.replace('/', '\\')
        abs_path = os.path.join(BASE_DIR, 'data', format_path)
        full_path = os.path.join(abs_path, folder_name)
        try:
            os.makedirs(full_path)
            return {'type': 'Success', 'data': full_path + ' Added.'}
        except OSError as e:
            self.filesys_logger.error("Failed to add dir.")
            return {'type': 'Fail', 'data': str(e)}
