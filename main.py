#!/usr/bin/env python3
# encoding: utf-8
# author: Vincent
# refer: https://github.com/vc5


from pathlib import Path
import requests
from bs4 import BeautifulSoup
from tkinter import filedialog

BASE_PATH = Path(__file__).parent
PDF_PATH = BASE_PATH /'pdf'
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'


class XueShu:
    index_url = 'https://xueshu.baidu.com/'
    

    def __init__(self):
        self.sess = requests.Session()
        self.sess.get(self.index_url)
        self.sess.headers['User-Agent'] = UA
        self.pdf_path = PDF_PATH


    def search(self,qs):
        url = 'http://xueshu.baidu.com/s'
        p = {'wd':qs,'sc_hit':'1'}
        r = self.sess.get(url=url,params = p).content
        soup = BeautifulSoup(r,'lxml')
        # c = soup.select('a.sc_q')
        c = soup.select('div.result')
        self.fetch_enw(c[0])
        return c

    def fetch_enw(self,cite:BeautifulSoup):
        url = 'http://xueshu.baidu.com/u/citation'
        title = cite.find(attrs={'data-click':"{'button_tp':'title'}"}).text
        # 来源列表
        sc_list = cite.select('div.sc_allversion  a.v_source')
        source_url = sc_list[0].get('href').strip()
        
        # print(source_url)
        cite_btn = cite.select('a.sc_q')[0]
        # source_url = cite.get('data-link')
        p_sign = cite_btn.get('data-sign')
        # diversion为引用格式
        p = {'url':source_url,'sign':p_sign,'diversion':'6511123030104604673','t':'enw'}
        r = self.sess.get(url,params=p)
        filename = '{}.enw'.format(title)
        with open(BASE_PATH / filename,'wb') as f:
            f.write(r.content)
        return r.text

    def fetch_all(self,pdf_path:Path = PDF_PATH):
        for article in pdf_path.glob('*.pdf'):
            self.search(article.name.split('.')[:-1])
    

    def update_pdf_path(self):
        self.pdf_path = filedialog.askdirectory()

def main():
    bot = XueShu()
    bot.fetch_all()

if __name__ == '__main__':
    main()
    