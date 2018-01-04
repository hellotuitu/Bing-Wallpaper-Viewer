#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import time
import os
try:
    #print(os.path.abspath(os.path.dirname(__file__)))
    os.chdir(os.path.abspath(os.path.dirname(__file__)))
    import gui
    import kernel

    gui.Bing(kernel.Kernel())
except Exception as why:
    print(why)
    time.sleep(10)
    
