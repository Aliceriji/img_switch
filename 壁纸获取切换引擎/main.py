import ctypes
import webbrowser
from tkinter import *
from static.pro import *
import json
from bin import All_run,del_All,ret_lis
import threading
import time
import requests
import random

GET_TIMES = True
All_lis = []
now = True

class MAIN:

    def __init__(self):
        self.root = Tk()
        self.run()
        self.root.mainloop()

    def __bro(self,TYPE=None):
        if TYPE == None and not os.path.isfile(json_path):
            with open(json_path,'w') as f:
                f.write(json.dumps(bro))
            self.bro = bro
        elif TYPE == None:
            with open(json_path,'r') as f:
                self.bro = json.loads(f.read())
        else:
            with open(json_path,'w') as f:
                f.write(json.dumps(self.bro))

    def mu_file(self):
        def add_Entry():
            for i in self.bro:
                Label(t,text=i).pack()
                e = Entry(t)
                e.insert(0,str(self.bro[i]))
                e.pack()
                Entry_lis.append(e)
        def save():
            lis = [i.get() for i in Entry_lis]
            if lis[0] == '' or lis[2] == '' or lis[-1] == '':return None
            for i,n in zip(lis,self.bro):
                if i == '':
                    i = '0'
                self.bro[n] = i
            self.__bro(1)
            t.destroy()
        Entry_lis = []
        t = Toplevel(self.root)
        t.title('修改默认配置')
        t.minsize(400,300)
        t.iconbitmap(self.icon)
        add_Entry()
        Button(t,text='点击保存',command=save).pack()

    def write_json(self,path,_json):
        with open(path,'w') as f:
            f.write(json.dumps(_json))

    def insert(self,lis,_t):
        def inner():
            _t.delete('0.0',END)
            for url in lis:
                _t.insert('end',url+'\n')
                _t.see(END)
        t = threading.Thread(target=inner)
        t.setDaemon(True)
        t.start()

    def __read(self):
        if os.path.isfile(url_path):
            global All_lis
            with open(url_path, 'r') as f:
                All_lis = json.loads(f.read())
        self.insert(All_lis,self.T1)

    def get_url_set(self,url):
        def inner(num=0):
            if num == 3:
                self.var.set('当前状态:无法切换')
                return None
            if ctypes.windll.user32.SystemParametersInfoW(20, 0, img_path, 3) == 1:
                self.var.set('当前状态:切换成功')
                return True
            else:
                return inner(num=1)
        if url == '':
            print('空值')
            return None
        try:
            data = requests.get(url)
        except EXCEPTION:
            print(url)
        if data.status_code == 200:
            with open(img_path,'wb+') as f:
                f.write(data.content)
            return True if inner() else False
        else:
            self.var.set('当前状态:切换失败')
            return False

    def time_get(self):
        def random_lis():
            random.shuffle(All_lis)
            random.shuffle(All_lis)
            random.shuffle(All_lis)
            random.shuffle(All_lis)
        def inner():
            while int(self.bro['自动更换(0/1)']) == 1:
                if len(All_lis) > 0:
                    random_lis()
                    url = All_lis.pop()
                    self.T2.insert('end',url+'\n')
                    self.write_json(url_path,All_lis)
                    self.__read()
                    if not self.get_url_set(url):
                        time.sleep(time_sleep)
                        continue
                    time.sleep(url_sleep)
                else:
                    time.sleep(time_sleep)
        t = threading.Thread(target=inner)
        t.setDaemon(True)
        t.start()

    def run(self):
        def var_set(title):
            self.var.set('当前状态:'+title)
        def _run():
            def inner():
                global All_lis,GET_TIMES
                while GET_TIMES:
                    var_set('获取中')
                    if int(self.bro['是否获取网页图片连接(0/1)']) != 1:
                        GET_TIMES = False
                        var_set('当前未开启')
                    elif len(All_lis) == 0:
                        lis = ret_lis()
                        All_lis.extend(
                            [i for _n in lis for i in _n if i not in All_lis]
                        )
                        self.write_json(url_path,All_lis)
                        var_set('读取完毕')
                        self.__read()
                    else:
                        time.sleep(time_sleep*3)
            global now,GET_TIMES
            if now != True and self.E2.get(): return None
            if self.bro['是否获取网页图片连接(0/1)'] == 1:GET_TIMES = True
            now = False
            All_run(self.E2.get())
            t = threading.Thread(target=inner)
            t.setDaemon(True)
            t.start()
        def add_html(t):
            title = '<a href="%s"><img src="%s" style="width: 328px;height: 205px"></a>\n'
            All_title = ''
            for url in t.get('0.0',END).strip().split('\n'):
                All_title += title%(url,url)
            with open(html_file,'w') as f:
                f.write(All_title)
            webbrowser.open(html_file)
        def __save(TYPE):
            if TYPE == 1:
                num = len([i for i in os.listdir(save_path) if 'jpg' in i]) +1
                file_name = save_path+'/'+str(num)+'.jpg'
                with open(img_path,'rb+') as f:
                    img_data = f.read()
                with open(file_name,'wb+') as f:
                    f.write(img_data)
                var_set('保存成功,'+str(num)+'.jpg')
            elif TYPE == 0:
                os.system('start explorer %s'%save_path)
        global All_lis
        self.__bro()
        self.icon = r'd:/ico/bitbug_favicon.ico'
        root = self.root
        root.title('壁纸更换软件')
        root.minsize(600,400)
        root.iconbitmap(self.icon)
        self.var = StringVar(root)
        menu = Menu(root,tearoff=False)
        save_menu = Menu(root,tearoff=False)
        menu.add_command(label='修改默认配置',command=self.mu_file)
        menu.add_command(label='添加存在url组',command=self.__read)
        menu.add_command(label='随机生成壁纸',command=lambda :self.get_url_set(All_lis.pop()) if len(All_lis) > 0 else var_set('等待获取'))
        menu.add_command(label='删除url组文件',command=lambda :[os.remove(url_path),var_set('删除成功'),self.T1.delete('0.0',END)] if os.path.isfile(url_path) else var_set('不存在文件'))
        save_menu.add_command(label='保存当前壁纸图片',command=lambda :__save(1))
        save_menu.add_command(label='打开图片路径',command=lambda :__save(0))
        menu.add_cascade(label='保存',menu=save_menu)
        root.config(menu=menu)
        self.time_get()
        self.var.set('当前状态:无')
        Label(root,textvariable=self.var).pack()
        Label(root,text='当前图片url组').place(y=5,x=100)
        self.T1 = Text(root,width=40,height=20)
        self.T1.place(y=30,x=10)
        Label(root,text='指定url设置').place(x=115,y=300)
        self.E1 = Entry(root)
        self.E1.place(x=75,y=325)
        Button(root,text='点击执行',command=lambda :self.get_url_set(self.E1.get())).place(x=120,y=350)
        Label(root,text='指定搜索内容').place(x=380,y=5)
        self.E2 = Entry(root)
        self.E2.place(x=350,y=30)
        Button(root,text='开始搜索链接,添加url组',command=_run).place(x=350,y=60)
        Label(root,text='切换过的url').place(x=380,y=95)
        self.T2 = Text(root,width=25,height=10)
        self.T2.place(x=335,y=120)
        Button(root,text='生成log_html浏览',command=lambda :add_html(self.T2) if self.T2.get('0.0',END).strip() else None).place(x=360,y=270)
        Button(root,text='生成url_html浏览',command=lambda :add_html(self.T1) if self.T1.get('0.0',END).strip() else None).place(x=362,y=310)

if __name__ == '__main__':
    MAIN()