# -*- coding: utf-8 -*-
"""
Created on Mon Dec 16 10:02:49 2024

@author: Asterisk
"""
import dearpygui.dearpygui as dpg

UserGraphs = {}
UserClosures = {}

ZOOM_LEVELS = list(range(30,180,10))
CURRENT_ZOOM = ZOOM_LEVELS.index(100)
CURRENT_SCALE = (1,1)
PREV_SCALE = (1,1)
FONT_SIZES = {}
RATIO = 1
ZOOM_ID = None

def reset_zoom():
    global ZOOM_LEVELS, CURRENT_ZOOM, CURRENT_SCALE, PREV_SCALE, RATIO
    ZOOM_LEVELS = list(range(30,180,10))
    CURRENT_ZOOM = ZOOM_LEVELS.index(100)
    CURRENT_SCALE = (1,1)
    PREV_SCALE = (1,1)
    RATIO = 1
    dpg.set_value("node_editor_zoom",ZOOM_LEVELS[CURRENT_ZOOM])

def get_terminal(*args,**kwargs):
    for child_index in dpg.get_item_children("node_editor",1):
        user_data = dpg.get_item_user_data(child_index)
        label = dpg.get_item_label(child_index)
        if user_data and user_data.terminal and label != "Output":
            return user_data