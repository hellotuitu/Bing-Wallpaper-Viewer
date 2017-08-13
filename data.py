    # coding=utf-8
import urllib2
import datetime
from PIL import Image
from bs4 import BeautifulSoup

source_url = 'https://bingwallpaper.com/CN/%s.html'


# 给定日期 获取图片数据
def get_image_data(date):
    date_str = str(date).replace('-', '')
    html = urllib2.urlopen(source_url % date_str).read()
    bs = BeautifulSoup(html, 'html.parser')
    img = bs.select('#photos > div > div.imgContainer > img')
    word = bs.select('#photos > div > div.panel-overlay > p').pop().get_text()
    # src = 'https:' + img.pop().get('src')
    raw_src = img.pop().get('src')
    src = 'http://cdn.nanxiongnandi.com/bing' + raw_src[raw_src.rindex('/'):]
    print src
    pic = urllib2.urlopen(src, timeout = 3).read()
    return [pic, word]


# 给定数据和路径 保存图片
def save_image_data(pic, full_path):
    img_file = open(full_path, 'wb')
    img_file.write(pic)
    img_file.flush()
    img_file.close()
    # img_file.


# 裁剪图像
def resize_image(w, h, w_box, h_box, pil_image):
    f1 = 1.0 * w_box / w  # 1.0 forces float division in Python2
    f2 = 1.0 * h_box / h
    factor = min([f1, f2])
    width = int(w * factor)
    height = int(h * factor)
    return pil_image.resize((width, height), Image.ANTIALIAS)
