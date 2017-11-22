import urllib2
import datetime
import io
from Tkconstants import NONE
from PIL import Image, ImageTk
from bs4 import BeautifulSoup
import sys, os

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class Kernel:
    def __init__(self):
        self.source_url = 'https://bingwallpaper.com/CN/%s.html'
        self.current_date = datetime.date.today() - datetime.timedelta(1)
        self.last_date = self.current_date
        self.current_image = NONE
        self.current_raw_image = NONE
        self.current_description = NONE

    def init_kernel(self):
        image = Image.open(resource_path('default.jpg'))
        w_box = 1000
        h_box = 1000
        w, h = image.size
        image_resized = self.resize_image(w, h, w_box, h_box, image)
        self.current_image = ImageTk.PhotoImage(image_resized)

    def get_data(self):
        date_str = str(self.current_date).replace('-', '')
        print self.source_url % date_str
        html = urllib2.urlopen(self.source_url % date_str, timeout=10).read()
        bs = BeautifulSoup(html, 'html.parser')
        a = bs.find_all('a', attrs={'href': '%s.html' % date_str}).pop()
        img = a.find_all('img').pop()
        word = img.get('alt')
        raw_src = img.get('src')
        src = 'http://cdn.nanxiongnandi.com/bing' + raw_src[raw_src.rindex('/'):]
        print src
        pic = urllib2.urlopen(src, timeout=3).read()
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
    import requests
    print requests.get('https://www.baidu.com')