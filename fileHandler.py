import os 
import json
from utils import CommonFunc

class FileHandler:
    settings_path = './settings.json'
    
    def __init__(self, case_name) -> None:
        with open(self.settings_path, 'r') as file:
            self.settings : dict = json.load(file)
        if not self.settings.get('root_tp_path', None):
            raise ValueError("Root TP path is not set in settings.json")
        self.root_tp_path = self.settings['root_tp_path']
        self.case_path = self.root_tp_path + f'\\test\\{case_name}'
        self.test_results_path = self.case_path + '\\test_results'
    
    def get_file_stats(self, file_path):
        file_stats = os.stat(file_path)
        return file_stats

    def get_file_time_content(self, file_path):
        with open(file_path, 'r') as file:
            lines = file.readlines()
            if len(lines) < 2:
                return None
            return [CommonFunc.extract_date_time(lines[1]), CommonFunc.extract_date_time(lines[-1])]
        raise ValueError("File is empty")

    def get_file_stats_and_content(self, file_path):
        return self.get_file_stats(file_path), self.get_file_time_content(file_path) 
    
    def get_full_info(self, file_path):
        res = {}
        properties, content = self.get_file_stats_and_content(file_path)
        res['file_size'] = properties.st_size
        res['created_at'] = CommonFunc.get_date_time(properties.st_ctime)
        res['modified_at'] = CommonFunc.get_date_time(properties.st_mtime)
        if content is None:
            return res
        res['log_start_time'] = content[0]
        res['log_end_time'] = content[1]
        return res 
    
    def get_mi_log_infor(self):
        res = {}
        files = os.listdir(self.case_path)
        mi_files = [f for f in files if f.startswith('mi_')]
        for file in mi_files:
            file_path = self.case_path + '/' + file
            res[file] = self.get_full_info(file_path)
        res['number_of_mi_files'] = len(mi_files)
        return res

    def get_mt_log_info(self):
        res = {}
        files = os.listdir(self.case_path)
        mt_files = [f for f in files if f.startswith('mt_')]
        for file in mt_files:
            file_path = self.case_path + '/' + file
            res[file] = self.get_full_info(file_path)
        res['number_of_mt_files'] = len(mt_files)
        return res
    
    def get_res_file_info(self):
        res = {}
        res['recycle_files'] = {}
        res['out_files'] = {}
        recycle_files = os.listdir(self.test_results_path + '\\recycle_files')
        out_files = os.listdir(self.test_results_path + '\\huflt\\out')
        for file in recycle_files:
            file_path = self.test_results_path + '\\recycle_files\\' + file
            res['recycle_files'][file] = self.get_full_info(file_path)
        for file in out_files:
            file_path = self.test_results_path + '\\huflt\\out\\' + file
            res['out_files'][file] = self.get_full_info(file_path)
        return res
    
    def get_all_info(self) -> dict:
        res = {}
        res['mi_log_info'] = self.get_mi_log_infor()
        res['mt_log_info'] = self.get_mt_log_info()
        res['test_results_infor'] = self.get_res_file_info()
        res['test_run_infor'] = {}
        res['test_run_infor'] = self.get_full_info(self.case_path + '\\test_run.log')
        return res
    