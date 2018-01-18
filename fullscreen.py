# coding: utf-8
# 2018/1/18, created by hello

import tkinter as tk


class FullScreenApp(object):
    def __init__(self, master, **kwargs):
        self.toggle = True
        self.master = master
        pad = 3
        self._geom = '200x200+0+0'
        master.geometry("{0}x{1}+0+0".format(
            master.winfo_screenwidth() - pad, master.winfo_screenheight() - pad))
        master.bind('<Escape>', self.toggle_geom)

    def toggle_geom(self, event):
        # geom = self.master.winfo_geometry()
        # print(geom, self._geom)
        # self.master.geometry(self._geom)
        # self._geom = geom
        self.master.attributes("-fullscreen", self.toggle)
        self.toggle = bool(not self.toggle)

root = tk.Tk()
app = FullScreenApp(root)
root.mainloop()
