# -*- coding: utf-8 -*-
"""
Created on Fri Feb  9 11:39:51 2024

@author: Asterisk
"""
from fractions import Fraction


from DPG_MenuBar import visual_menubar
from DPG_RecipeSelector import recipe_selector

import dearpygui.dearpygui as dpg

        
def link_callback(sender,app_data,user_data):
    susd = dpg.get_item_user_data(app_data[0])
    rusd = dpg.get_item_user_data(app_data[1])
    if hasattr(susd, "terminal") and susd.terminal and\
        hasattr(rusd, "terminal") and rusd.terminal:
        dpg.add_node_link(app_data[0], app_data[1], parent=sender)
        
def delink_callback(sender,app_data,user_data):
    return

def node_editor():                        
    with dpg.child_window(border = False):
        dpg.add_text("No Recipe",tag = "node_editor_name")
        dpg.add_node_editor(label="Node Editor", minimap=True,
                        minimap_location=dpg.mvNodeMiniMap_Location_BottomRight,
                        tag="node_editor",callback=link_callback, delink_callback=delink_callback)

def main_window():            
    with dpg.theme(tag = "base_theme") as canvas_theme, dpg.theme_component():
        dpg.add_theme_style(dpg.mvStyleVar_WindowPadding, 0,0)
        dpg.add_theme_color(dpg.mvThemeCol_ChildBg, (255,255,255,255))
        dpg.add_theme_style(dpg.mvStyleVar_ButtonTextAlign, 0.0, 0.5)
    
    with dpg.window(tag = "main"):
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
    dpg.set_viewport_small_icon("./MathySpark.ico")
    dpg.set_viewport_large_icon("./MathySpark.ico")
    main_window()
    dpg.set_primary_window("main",True)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()