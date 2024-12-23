# -*- coding: utf-8 -*-
"""
Created on Mon Dec 16 10:00:58 2024

@author: Asterisk
"""
import dearpygui.dearpygui as dpg

def infobox(title,text):
    x,y = dpg.get_viewport_client_width(),dpg.get_viewport_client_height()
    with dpg.window(label = title, modal = True, pos = (x/2-100,y/2-50)) as win:
        def button_callback(sender,app_data,user_data):
            dpg.configure_item(win, show=False)
            dpg.delete_item(win)
            
        dpg.add_text(text)
        dpg.add_separator()
        with dpg.group(horizontal=True):
            dpg.add_button(label="OK", width=75, callback=button_callback)
    return 

def text_prompt(continuation, label = "",prompt = ""):
    x,y = dpg.get_viewport_client_width(),dpg.get_viewport_client_height()
    with dpg.window(label = label, modal = True, pos = (x/2-100,y/2-50)) as win:
        def button_callback(sender,app_data,user_data):
            dpg.configure_item(win, show=False)
            resp = dpg.get_item_label(sender)
            name = dpg.get_value(text)
            dpg.delete_item(win)
            if resp == "OK":
                continuation(name)
            else:
                resp = ""
            
        dpg.add_text(prompt)
        text = dpg.add_input_text(default_value = "",
                           height = -1, width = -1)
        dpg.add_separator()
        with dpg.group(horizontal=True):
            dpg.add_button(label="OK", width=75, callback=button_callback)
            dpg.add_button(label="Cancel", width=75, callback=button_callback)
    return 

def binary_prompt(continuation, label = "",prompt = ""):
    x,y = dpg.get_viewport_client_width(),dpg.get_viewport_client_height()
    def button_callback(sender,app_data,user_data):
        dpg.configure_item("modal_id_binary", show=False)
        resp = dpg.get_item_label(sender)
        dpg.delete_item("modal_id_binary")
        if resp == "OK":
            continuation()
        else:
            resp = ""
            
    with dpg.window(label = label, tag="modal_id_binary", pos = (x/2-100,y/2-50)):
        dpg.add_text(prompt)
        with dpg.group(horizontal=True):
            dpg.add_button(label="OK", width=75, callback=button_callback)
            dpg.add_button(label="Cancel", width=75, callback=button_callback)
    return 

def promptable(promptf,label="",prompt=""):
    def prompt_decorator(func):
        def wrapper(sender,app_data,user_data,**kwargs):
            return promptf(lambda x: func(sender,app_data,user_data,prompt_response = x,**kwargs),label,prompt)
        return wrapper
    return prompt_decorator