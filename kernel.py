# -*- coding: utf-8
import datetime
import io
from tkinter.constants import NONE
from PIL import Image, ImageTk
from bs4 import BeautifulSoup
import sys, os
import requests


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class Kernel:
    """kernel of the viewer"""
    def __init__(self):
        # change resorce to http://bingwallpaper.anerg.com/cn/
        # it's a sad story because bing only provides no more than 7 days' wallpapers

        # set current day to the day before, in case today's wallpaper is not availiable
        self.current_date = datetime.date.today() - datetime.timedelta(1)
        self.last_date = self.current_date
        self.current_image = NONE
        self.current_raw_image = NONE
        self.current_description = NONE

    def init_kernel(self):
        # image = Image.open(resource_path('default.jpg'))
        w_box = 1000
        h_box = 1000
        image = Image.new('RGB', (1366, 768), 'black')
        w, h = image.size
        image_resized = self.resize_image(w, h, w_box, h_box, image)
        self.current_image = ImageTk.PhotoImage(image_resized)

    def get_data(self):
        try:
            month = str(self.current_date.month).zfill(2)
            year = self.current_date.year
            source = 'http://bingwallpaper.anerg.com/cn/{}{}'.format(year, month)
            index = requests.get(source, timeout=5)
            parser = BeautifulSoup(index.content, 'html.parser')
            containers = parser.find_all('div', attrs={'class': 'panel'})
            imgs = []
            for c in containers:
                imgs.append(c.find('img'))
            imgs.reverse()
            current_img = imgs[self.current_date.day - 1]
            word = current_img.get('alt')
            pic = requests.get(current_img.get('src'), timeout=5).content
        except Exception as why:
            raise Exception('获取数据失败： {}'.format(why))
        return [pic, word]

    def update_data(self):
        self.current_raw_image, self.current_description = self.get_data()
        self.process_image()

    def process_image(self):
        data_stream = io.BytesIO(self.current_raw_image)
        image = Image.open(data_stream)
        w_box = 1000
        h_box = 1000
        w, h = image.size
        image_resized = self.resize_image(w, h, w_box, h_box, image)
        self.current_image = ImageTk.PhotoImage(image_resized)

    def save_current_image(self, full_path):
        img_file = open(full_path, 'wb')
        img_file.write(self.current_raw_image)
        img_file.flush()
        img_file.close()

    def next_date(self):
        self.last_date = self.current_date
        self.current_date += datetime.timedelta(1)

    def pre_date(self):
        self.last_date = self.current_date
        self.current_date -= datetime.timedelta(1)

    def goto_date(self, date_str):
        self.last_date = self.current_date
        self.current_date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()

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
