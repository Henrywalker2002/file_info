import json
from fileHandler import FileHandler
import os 

if __name__ == '__main__':
    
    settings: dict = json.load(open('settings.json', 'r'))
    if not settings.get('root_tp_path', None):
        raise ValueError("Root TP path is not set in settings.json")
    file_handler = None
    res = {}
    if not settings.get('case_name', None):
        path = settings.get('root_tp_path') + '\\test'
        directories = [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d)) and d.startswith('case')]
        for directory in directories:
            file_handler = FileHandler(directory)
            res[directory] = file_handler.get_all_info()
    else:
        file_handler = FileHandler(settings['case_name'])
        res[settings['case_name']] = file_handler.get_all_info()
    if not settings.get('is_to_file', False):
        print(json.dumps(res, indent=4))
    else :
        if not settings.get('file_output_path', None):
            with open('./output.json', 'w') as file:
                json.dump(res, file, indent=4)
        else:
            with open(settings['file_output_path'], 'w') as file:
                json.dump(res, file, indent=4)


