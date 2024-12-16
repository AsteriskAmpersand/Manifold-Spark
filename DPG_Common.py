# -*- coding: utf-8 -*-
"""
Created on Mon Dec 16 10:02:49 2024

@author: Asterisk
"""
import dearpygui.dearpygui as dpg

UserGraphs = {}
UserRecipes = {}


def get_terminal(*args,**kwargs):
    for child_index in dpg.get_item_children("node_editor",1):
        user_data = dpg.get_item_user_data(child_index)
        label = dpg.get_item_label(child_index)
        if user_data and user_data.terminal and label != "Output":
            return user_data