import json


class SafeFileIO:
    @staticmethod
    def safe_read_file_content(target_file_path):
        with open(target_file_path, "r") as f:
            content = f.read()
            return content

    @staticmethod
    def safe_load_json_content(json_file_path):
        with open(json_file_path, "r") as f:
            json_data = json.load(f)
            return json_data

    @staticmethod
    def safe_write_content(target_file_path, content):
        with open(target_file_path, "w") as f:
            for data in content:
                f.write(data)
                f.write('\n')
                
    @staticmethod            
    def safe_get_file_rows(target_file_path):
        with open(target_file_path, 'r') as f:
            row_content = f.readlines()
            return len(row_content)
