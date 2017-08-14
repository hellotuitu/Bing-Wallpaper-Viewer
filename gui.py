# -*- coding: UTF-8 -*-
from Tkinter import *
import tkFileDialog
from tkSimpleDialog import askstring
import tkMessageBox
import thread
import platform

class Bing:
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

        self.image_label.bind("<ButtonPress-3>", self.right_key_handler)
        self.image_label.bind("<ButtonPress-1>", self.left_key_handler)

        self.image_label.grid(row=0, column=0, columnspan=3)
        self.pre_button.grid(row=1, column=0)
        self.description_label.grid(row=1, column=1)
        self.next_button.grid(row=1, column=2)

        self.init_set()
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
            self.date_v.set(str(self.kernel.current_date))
            if platform.system() != 'Windows':
                self.root.title(self.kernel.current_description)
        except BaseException:
            print 'error'
            return False
        else:
            return True

    def multithread(self, threadName, delay):
        self.next_button['state'] = DISABLED
        self.pre_button['state'] = DISABLED

        self.date_v.set('loading...')
        if not self.update():
            self.date_v.set('fail to load!')

        self.next_button['state'] = NORMAL
        self.pre_button['state'] = NORMAL

    def pre_button_handler(self):
        self.kernel.pre_date()
        thread.start_new_thread(self.multithread, ("Thread-1", 0,))
        # self.update()

    def next_button_handler(self):
        self.kernel.next_date()
        thread.start_new_thread(self.multithread, ("Thread-1", 0,))

    def save_file_handler(self):
        self.kernel.save_current_image(str(self.kernel.current_date) + '.jpg')

    def save_file_to_handler(self):
        filename = tkFileDialog.askdirectory()
        self.kernel.save_current_image(filename + '/' + str(self.kernel.current_date) + '.jpg')

    def ask_date_to_handler(self):
        input_date = askstring('Bing Wallpaper Viewer', '输入日期', initialvalue=str(self.kernel.current_date))
        self.kernel.goto_date(input_date)
        thread.start_new_thread(self.multithread, ("Thread-1", 0,))

    def right_key_handler(self, event):
        self.menubar.post(event.x_root, event.y_root)

    def left_key_handler(self, event):
        self.menubar.unpost()
