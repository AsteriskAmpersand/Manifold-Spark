# -*- coding: utf-8 -*-
"""
Created on Mon Dec 16 09:58:33 2024

@author: Asterisk
"""
import DPG_Prompts as prompt
from DPG_Common import UserGraphs, UserClosures, get_terminal
from DPG_GraphOps import display_node,load_graph
from ProductionGraph import ProductionGraphRecipeNode
from ClosedRecipe import ClosedRecipe
from FileOps import get_file, get_files, get_folder

import dearpygui.dearpygui as dpg
from pathlib import Path
import json

def _export_graph(terminal,outpath):
    with open(outpath,"w") as outf:
        json_data = terminal.pack()
        outf.write(json.dumps(json_data, indent = 2))

def export_all_graph(sender,app_data,user_data):
    folder = get_folder()
    if not folder:
        return
    for name,terminal in UserGraphs.items():
        _export_graph(terminal,folder+"\\"+name+".json")

def export_graph(sender,app_data,user_data):
    terminal = get_terminal()
    outpath = get_file()
    if not outpath or not terminal:
        return
    _export_graph(terminal,outpath)

def _import_graph(inpath):
    with open(inpath,"r") as inf:
        json_data = json.load(inf)
        terminal = ProductionGraphRecipeNode.UnpackNetwork(json_data)
    return terminal

def import_graph():
    inpaths = get_files()
    if not inpaths:return
    for inpath in inpaths:
        terminal = _import_graph(inpath)
        terminal.visual_name = Path(inpath).stem
        add_user_chain(terminal)
        
def save_graph(sender,app_data,user_data):
    terminal = get_terminal()
    if hasattr(terminal,"visual_name"):
        _save_graph(terminal)
    else:
        save_as_graph(sender,app_data,user_data)

def _save_graph(terminal):
    add_user_chain(terminal)


def menu_load_graph(sender,app_data,user_data):
    inpath = get_file()
    if not inpath: return
    terminal = _import_graph(inpath)
    if not terminal: return
    load_graph(terminal)

def user_graph_callback(sender,app_data,user_data):
    graph = user_data.copy()
    load_graph(graph)
    dpg.set_value("node_editor_name",dpg.get_item_label(sender))
    graph.visual_name = dpg.get_item_label(sender)

def add_user_chain(terminal_node):
    target = "recipes/user"
    name = terminal_node.visual_name
    tag = "recipes/user/%s"%name
    if name in UserGraphs:
        UserGraphs[name] = terminal_node.copy()
        UserClosures[name] = ClosedRecipe(terminal_node.copy())
        dpg.set_item_user_data(tag,UserGraphs[name])
        return
    tnc = terminal_node.copy()
    UserGraphs[terminal_node.visual_name] = tnc
    UserClosures[terminal_node.visual_name] = ClosedRecipe(tnc)
    b = dpg.add_button(parent = target,
                       label = name,
                       user_data = UserGraphs[terminal_node.visual_name],
                       tag = tag,
                       width = -1,
                       callback = user_graph_callback)
    dpg.bind_item_theme(b,"base_theme")



@prompt.promptable(prompt.text_prompt,"Save Name","Please insert a name for this production chain")
def save_as_graph(sender,app_data,user_data,prompt_response):
    if not prompt_response:
        #print("No Prompt Response")
        return
    terminal = get_terminal()
    if not terminal:
        return
    match = False
    if hasattr(terminal,"visual_name"):
        match = terminal.visual_name == prompt_response
    #dpg.set_item_label(terminal.visual_node, prompt_response)
    def overwrite_chain():
        node = terminal.copy()
        node.visual_name = prompt_response
        UserGraphs[prompt_response] = node
        dpg.set_value("node_editor_name",node.visual_name)
        dpg.set_item_user_data("recipes/user/%s"%prompt_response,UserGraphs[prompt_response])
    if prompt_response in UserGraphs and not match:
        prompt.binary_prompt(overwrite_chain,"Overwrite Chain?","There's an already existing chain with that name, overwrite?")
    else:
        terminal.visual_name = prompt_response
        _save_graph(terminal)
        dpg.set_value("node_editor_name",terminal.visual_name)
    
def serialize(sender,app_data,user_data):
    closure = (dpg.get_item_label(sender)  == "Closure")
    for child_index in dpg.get_item_children("node_editor",1):
        user_data = dpg.get_item_user_data(child_index)
        label = dpg.get_item_label(child_index)
        if user_data and user_data.terminal and label != "Output":
            text = user_data.serialize_closure() if closure else user_data.serialize()
            label = user_data.label()
            with dpg.window(width = 8 * max(map(len,text.split("\n"))), 
                                        height = 18 * len(text.split("\n")),
                                        label = label):
                dpg.add_input_text(default_value = text,readonly = True,
                                   height = -1, width = -1, multiline = True)
            return


def visual_menubar():
    with dpg.viewport_menu_bar(tag = "menu_bar"):
        with dpg.menu(label="File"):
            dpg.add_menu_item(label="Export", callback = export_graph)
            dpg.add_menu_item(label="Export All", callback = export_all_graph)
            dpg.add_menu_item(label="Import", callback = import_graph)
        with dpg.menu(label="Chain"):
            dpg.add_menu_item(label="Save", callback = save_graph)
            dpg.add_menu_item(label="Save As", callback = save_as_graph)
            dpg.add_menu_item(label="Load", callback = menu_load_graph)
            dpg.add_menu_item(label="Serialize", callback = serialize)
            dpg.add_menu_item(label="Closure", callback = serialize)