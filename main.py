#!/usr/bin/env python3
# encoding: utf-8
# author: Vincent
# refer: https://github.com/vc5


from pathlib import Path
import requests
from bs4 import BeautifulSoup
from tkinter import filedialog, Tk
import re
from urllib.parse import urlparse, unquote

BASE_PATH = Path(__file__).parent
PDF_PATH = BASE_PATH / 'pdf'
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'


root = Tk()
root.withdraw()


class XueShu:
    index_url = 'https://xueshu.baidu.com/'

    def __init__(self):
        self.sess = requests.Session()
        self.sess.get(self.index_url)
        self.sess.headers['User-Agent'] = UA
        self.pdf_path = PDF_PATH

    def search(self, qs):
        url = 'http://xueshu.baidu.com/s'
        p = {'wd': qs, 'sc_hit': '1'}
        r = self.sess.get(url=url, params=p)
        soup = BeautifulSoup(r.content, 'html.parser')
        # c = soup.select('a.sc_q')
        c = soup.select('div.result')
        # self.fetch_enw(c[0])
        return c

    def fetch_enw(self, cite: BeautifulSoup):
        url = 'http://xueshu.baidu.com/u/citation'
        title = cite.find(attrs={'data-click': "{'button_tp':'title'}"}).text
        print('正在查询文献【%s】的引文' % title)
        # 来源列表
        sc_list = cite.select('div.sc_allversion  a.v_source')
        # source_url = sc_list[0].get('href').strip()
        # parsed_source_url = urlparse(source_url)
        # if parsed_source_url.netloc == 'xueshu.baidu.com':
        #     # true_sc_url_pat =r'&sc_vurl=(.*?)&'
        #     source_url = re.findall(r'&sc_vurl=(.*?)&',source_url)[0]
        #     source_url = unquote(source_url)
        # print(source_url)
        cite_btn = cite.select('a.sc_q')[0]
        source_url = cite_btn.get('data-link')
        p_sign = cite_btn.get('data-sign')
        # diversion为引用格式
        p = {'url': source_url, 'sign': p_sign,
             'diversion': '6511123030104604673', 't': 'enw'}
        r = self.sess.get(url, params=p)

        # with open(BASE_PATH / filename, 'wb') as f:
        #     f.write(r.content)
        # print(r.content.decode())
        return r.content

    def fetch_all(self, pdf_path: Path = PDF_PATH):
        filename = 'endnote.enw'
        buff = b''
        article_list = sorted(pdf_path.glob('**/*.pdf'))
        print('在文件夹%s中共发现%s篇文献' % (pdf_path, len(article_list)))
        for article in pdf_path.glob('**/*.pdf'):
            try:
                source = self.search(article.name.split('.')[:-1])[0]
                buff = buff + self.fetch_enw(source) + b'\n\n'

            except IndexError:
                print('未检索到【%s】' % article.name)
        with open(BASE_PATH / filename, 'wb') as f:
            f.write(buff)

    def fetch_info_page(self):
        pass

    def update_pdf_path(self):
        dir_str = filedialog.askdirectory()
        self.pdf_path = Path(dir_str)

    def save(self, filename):
        pass


def main():
    bot = XueShu()
    bot.update_pdf_path()
    bot.fetch_all(bot.pdf_path)


if __name__ == '__main__':
    main()
