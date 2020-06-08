from static.img_main import img_main
import pprint

class baidu_img(img_main):

    url = 'https://image.baidu.com/'

    def run(self,title):
        self.title = title
        self.__url = 'https://image.baidu.com/search/acjson'
        self.lis = []

    def __next__(self):
        if self.now != True:return None
        params = {
            'tn': 'resultjson_com',
            'ipn': 'rj',
            'ct': '201326592',
            'fp': 'result',
            'queryWord': self.title,
            'cl': '2',
            'word': self.title,
            'width': self.width,
            'height': self.height,
            'pn': (self.num-1)*30,
            'rn': 30,
        }
        resp = self.get_data(
            url = self.__url,
            headers = self.headers,
            params = params,
        )
        self.num += 1
        if resp != None and resp.status_code == 200:
            data = resp.json().get('data')
            lis = [i.get('replaceUrl')[-1].get('ObjUrl') for i in data if i and i.get('hoverURL') not in self.lis]
            self.lis.extend(lis)
            if len(lis) == 0:self.now = False
            yield lis
        else:
            self.now = False
            yield None

if __name__ == '__main__':
    b = baidu_img('栗山未来')
    b.height = 1200
    while 1:
        input('>>')
        for i in next(b):
            print(i)