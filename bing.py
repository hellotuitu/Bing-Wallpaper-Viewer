#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
import os
try:
    # set work dir
    os.chdir(os.path.abspath(os.path.dirname(__file__)))
    import gui
    import kernel

    gui.Bing(kernel.Kernel())
except Exception as why:
    # if something goes wrong, show it to users
    print(why)
    time.sleep(3)
