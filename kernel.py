#!/usr/bin/env python3
# -*- coding: utf-8
import datetime
import io
import requests
from tkinter.constants import NONE
from PIL import Image
from bs4 import BeautifulSoup


class Kernel:
    """kernel of the viewer

    change resorce to http://bingwallpaper.anerg.com/cn/
    """
    def __init__(self):
        # set current day to the day before, in case today's wallpaper is not availiable
        self.current_date = datetime.date.today() - datetime.timedelta(1)
        # default image
        self.current_image = Image.new('RGB', (1366, 768), 'black')
        self.current_description = None

    def get_data(self, date):
        try:
            month = str(date.month).zfill(2)
            year = date.year
            source = 'http://bingwallpaper.anerg.com/cn/{}{}'.format(year, month)
            index = requests.get(source, timeout=5)
            parser = BeautifulSoup(index.content, 'html.parser')
            containers = parser.find_all('div', attrs={'class': 'panel'})
            imgs = []
            for c in containers:
                imgs.append(c.find('img'))
            imgs.reverse()
            current_img = imgs[date.day - 1]
            word = current_img.get('alt')
            pic = requests.get(current_img.get('src'), timeout=5).content
            data_stream = io.BytesIO(pic)
            image = Image.open(data_stream)
        except Exception as why:
            raise Exception('获取数据失败： {}'.format(why))
        return [image, word]

    def update_data_with_date(self, date):
        self.current_image, self.current_description = self.get_data(date)

        # update current date if all success
        self.current_date = date

    def save_current_image(self, full_path):
        if self.current_description:
            self.current_image.save(full_path)
            return True
        else:
            return False

    def next_date(self):
        return self.current_date + datetime.timedelta(1)

    def pre_date(self):
        return self.current_date - datetime.timedelta(1)

    @staticmethod
    def resize_image(w, h, w_box, h_box, pil_image):
        f1 = 1.0 * w_box / w  # 1.0 forces float division in Python2
        f2 = 1.0 * h_box / h
        factor = min([f1, f2])
        width = int(w * factor)
        height = int(h * factor)
        return pil_image.resize((width, height), Image.ANTIALIAS)


if __name__ == '__main__':
    # https://www.bing.com/HPImageArchive.aspx?format=js&index=1&n=1
    html = requests.get('http://bingwallpaper.anerg.com/201710')
    s = BeautifulSoup(html.content, 'html.parser')
    s = s.find_all('div', attrs={'class': 'panel'})
    for i in s:
        print(i.find('a').get('href'))

    print(len(s))

    a = '111'
    a.center()
