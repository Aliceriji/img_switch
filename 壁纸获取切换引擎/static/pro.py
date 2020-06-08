import os
_PATH = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
PATH = os.path.join(_PATH,'path')
img_path = os.path.join(PATH,'1.jpg')
json_path = os.path.join(PATH,'access.json')
url_path = os.path.join(PATH,'url.json')
save_path = os.path.join(_PATH,'save_img')
log_url_path = os.path.join(PATH,'log.txt')

html_file = os.path.join(PATH,'index.html')

bro = {
    '自动壁纸等待时间':60,
    '自动更换(0/1)':1,
    '保存图片路径':save_path,
    '是否获取网页图片连接(0/1)':1,
    '获取网页组号码':1,
}

time_out = 3
time_sleep = 3

url_sleep = 3600