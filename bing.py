# -*- coding: utf-8 -*-
import urllib2
import datetime
import io
from PIL import Image
from bs4 import BeautifulSoup


response = urllib2.urlopen("https://bingwallpaper.com/CN/20170805.html")
html = response.read()
bs = BeautifulSoup(html, 'html.parser')
li = bs.select('#photos > div > div.imgContainer > img')
print li[0].get('src')
pic = urllib2.urlopen('https:' + li[0].get('src')).read()

data_stream = io.BytesIO(pic)
# local=open('tmp.png','wb')
# local.write(pic)
# local.close()
image = Image.open(data_stream)
w_box = 1000
h_box = 1000
w, h = image.size
# image_resized = resize(w, h, w_box, h_box, image)
# image.show()
image.show()
print "hello world"