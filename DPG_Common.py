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

def set_global_zoom(node_editor,sizes=None,scales=None):
    for node in dpg.get_item_children(node_editor)[1]:
        prod_node = dpg.get_item_user_data(node)
        set_zoom(node,prod_node,sizes,scales)
        
def set_zoom(node,prod_node,sizes=None,scales=None):
    scale = ZOOM_LEVELS[CURRENT_ZOOM]
    ddiv = lambda u,v: (u[0]/v[0],u[1]/v[1])
    dpg.bind_item_font(node,FONT_SIZES[scale])
    if not dpg.get_item_label(node) == "Output":
        for element in dpg.get_item_children(node):
            dpg.set_item_width(prod_node.visual_num,round(40*scale/100))
            dpg.set_item_width(prod_node.visual_denom,round(40*scale/100))
        for component_list in prod_node.visual_components.values():
            for component in component_list:
                try:
                    dpg.set_item_height(component,round(20*scale/100))
                except:
                    pass
        if sizes is not None and scales is not None:
            size = dpg.get_item_rect_size(node)
            node_scale = ddiv(size,sizes[node])
            scales.append(node_scale)

def reset_zoom():
    global ZOOM_LEVELS, CURRENT_ZOOM, CURRENT_SCALE, PREV_SCALE, RATIO
    ZOOM_LEVELS = list(range(30,180,10))
    CURRENT_ZOOM = ZOOM_LEVELS.index(100)
    CURRENT_SCALE = (1,1)
    PREV_SCALE = (1,1)
    RATIO = 1
    dpg.set_value("node_editor_zoom","%d%%"%ZOOM_LEVELS[CURRENT_ZOOM])

def get_terminal(*args,**kwargs):
    for child_index in dpg.get_item_children("node_editor",1):
        user_data = dpg.get_item_user_data(child_index)
        label = dpg.get_item_label(child_index)
        if user_data and user_data.terminal and label != "Output":
            return user_data