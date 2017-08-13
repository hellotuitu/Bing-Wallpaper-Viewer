# -*- coding: UTF-8 -*-

from Tkinter import *
from PIL import Image, ImageTk
import data
import datetime
import io
from FileDialog import LoadFileDialog
import tkFileDialog
# from tkinter.simpledialog  import *
from tkSimpleDialog import askstring
import tkMessageBox
import _thread
import time

def hello(threadName, delay):
    next_bt['state'] = DISABLED
    time.sleep(3)
    update()
    next_bt['state'] = NORMAL

def next_button():
    global current_date, data_v
    date_v.set('loading...')

    current_date = current_date + datetime.timedelta(1)
    # update()
    _thread.start_new_thread( hello, ("Thread-1", 3, ) )
    print 'done'


def pre_button():
    global current_date, v, img_label, root, image, current_pic, current_word
    print 'pre button'
    # _thread.start_new_thread( hello, ("Thread-1", 0, ) )
    current_date = current_date - datetime.timedelta(1)
    pic, word = data.get_image_data(current_date)
    current_pic = pic
    current_word = word
    img = process_image(pic)
    tk_img = ImageTk.PhotoImage(img)
    # img_label.image = tk_img
    # root.update_idletasks()
    img_label.configure(image=tk_img)
    image = tk_img  # keep a reference
    date_v.set(str(current_date))
    root.title(word)
    v.set(word)


def process_image(pic):
    data_stream = io.BytesIO(pic)
    image = Image.open(data_stream)
    w_box = 1000
    h_box = 1000
    w, h = image.size
    image_resized = data.resize_image(w, h, w_box, h_box, image)
    return image_resized


def update():
    global current_date, v, img_label, root, image, current_pic, current_word
    if current_date >= datetime.date.today():
        current_date = datetime.date.today() - datetime.timedelta(1)
        tkMessageBox.showwarning('Bing Wallpaper Viewer', '该日期不可达!')
        return NONE
    pic, word = data.get_image_data(current_date)
    current_pic = pic
    current_word = word
    img = process_image(pic)
    tk_img = ImageTk.PhotoImage(img)
    # img_label.image = tk_img
    # root.update_idletasks()
    img_label.configure(image=tk_img)
    image = tk_img  # keep a reference
    date_v.set(str(current_date))
    root.title(word)
    v.set(word)

current_date = datetime.date.today() - datetime.timedelta(1)
current_pic = NONE
current_word = NONE
# word_label = NONE
# img_label = NONE
# text = StringVar()

image = NONE
root = Tk()
root.title('Bing Wallpaper Viewer')
v = StringVar(root)
date_v = StringVar(root)
date_v.set(str(current_date))
pic, word = data.get_image_data(current_date)
current_pic = pic
current_word = word
img = process_image(pic)
tk_img = ImageTk.PhotoImage(img)
# word_label = Label(root, textvariable=v)
# word_label.pack()
img_label = Label(root, image=tk_img)
img_label.grid(row=0, column=0, columnspan=3)
# img_label.pack()
pre_bt = Button(root, text=' < pre ', command=pre_button)
pre_bt.grid(row=1, column=0)#.pack(side=LEFT)
date_label = Label(root, textvariable=date_v,  anchor='center', width = 100).grid(row=1, column=1)#.pack(side=LEFT)
next_bt = Button(root, text=' next > ', command=next_button)
next_bt.grid(row=1, column=2)#.pack(side=RIGHT)

menubar=Menu(root,tearoff=False)
def save_file_command():
    data.save_image_data(current_pic, str(current_date) + '.jpg')

def save_file_to():
    filename = tkFileDialog.askdirectory()
    # fd = LoadFileDialog(root) # 创建打开文件对话框
    # filename = fd.go() # 显示打开文件对话框，并获取选择的文件名称
    data.save_image_data(current_pic, filename + '/' + str(current_date) + '.jpg')
    # print filename

def ask_date():
    global current_date
    r = askstring('Bing Wallpaper Viewer', '输入日期', initialvalue = str(current_date))
    current_date = datetime.datetime.strptime(r, "%Y-%m-%d").date()
    update()

menubar.add_command(label='保存到当前文件夹下', command=save_file_command)
menubar.add_separator()
menubar.add_command(label='保存到指定的文件夹下', command=save_file_to)
menubar.add_separator()
menubar.add_command(label='跳转到指定日期的图片', command=ask_date)

# frame=Frame(root,
#             width=100,height=100,
#             background='red')
# frame.grid()


def rightKey(event):
    menubar.post(event.x_root, event.y_root)
def leftKey(event):
    print 'left button'
    menubar.unpost()
def leave(event):
    print 'leave'
    # menubar.unpost()

img_label.bind("<ButtonPress-3>",rightKey)
img_label.bind("<ButtonPress-1>",leftKey)
# img_label.bind("<Leave>",leave)
#frame框绑定鼠标右键
# frame.bind()

root.mainloop()




# # 创建两个列表
# li = ['C', 'python', 'php', 'html', 'SQL', 'java']
# movie = ['CSS', 'jQuery', 'Bootstrap']
# listb = Listbox(root)  # 创建两个列表组件
# listb2 = Listbox(root)
# for item in li:  # 第一个小部件插入数据
#     listb.insert(0, item)
#
# for item in movie:  # 第二个小部件插入数据
#     listb2.insert(0, item)
# Button(root, text='Hello Button', command=helloButton).pack()
# listb.pack()  # 将小部件放置到主窗口中
# listb2.pack()
# filename = './tmp.png'
# img = ImageTk.PhotoImage(file=filename)
# label = Label(root, image=img)
# label.pack()
# root.mainloop()  # 进入消息循环
