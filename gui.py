#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import os
import datetime
import threading
from tkinter import *
from tkinter import filedialog as tkFileDialog
from tkinter.simpledialog import askstring
from PIL import ImageTk


class Bing:
    """user interface"""

    def __init__(self, kernel):
        # declare some attrubutes
        self.size = (0, 0)
        self.image = None
        self.init_width = 1000
        self.resize_counter = 0
        self.toggle = True
        self.root = root = Tk()
        self.kernel = kernel

        self.image_label = Label(root)
        self.date_v = StringVar(root)
        self.description_label = Label(root, textvariable=self.date_v)
        self.pre_button = Button(root, text=' < pre ', command=self.pre_button_handler)
        self.next_button = Button(root, text=' next > ', command=self.next_button_handler)

        self.menubar = Menu(self.root, tearoff=False)
        self.menubar.add_command(label='保存到当前文件夹下', command=self.save_file_handler)
        self.menubar.add_separator()
        self.menubar.add_command(label='保存到指定的文件夹下', command=self.save_file_to_handler)
        self.menubar.add_separator()
        self.menubar.add_command(label='跳转到指定日期的图片', command=self.ask_date_to_handler)

        # mouse event
        self.image_label.bind("<ButtonPress-3>", self.right_key_handler)
        self.image_label.bind("<ButtonPress-1>", self.left_key_handler)

        # keyboard event
        self.root.bind('<Up>', self.event_wrap(self.pre_button_handler))
        self.root.bind('<Left>', self.event_wrap(self.pre_button_handler))
        self.root.bind('<Right>', self.event_wrap(self.next_button_handler))
        self.root.bind('<Down>', self.event_wrap(self.next_button_handler))
        self.root.bind('<Control-s>', self.event_wrap(self.save_file_handler))
        # full screen toggle
        self.root.bind('<Escape>', self.event_wrap(self.toggle_fullscreen))

        # window resize event
        self.root.bind('<Configure>', self.on_resize_handler)

        for col in range(3):
            Grid.columnconfigure(self.root, col, weight=1)
        for row in range(2):
            Grid.rowconfigure(self.root, row, weight=1)

        self.image_label.grid(row=0, column=0, columnspan=3, sticky=N + S + E + W)
        self.pre_button.grid(row=1, column=0, sticky=N + S + E + W)
        self.description_label.grid(row=1, column=1, sticky=N + S + E + W)
        self.next_button.grid(row=1, column=2, sticky=N + S + E + W)

        self.init_set()
        # make it can not be resizable
        # self.root.resizable(False, False)
        self.root.resizable(True, True)
        # root.geometry('1000x590+500+200')
        self.root.mainloop()

    def init_set(self):
        self.root.title('Bing Wallpaper Viewer')
        w_box = h_box = self.init_width
        w, h = self.kernel.current_image.size
        image_resized = self.kernel.resize_image(w, h, w_box, h_box, self.kernel.current_image)
        self.image = ImageTk.PhotoImage(image_resized)
        self.image_label['image'] = self.image
        threading.Thread(target=self.back_thread, args=(self.kernel.current_date,)).start()

    def update(self, date):
        try:
            self.kernel.update_data_with_date(date)
            label_width = self.image_label.winfo_width()
            if hasattr(self, 'margin'):
                h_box = w_box = label_width - self.margin
            else:
                h_box = w_box = self.init_width
            w, h = self.kernel.current_image.size
            image_resized = self.kernel.resize_image(w, h, w_box, h_box, self.kernel.current_image)
            # self.image.paste(image_resized)
            self.image = ImageTk.PhotoImage(image_resized)
            self.image_label['image'] = self.image
            desp = "{}: {}".format(self.kernel.current_date,
                                   self.kernel.current_description.split('(')[0]).center(40)
            self.date_v.set(desp)

        except BaseException as why:
            print(why)
            why = str(why).center(40) if len(str(why)) <= 40 else str(why)[0:37] + '...'
            self.date_v.set(why)
            self.description_label['fg'] = 'red'

    def back_thread(self, date=None):
        self.description_label['fg'] = 'black'
        self.pre_button['state'] = DISABLED
        self.next_button['state'] = DISABLED
        self.date_v.set('loading...')

        self.update(date)

        self.next_button['state'] = NORMAL
        self.pre_button['state'] = NORMAL

    def pre_button_handler(self):
        if self.pre_button['state'] != DISABLED:
            threading.Thread(target=self.back_thread, args=(self.kernel.pre_date(),)).start()

    def next_button_handler(self):
        if self.next_button['state'] != DISABLED:
            threading.Thread(target=self.back_thread, args=(self.kernel.next_date(),)).start()

    def ask_date_to_handler(self):
        if self.pre_button['state'] != DISABLED:
            input_date = askstring('Bing Wallpaper Viewer', '输入日期', initialvalue=str(self.kernel.current_date))
            date = datetime.datetime.strptime(input_date, "%Y-%m-%d").date()
            threading.Thread(target=self.back_thread, args=(date,)).start()

    def save_file(self, path):
        if os.path.isfile(path):
            self.date_v.set('图像已经保存过了')
        else:
            try:
                if self.kernel.save_current_image(path):
                    self.date_v.set('保存成功')
                else:
                    self.date_v.set('保存失败')
            except:
                self.date_v.set('保存失败')

    def save_file_handler(self):
        path = str(self.kernel.current_date) + '.jpg'
        self.save_file(path)

    def save_file_to_handler(self):
        filename = tkFileDialog.askdirectory()
        path = filename + '/' + str(self.kernel.current_date) + '.jpg'
        self.save_file(path)

    def right_key_handler(self, event):
        self.menubar.post(event.x_root, event.y_root)

    def left_key_handler(self, event):
        self.menubar.unpost()

    def on_resize_handler(self, event):
        self.resize_counter += 1
        threading.Thread(target=self.on_resize, args=(event, self.resize_counter,)).start()

    def on_resize(self, event, counter):
        # if window just move, ignore the event
        if self.size == (self.image_label.winfo_width(), self.image_label.winfo_height()):
            return None
        self.size = (self.image_label.winfo_width(), self.image_label.winfo_height())

        label_width = self.image_label.winfo_width()
        # label still not initialized
        if label_width < 10:
            return None

        # set margin
        if not hasattr(self, 'margin'):
            self.margin = label_width - self.init_width

        # resize image
        h_box = w_box = label_width - self.margin
        w, h = self.kernel.current_image.size

        if counter != self.resize_counter:
            # if more events happen
            # just do nothing
            return None

        image_resized = self.kernel.resize_image(w, h, w_box, h_box, self.kernel.current_image)
        if (self.image.width(), self.image.height()) == image_resized.size:
            # if size does not change
            return None
        self.image = ImageTk.PhotoImage(image_resized)
        self.image_label['image'] = self.image

    def toggle_fullscreen(self):
        self.root.attributes("-fullscreen", self.toggle)
        if self.toggle:
            self.pre_button.grid_remove()
            self.next_button.grid_remove()
            self.description_label.grid_remove()
            self.__margin = self.margin
            self.margin = 0
        else:
            self.pre_button.grid(row=1, column=0, sticky=N + S + E + W)
            self.description_label.grid(row=1, column=1, sticky=N + S + E + W)
            self.next_button.grid(row=1, column=2, sticky=N + S + E + W)
            self.root.geometry("1000x600+0+0")
            self.margin = self.__margin
        self.toggle = bool(not self.toggle)

    @staticmethod
    def event_wrap(func):
        def handle(event):
            func()

        return handle


if __name__ == '__main__': pass
