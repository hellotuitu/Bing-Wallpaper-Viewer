# -*- coding: UTF-8 -*-
import os
import _thread as thread
from tkinter import *
from tkinter import filedialog as tkFileDialog
from tkinter.simpledialog import askstring


# import platform
# from tkSimpleDialog import askstring
# import tkFileDialog
# from tkinter import messagebox as tkMessageBox
# import tkMessageBox

class Bing:
    """user interface"""
    def __init__(self, kernel):
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

        self.image_label.grid(row=0, column=0, columnspan=3)
        self.pre_button.grid(row=1, column=0)
        self.description_label.grid(row=1, column=1)
        self.next_button.grid(row=1, column=2)

        self.init_set()
        self.root.resizable(True, True)
        self.root.mainloop()

    def init_set(self):
        self.root.title('Bing Wallpaper Viewer')
        self.kernel.init_kernel()
        self.image_label['image'] = self.kernel.current_image
        thread.start_new_thread(self.multithread, ("Thread-1", 0,))

    def update(self):
        try:
            self.kernel.update_data()
            self.image_label['image'] = self.kernel.current_image

            desp = "{}: {}".format(self.kernel.current_date,
                                   self.kernel.current_description.split('(')[0]).center(40)
            self.date_v.set(desp)

        except BaseException as why:
            self.kernel.current_date = self.kernel.last_date
            why = str(why).center(40) if len(str(why)) <= 40 else str(why)[0:37] + '...'
            self.date_v.set(why)
            self.description_label['fg'] = 'red'

    def multithread(self, thread_name, delay):
        self.description_label['fg'] = 'black'
        self.pre_button['state'] = DISABLED
        self.next_button['state'] = DISABLED
        self.date_v.set('loading...')

        self.update()

        self.next_button['state'] = NORMAL
        self.pre_button['state'] = NORMAL

    def pre_button_handler(self):
        if self.pre_button['state'] == NORMAL:
            self.kernel.pre_date()
            thread.start_new_thread(self.multithread, ("Thread-1", 0,))

    def next_button_handler(self):
        if self.next_button['state'] == NORMAL:
            self.kernel.next_date()
            thread.start_new_thread(self.multithread, ("Thread-1", 0,))

    def save_file_handler(self):
        path = str(self.kernel.current_date) + '.jpg'
        if os.path.isfile(path):
            self.date_v.set('图像已经保存过了')
        else:
            self.kernel.save_current_image(path)
            self.date_v.set('保存成功')

    def save_file_to_handler(self):
        filename = tkFileDialog.askdirectory()
        path = filename + '/' + str(self.kernel.current_date) + '.jpg'
        if os.path.isfile(path):
            self.date_v.set('图像已经保存过了')
        else:
            self.kernel.save_current_image(path)
            self.date_v.set('保存成功')

    def ask_date_to_handler(self):
        input_date = askstring('Bing Wallpaper Viewer', '输入日期', initialvalue=str(self.kernel.current_date))
        self.kernel.goto_date(input_date)
        thread.start_new_thread(self.multithread, ("Thread-1", 0,))

    def right_key_handler(self, event):
        self.menubar.post(event.x_root, event.y_root)

    def left_key_handler(self, event):
        self.menubar.unpost()

    @staticmethod
    def event_wrap(func):
        def handle(event):
            func()

        return handle


if __name__ == '__main__': pass
