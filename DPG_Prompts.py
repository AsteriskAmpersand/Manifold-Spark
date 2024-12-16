# -*- coding: utf-8 -*-
"""
Created on Mon Dec 16 10:00:58 2024

@author: Asterisk
"""
import dearpygui.dearpygui as dpg

def text_prompt(continuation, label = "",prompt = ""):
    def button_callback(sender,app_data,user_data):
        dpg.configure_item("modal_id_text", show=False)
        resp = dpg.get_item_label(sender)
        name = dpg.get_value(text)
        dpg.delete_item("modal_id_text")
        if resp == "OK":
            continuation(name)
        else:
            resp = ""
            
    with dpg.window(label = label, modal = True, tag="modal_id_text"):
        dpg.add_text(prompt)
        text = dpg.add_input_text(default_value = "",
                           height = -1, width = -1)
        dpg.add_separator()
        with dpg.group(horizontal=True):
            dpg.add_button(label="OK", width=75, callback=button_callback)
            dpg.add_button(label="Cancel", width=75, callback=button_callback)
    return 

def binary_prompt(continuation, label = "",prompt = ""):
    def button_callback(sender,app_data,user_data):
        dpg.configure_item("modal_id_binary", show=False)
        resp = dpg.get_item_label(sender)
        dpg.delete_item("modal_id_binary")
        if resp == "OK":
            continuation()
        else:
            resp = ""
            
    with dpg.window(label = label, modal = True, tag="modal_id_binary"):
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