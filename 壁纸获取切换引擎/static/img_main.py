import requests
from static.pro import time_out,time_sleep
import time

class img_main:

    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.3',
    }

    def __init__(self,title):
        self.now = True
        self.num = 1
        self.width = 1920
        self.height = 1080
        self.run(title)

    def run(self,title):
        pass

    def get_data(self, num=0, **kwargs):
        if num == 3: return None
        try:
            resp = requests.get(timeout=time_out, **kwargs)
            time.sleep(time_sleep)
            return resp
        except Exception:
            time.sleep(1)
            return self.get_data(num + 1, **kwargs)