# Bing Wallpaper Viewer
someday, I certainly feel Bing's wallpaper is
good when I surf in the Interet.But, bing only allows
users to download today's wallpaper and the wallpaper
has watermelon.For this reason, I wrote this program
to view and download everyday's wallpaper from bing.

I think it will be useful if you like bing's wallpapers
too.Have fun with it!

## Requirements

Based on ~~python2.7~~ Python 3.x. Packages imported by this program
could be found in `requirements.txt`.

## How to run

1. first, download or clone the entire project.
1. then, run command `python3 bing.py` in your terminal.

for convenience, I made a shortcut for this program.In fact, it's a text file,
if you want to use it, open it with any editor and fill in values I comment.
Then, give executable permission to the shortcut and copy it to desktop.
Now, you can start the program by clicking the shortcut in your desktop. 

## Features

(尬尬的英文实在是写不下去了...)

- 支持壁纸保存
- 支持查看任意一天的壁纸
- 支持方向键操作
- 支持全屏模式
- 支持壁纸随窗口大小自适应缩放

## 键盘控制

- `ctrl-s`: 保存当前图片到程序目录
- `up`or`left`: 跳转到前一天的壁纸
- `down`or`right`: 跳转到后一天的壁纸
- `esc`: 进入或退出全屏模式

## Note

Data comes from `http://bingwallpaper.anerg.com`

## TODO

- [x] change to python 3.x
- [x] handle exceptions and display them
- [x] add keyboard control
- [x] add full screen mode
- [x] make window size changable
- [ ] design a new way to display messages in full screen mode
