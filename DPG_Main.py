# -*- coding: utf-8 -*-
"""
Created on Fri Feb  9 11:39:51 2024

@author: Asterisk
"""
from fractions import Fraction

from util import resource_path
from DPG_MenuBar import visual_menubar
from DPG_RecipeSelector import recipe_selector
import DPG_Common as Com

import dearpygui.dearpygui as dpg

        
def link_callback(sender,app_data,user_data):
    susd = dpg.get_item_user_data(app_data[0])
    rusd = dpg.get_item_user_data(app_data[1])
    if hasattr(susd, "terminal") and susd.terminal and\
        hasattr(rusd, "terminal") and rusd.terminal:
        dpg.add_node_link(app_data[0], app_data[1], parent=sender)


def delink_callback(sender,app_data,user_data):
    return

def update_zoom(node_editor, editor_pos, mouse_pos):
    if len(dpg.get_item_children(node_editor)[1]) == 0:
        return
    dsum = lambda u,v: (u[0]+v[0],u[1]+v[1])
    dmin = lambda u: (-u[0],-u[1])
    dsub = lambda u,v: dsum(u,dmin(v))
    dprod = lambda u,v: (u[0]*v[0],u[1]*v[1])
    ddiv = lambda u,v: (u[0]/v[0],u[1]/v[1])
    sizes = {}
    scales = []
    #get size of all nodes at zoom 100:
    for node in dpg.get_item_children(node_editor)[1]:
        dpg.bind_item_font(node,Com.FONT_SIZES[Com.ZOOM_LEVELS[7]])
        sizes[node] = dpg.get_item_rect_size(node)
    #get size of all nodes at current zoom:
    Com.set_global_zoom(node_editor,sizes,scales)
    Com.CURRENT_SCALE = max(map(lambda x: x[0], scales)),max(map(lambda x: x[1], scales))
    scale = Com.ZOOM_LEVELS[Com.CURRENT_ZOOM]
    Com.CURRENT_SCALE = (scale/100,scale/100)
    #Scale up the mouse position then substract everythign from the difference between old and new scaled up
    ratio = ddiv(Com.CURRENT_SCALE,Com.PREV_SCALE)
    x,y = dpg.get_item_rect_min(node)
    nx,ny = dpg.get_item_pos(node)
    deltawin = nx-x, ny-y
    mouse_node = dsum(mouse_pos,deltawin)
    mouse_node_p = dprod(mouse_node,ratio)
    delta = dsub(mouse_node,mouse_node_p)
    for node in dpg.get_item_children(node_editor)[1]:
        pos = dpg.get_item_pos(node)
        dpg.set_item_pos(node,dsum(delta,dprod(pos,ratio)))
    dpg.set_value("node_editor_zoom","%d%%"%(Com.ZOOM_LEVELS[Com.CURRENT_ZOOM]))


def wheel_callback(sender,app_data,user_data):
    Com.PREV_SCALE = Com.CURRENT_SCALE
    window,node_editor = user_data
    w,h = dpg.get_item_rect_size(window)
    x,y = dpg.get_item_pos(window)
    mx,my = dpg.get_mouse_pos()
    if x <= mx <= x+w and y <= my <= y+h:
        if app_data > 0:
            Com.CURRENT_ZOOM = min(len(Com.ZOOM_LEVELS)-1,Com.CURRENT_ZOOM + 1)
            update_zoom(node_editor,(x,y),(mx,my))
        else:
            Com.CURRENT_ZOOM = max(0,Com.CURRENT_ZOOM - 1)
            update_zoom(node_editor,(x,y),(mx,my))
            

def node_editor():                        
    with dpg.child_window(border = False) as win:
        with dpg.table(resizable=True, header_row=False,tag = "node_editor_header"):
            recipe_width = 0.9
            dpg.add_table_column(init_width_or_weight=recipe_width)
            dpg.add_table_column(init_width_or_weight=1-recipe_width)
            with dpg.table_row():
                dpg.add_text("No Recipe",tag = "node_editor_name")
                dpg.add_text("%d%%"%(Com.ZOOM_LEVELS[Com.CURRENT_ZOOM]),tag = "node_editor_zoom")
        with dpg.node_editor(label="Node Editor", minimap=True,
                        minimap_location=dpg.mvNodeMiniMap_Location_BottomRight,
                        tag="node_editor",callback=link_callback, delink_callback=delink_callback) as node_editor:
            with dpg.handler_registry() as handler:
                dpg.add_mouse_wheel_handler(parent=handler, callback = wheel_callback, user_data = (win,node_editor))
                #dpg.bind_item_handler_registry(node_editor,handler)

def scale_settings():
    with dpg.font_registry():
        Com.FONT_SIZES = { z:dpg.add_font(resource_path("./OpenSans-VariableFont_wdth,wght.ttf"), round(16*z/100))  for z in Com.ZOOM_LEVELS}
      
  
         # first argument ids the path to the .ttf or .otf file
            #default_font = dpg.add_font("NotoSerifCJKjp-Medium.otf", 20)

def main_window():        
    scale_settings()
    with dpg.theme(tag = "base_theme") as canvas_theme, dpg.theme_component():
        dpg.add_theme_style(dpg.mvStyleVar_WindowPadding, 0,0)
        dpg.add_theme_color(dpg.mvThemeCol_ChildBg, (255,255,255,255))
        dpg.add_theme_style(dpg.mvStyleVar_ButtonTextAlign, 0.0, 0.5)
    
    with dpg.window(tag = "main") as win:
        dpg.bind_item_font(win,Com.FONT_SIZES[100])
        visual_menubar()
        dpg.add_separator(tag = "sep")
        dpg.add_spacer(height=5)
        with dpg.table(resizable=True, header_row=False,tag = "work_area"):
            dpg.set_item_pos("work_area",(0,dpg.get_item_height("menu_bar")))
            recipe_width = 0.2
            dpg.add_table_column(init_width_or_weight=recipe_width)
            dpg.add_table_column(init_width_or_weight=1-recipe_width)
            with dpg.table_row():
                recipe_selector()
                node_editor()
                
    

       
if __name__ == '__main__':
    import dearpygui.dearpygui as dpg

    dpg.create_context()
    dpg.create_viewport(title='Oddsparks Production Chain Builder', width=600, height=600)
    dpg.set_viewport_small_icon(resource_path("./ManifoldSpark.ico"))
    dpg.set_viewport_large_icon(resource_path("./ManifoldSpark.ico"))
    main_window()
    dpg.set_primary_window("main",True)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context() 
      
    