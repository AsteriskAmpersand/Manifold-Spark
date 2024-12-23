# -*- coding: utf-8 -*-
"""
Created on Mon Dec 16 03:10:53 2024

@author: Asterisk
"""

import win32gui, win32con, os
from pathlib import Path
from tkinter import Tk
from tkinter.filedialog import askdirectory
# shows dialog box and return the path
import sys,os

if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable)
elif __file__:
    application_path = os.path.dirname(__file__)


pathmem = application_path


def get_folder():
    global pathmem
    path = askdirectory(title='Select Folder',initialdir = pathmem)
    if path:
        pathmem = path
    return path

def _get_file(multi = False, save = False, name = ""):
    global pathmem
    file_types = "Json Files\0*.json\0Other file types\0*.*\0"
    customfilter = ""
    multiflag = win32con.OFN_ALLOWMULTISELECT if multi else 0
    try:
        if save:
            fname, customfilter, flags = win32gui.GetSaveFileNameW(
                InitialDir=pathmem,
                Flags= multiflag | win32con.OFN_EXPLORER | win32con.OFN_NOCHANGEDIR,
                DefExt="json",
                Title="Select Files",
                Filter=file_types,
                CustomFilter=customfilter,
                FilterIndex=1,
                File = name
                )
        else:
            fname, customfilter, flags = win32gui.GetOpenFileNameW(
                InitialDir=pathmem,
                Flags= multiflag | win32con.OFN_EXPLORER | win32con.OFN_NOCHANGEDIR,
                DefExt="json",
                Title="Select Files",
                Filter=file_types,
                CustomFilter=customfilter,
                FilterIndex=1,
                File = name
                )
    except:
        fname = ""
    if "\0" in fname:
        pathmem = fname.split("\0")[0]
    else:
        pathmem = str(Path(fname).parent.resolve())
    return fname

def get_file(save = False,name = ""):
    fname = _get_file(save = save,name = name)
    return fname.replace("\0","\\") if fname else None

def get_files():
    fnames = _get_file(True)
    if fnames:
        ret = fnames.split("\0")
        if len(ret) == 1:
            return ret
        base = ret[0]
        return [base +"\\"+path for path in ret[1:]]
