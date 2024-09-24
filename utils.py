import time

class CommonFunc:
    @staticmethod
    def get_date_time(fl_time : float) -> str:
        local_time = time.localtime(fl_time)
        return time.strftime("%Y-%m-%d %H:%M:%S", local_time)