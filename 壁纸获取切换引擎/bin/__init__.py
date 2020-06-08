from bin.baidu_img import baidu_img
from copy import copy
import threading
from static.pro import time_sleep
import time

dic = {
    '百度图搜':baidu_img,
}

th_dic = copy(dic)

th_lis = []

times = 0

close = True

lis = []

lock = threading.Lock()

def All_run(title,num=1,height=None,width=None):
    def inner(p):
        global times,lis
        while 1:
            if times > 0 and close:
                _lis = [i for i in next(p) if i != None]
                lock.acquire()
                if len(_lis):
                    lis.extend(
                        _lis
                    )
                times -= 1
                lock.release()
                if times == 0:times = -1
            elif close:
                time.sleep(time_sleep)
            else:
                break
    global close
    close = True
    for pro in th_dic:
        p = th_dic[pro](title)
        if num != 1:p.num = num
        if height and width:
            p.height = height
            p.width = width
        t = threading.Thread(target=inner,args=(p,))
        t.setDaemon(True)
        t.start()

def del_All():
    global close
    close = False
    lis.clear()

def ret_lis():
    global times,lis
    times = len(th_dic)
    while 1:
        if times == -1:
            _lis = copy(lis)
            lis.clear()
            return _lis
        time.sleep(time_sleep)