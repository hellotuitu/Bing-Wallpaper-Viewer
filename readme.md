# Bing Wallpaper Viewer
someday, I certainly feel Bing's wallpaper is
good when I surf in the Interet.But, bing only allows
users to download today's wallpaper and the wallpaper
has watermelon.For this reason, I wrote this program
to view and download everyday's wallpaper from bing.

I think it will be useful if you like bing's wallpapers
too.

## Requirements

Based on python2.7.Packages imported by this program
could be found in `requirements.txt`.

## Usage

 ![bing_gui](./bing_gui.png)

like the picture above showed, in the bottom,there
are three blocks(two buttons and one label).

- `< pre`: by pressing this button, the image area will show
wallpaper the day before.
- `label`: the label shows the current day.
- `next >`: by pressing this button, the image area will show
wallpaper the day after.

if you right click in the image area, a menu will be poped out.
The menu has three buttons.
- `保存到当前文件夹`: this button allows you to save current image to 
current folder.
- `保存到指定的文件夹`: this button allows you to save current image to
folder you specified.
- `跳转到指定日期的图片`: this button allows you to view wallpaper of the
day you specified.

Just a reminder, the memu will be hidden by left click in the image area.

### How to run it

1. first, download or clone the entire project.
1. then, run command `python2 bing.py` in your terminal.

## Note

the data comes from `https://bingwallpaper.com` and `http://cdn.nanxiongnandi.com/bing`.

