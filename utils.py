import time
import re

class CommonFunc:
    @staticmethod
    def get_date_time(fl_time : float) -> str:
        local_time = time.localtime(fl_time)
        return time.strftime("%Y-%m-%d %H:%M:%S", local_time)

    @staticmethod
    def extract_date_time(line : str) -> str:
        datetime_pattern = r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}'
        match = re.search(datetime_pattern, line)
        if match:
            return match.group(0)
        else:
            return None