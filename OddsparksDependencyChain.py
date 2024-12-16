# -*- coding: utf-8 -*-
"""
Created on Fri Feb  9 11:39:51 2024

@author: Asterisk
"""
from fractions import Fraction

from Resources import Resources
from Facilities import Facilities
from Recipes import Recipe, Recipes, RecipeList
from ProductionGraph import ProductionGraphRecipeNode,BaseGraphs
from FileOps import get_file, get_files, get_folder

from fractions import Fraction
import dearpygui.dearpygui as dpg
import json        
from pathlib import Path

#class ProductionGraph():
#    pass

#Recipes.printDependencies()

X_BASE = 600
Y_BASE = 250
HORIZONTAL = -250
VERTICAL = 125

UserGraphs = {}
UserRecipes = {}

def link_callback(sender,app_data,user_data):
    susd = dpg.get_item_user_data(app_data[0])
    rusd = dpg.get_item_user_data(app_data[1])
    if hasattr(susd, "terminal") and susd.terminal and\
        hasattr(rusd, "terminal") and rusd.terminal:
        dpg.add_node_link(app_data[0], app_data[1], parent=sender)
        
def delink_callback(sender,app_data,user_data):
    return

def displace_lower_nodes(start_y,delta_y,source):
    current = source
    while(current.resource in current.sockets_out and current.sockets_out[current.resource] is not None):
        current = current.sockets_out[current.resource]
    displace_lower_nodes_downstream(start_y,delta_y,source,current)

def displace_lower_nodes_downstream(start_y,delta,source,current):
    cx,cy = dpg.get_item_pos(current.visual_node)
    if cy > start_y:
        cy += delta
        dpg.set_item_pos(current.visual_node,(cx,cy))
    for key,node in current.sockets_in.items():
        if node != source:
            displace_lower_nodes_downstream(start_y,delta,source,node)

def substitute_recipe_callback(sender,app_data,user_data):
    prod_node,replacement = user_data
    x,y = dpg.get_item_pos(prod_node.visual_node)
    dpg.delete_item(dpg.get_item_parent(sender))
    my = propagate_visual_deletion(prod_node)
    nprod_node = prod_node.substitute(replacement)
    vals = prod_node.visual
    vals[1] = x
    vals[2] = y
    yp,node = production_graph_to_node_graph(nprod_node,*vals)
                                             #,prod_node.visual_target,0,0,
                                             #target_socket = prod_node.visual_target_socket)
    displace_lower_nodes(y,yp-my,nprod_node)
    
def propagate_visual_deletion(prod_node):
    x,y = dpg.get_item_pos(prod_node.visual_node)
    dpg.delete_item(prod_node.visual_node)
    for inp,node in prod_node.sockets_in.items():
        ny = propagate_visual_deletion(node)
        y = max(ny,y)
    return y

def ratio_change(sender,app_data,user_data):
    num = dpg.get_value(user_data.visual_num)
    denom = dpg.get_value(user_data.visual_denom)
    if denom < 1:
        return
    if num < 0:
        return
    user_data.adjust_quantity(num,denom,fset=True)
    propagate_ratio_change(user_data)
    display_ratio_change(user_data)
    
def display_ratio_change(terminal_node):
    for (output,amount),(frac,fl) in zip(terminal_node.recipe.output_map.items(),terminal_node.visual_display_node):
        rate = Fraction(amount,terminal_node.recipe.processing_time)*terminal_node.quantity
        dpg.set_value(frac,"%s [%d/%d u/s]"%(output.name,rate.numerator,rate.denominator))
        dpg.set_value(fl,"%0.2f u/min"%(rate*60))
       
def propagate_ratio_change(prod_node):
    dpg.set_value(prod_node.visual_num,prod_node.quantity.numerator)
    dpg.set_value(prod_node.visual_denom,prod_node.quantity.denominator)
    for inp,node in prod_node.sockets_in.items():
        propagate_ratio_change(node)

def populate_substitution(sender,app_data,user_data):
    prod_node = user_data
    facs = [sub.name for sub in prod_node.resource.recipes_as_output]
    for substitute in prod_node.resource.recipes_as_output:
        label = substitute.facility.name
        if facs.count(label) > 1:
            label += " (%s)"%substitute.inputs[0][0].name
        dpg.add_button(label = label, user_data = (prod_node,substitute), callback = substitute_recipe_callback)

def build_visual_node(prod_node):
    enabled = prod_node.terminal
    if not enabled:
        with dpg.popup(dpg.last_item()) as pup:
            populate_substitution(pup,None,prod_node)
            #for substitue in user_recipes(prod_node.resource)
    with dpg.node_attribute(attribute_type = dpg.mvNode_Attr_Static):
        with dpg.group(horizontal = True):
            node_amount = Fraction(prod_node.quantity)
            num,denom = node_amount.numerator,node_amount.denominator
            att_num = dpg.add_input_int(label="", default_value = num,min_value = 0, 
                                        user_data = prod_node,
                                        enabled = enabled, width = 60, min_clamped = True,
                                        callback = ratio_change)
            dpg.add_text(default_value="/")
            att_denom = dpg.add_input_int(label="", min_value = 1, default_value = denom,
                                          user_data = prod_node,
                                          enabled = enabled, width = 60, min_clamped = True,
                                          callback = ratio_change)
            prod_node.visual_num = att_num
            prod_node.visual_denom = att_denom

def build_visual_sockets(prod_node,target,target_socket):
    sockets = []
    for inp in prod_node.recipe.inputs:
        with dpg.node_attribute(attribute_type = dpg.mvNode_Attr_Input) as inp_socket:
            sockets.append(inp_socket)
            dpg.add_text(default_value = "%2d x  %s"%(inp[1],inp[0].name))
    amounts = prod_node.recipe.output_amount if type(prod_node.recipe.output) is list else [prod_node.recipe.output_amount]
    output_sockets = []
    for output,amount in zip(prod_node.recipe.output_map.keys(),amounts):
        with dpg.node_attribute(attribute_type = dpg.mvNode_Attr_Output) as out_socket:
            output_sockets.append(out_socket)
            dpg.add_text(default_value = "%s x %2d"%(output.name,amount))
            if target_socket and target_socket[0] == output:
                dpg.add_node_link(out_socket,target_socket[1],parent=target)
    prod_node.visual_output_sockets = output_sockets    
    return sockets

def production_graph_to_node_graph(prod_node,target,x,y,target_socket = None,enabled = False):
    prod_node.visual = [target,x,y,target_socket]
    prod_node.visual_target = target,
    prod_node.visual_target_socket = target_socket
    with dpg.node(parent = target, label=prod_node.recipe.facility.name,
                  user_data = prod_node,pos = (x, y)) as node:
        prod_node.terminal = enabled
        prod_node.visual_node = node
        build_visual_node(prod_node)
        sockets = build_visual_sockets(prod_node,target,target_socket)
        for dsp,(inp,nnode) in enumerate(prod_node.sockets_in.items()):
            y,child = production_graph_to_node_graph(nnode,target,x+HORIZONTAL,y+VERTICAL*(dsp>0),(inp,sockets[dsp]))
    return y,node

def display_node(target,terminal_node):
    with dpg.node(parent = target, label="Output",
                  user_data = terminal_node, pos = (X_BASE- HORIZONTAL, Y_BASE - VERTICAL)) as node:
        vis = []
        for (output,amount),out_socket in zip(terminal_node.recipe.output_map.items(),terminal_node.visual_output_sockets):
            with dpg.node_attribute(attribute_type = dpg.mvNode_Attr_Input) as inp_socket:
                rate = Fraction(amount,terminal_node.recipe.processing_time)*terminal_node.quantity
                frac = dpg.add_text(default_value = "%s [%d/%d u/s]"%(output.name,rate.numerator,rate.denominator))
                fl = dpg.add_text(default_value = "%0.2f u/min"%(rate*60))
                dpg.add_node_link(out_socket, inp_socket, parent=target)
                vis.append((frac,fl))
        terminal_node.visual_display_node = vis

def recipe_select_callback(item,app_data,user_data):
    recipe = user_data
    target = "node_editor"
    dpg.delete_item(target,children_only = True)
    if recipe in BaseGraphs:
        terminal = BaseGraphs[recipe].copy()
        production_graph_to_node_graph(terminal,target,X_BASE,Y_BASE,enabled = True)
        display_node(target,terminal)
        dpg.set_value("node_editor_name","[%s] %s"%(recipe.facility.name,facility_name_generator(recipe)))

name_transform = lambda x: x.name.lower().replace(" ","_")
def tag_generator(recipe):
    inres = "+".join(map(name_transform,[name for name, _ in recipe.inputs]))
    outres = "+".join(map(name_transform,recipe.output_map.keys()))
    return inres+">"+outres

def facility_name_generator(recipe):
    facility = recipe.facility
    if facility.name in ["Plant Extractor","Geode Breaker"]:
        resource = recipe.inputs[0][0]
    else:
        resource = list(recipe.output_map.keys())[0].name
    if facility.name == "Aetheric Distiller" and resource == "Aetheric Shard":
        resource += " (%s)"%(recipe.inputs[0][0])
    return resource

def resource_meta_name_generator(resource):
    def resource_name_generator(recipe):
        facility = recipe.facility
        if len(recipe.output_map) > 1:
            resource_name = "%s"%facility.name + " [" + " + ".join(map(lambda x: x[0].name,recipe.inputs)) + " -> "+\
                            " + ".join(map(lambda x: x.name,recipe.output_map.keys())) +\
                                "]"
        else:
            resource_name = "%s"%facility.name
        #if len(resource.recipes_as_output)>2:
        #    for rcp in resource.recipes_as_output:
        #        if recipe != rcp and rcp.facility == recipe.facility:
        #            resource_name += " [%s]"%(recipe.inputs[0][0].name)
        #            break
        return resource_name
    return resource_name_generator

def populate_by_facility(facilities):
    for facility in sorted(facilities.values(),key=lambda x:x.name):
        if facility.name not in ["Compressor","Manual Collection per Second"] and\
            "Noxious Coral" not in facility.name:
            with dpg.tree_node(label=facility.name,
                           tag="recipe/base/facility/%s"%name_transform(facility)):
                path = lambda _: "facility/" + name_transform(facility)
                populate_from_recipe_list(facility.recipes,path,
                                          facility_name_generator)

def populate_by_resource(resources):
    for resource in sorted(resources.values(),key=lambda x: "-" + x.name if "Spark" in x.name else x.name):
        if resource.name in ["Miasma"]:
            continue
        with dpg.tree_node(label=resource.name,
                       tag="recipe/base/resource/%s"%name_transform(resource)):
            path = lambda x: "resource/" + name_transform(resource)+ "/" + name_transform(x.facility)
            populate_from_recipe_list(
                                        filter(
                                               lambda x: x.facility.name not in 
                                                               ["Compressor","Manual Collection per Second"],
                                               resource.recipes_as_output),
                                        path,resource_meta_name_generator(resource))


def recipe_key(recipe):
    output = next(iter(recipe.output_map.keys())).name
    if "Spark" in output:
        output = "-" + output
    return output
    
def populate_from_recipe_list(recipe_list,path,name_generator):
    for recipe in sorted(recipe_list, key=recipe_key):
        resource_name = name_generator(recipe)
        tag = tag_generator(recipe)
        b = dpg.add_button(label = resource_name, 
                       user_data = recipe,
                       tag = "recipe/base/%s/%s"%
                               (path(recipe),tag),
                       width = -1,
                       callback = recipe_select_callback)
        dpg.bind_item_theme(b,"base_theme")

def add_user_chain(terminal_node):
    target = "recipes/user"
    name = terminal_node.visual_name
    if name in UserGraphs:
        UserGraphs[name] = terminal_node
        return
    UserGraphs[terminal_node.visual_name] = terminal_node
    tag = "recipe/user/%s"%name
    b = dpg.add_button(parent = target,
                       label = name,
                       user_data = terminal_node,
                       tag = tag,
                       width = -1,
                       callback = user_graph_callback)
    dpg.bind_item_theme(b,"base_theme")

def serialize(sender,app_data,user_data):
    for child_index in dpg.get_item_children("node_editor",1):
        user_data = dpg.get_item_user_data(child_index)
        label = dpg.get_item_label(child_index)
        if user_data and user_data.terminal and label != "Output":
            text = user_data.serialize()
            label = user_data.label()
            with dpg.window(width = 8 * max(map(len,text.split("\n"))), 
                                        height = 18 * len(text.split("\n")),
                                        label = label):
                dpg.add_input_text(default_value = text,readonly = True,
                                   height = -1, width = -1, multiline = True)
            #print(text)

def get_terminal(*args,**kwargs):
    for child_index in dpg.get_item_children("node_editor",1):
        user_data = dpg.get_item_user_data(child_index)
        label = dpg.get_item_label(child_index)
        if user_data and user_data.terminal and label != "Output":
            return user_data

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
        def wrapper(*args,**kwargs):
            return promptf(lambda x: func(*args,prompt_response = x,**kwargs),label,prompt)
        return wrapper
    return prompt_decorator

@promptable(text_prompt,"Save Name","Please insert a name for this production chain")
def save_as_graph(sender,app_data,user_data,prompt_response):
    terminal = get_terminal()
    if not terminal:
        return
    terminal.visual_name = prompt_response
    #dpg.set_item_label(terminal.visual_node, prompt_response)
    def overwrite_chain():
        UserGraphs[prompt_response] = terminal
    if prompt_response in UserGraphs:
        binary_prompt(overwrite_chain,"Overwrite Chain?","There's an already existing chain with that name, overwrite?")
    else:
        _save_graph(terminal)

def _save_graph(terminal):
    rtr = []
    filename = terminal.visual_name
    add_user_chain(terminal)

def user_graph_callback(sender,app_data,user_data):
    _load_graph(user_data)
    dpg.set_value("node_editor_name",dpg.get_item_label(sender))
    
def _load_graph(graph):
    target = "node_editor"
    dpg.delete_item(target,children_only = True)
    production_graph_to_node_graph(graph, target, 
                                   X_BASE, Y_BASE, enabled = True)
    display_node(target,graph)


def load_graph(sender,app_data,user_data):
    inpath = get_file()
    if not inpath: return
    terminal = _import_graph(inpath)
    if not terminal: return
    _load_graph(terminal)

def main_window():            
    with dpg.theme(tag = "base_theme") as canvas_theme, dpg.theme_component():
        dpg.add_theme_style(dpg.mvStyleVar_WindowPadding, 0,0)
        dpg.add_theme_color(dpg.mvThemeCol_ChildBg, (255,255,255,255))
        dpg.add_theme_style(dpg.mvStyleVar_ButtonTextAlign, 0.0, 0.5)
    
    with dpg.window(tag = "main"):
        with dpg.viewport_menu_bar(tag = "menu_bar"):
            with dpg.menu(label="File"):
                dpg.add_menu_item(label="Export", callback = export_graph)
                dpg.add_menu_item(label="Export All", callback = export_all_graph)
                dpg.add_menu_item(label="Import", callback = import_graph)
            with dpg.menu(label="Chain"):
                dpg.add_menu_item(label="Save", callback = save_graph)
                dpg.add_menu_item(label="Save As", callback = save_as_graph)
                dpg.add_menu_item(label="Load", callback = load_graph)
                #dpg.add_menu_item(label="Pack", callback = pack_graph)
                dpg.add_menu_item(label="Serialize", callback = serialize)
                
        dpg.add_separator(tag = "sep")
        
        dpg.add_spacer(height=5)
        with dpg.table(resizable=True, header_row=False,tag = "work_area"):
            dpg.set_item_pos("work_area",(0,dpg.get_item_height("menu_bar")))
            recipe_width = 0.2
            dpg.add_table_column(init_width_or_weight=recipe_width)
            dpg.add_table_column(init_width_or_weight=1-recipe_width)
            with dpg.table_row():
                with dpg.child_window(border = False,tag="recipe"):
                    with dpg.tree_node(label="Base Recipes",tag="recipe/base"):
                        dpg.add_separator()
                        with dpg.tree_node(label="By Facility",tag="recipe/base/facility"):
                            populate_by_facility(Facilities)
                        with dpg.tree_node(label="By Resource",tag="recipes/base/resource"):
                            populate_by_resource(Resources)
                    with dpg.tree_node(label="User Chains",tag="recipes/user"):
                        dpg.add_separator()
                    #with dpg.tree_node(label="User Closed Chains",tag="recipes/closed_chain"):
                    #    dpg.add_separator()
                        
                with dpg.child_window(border = False):
                    dpg.add_text("No Recipe",tag = "node_editor_name")
                    dpg.add_node_editor(label="Node Editor", minimap=True,
                                    minimap_location=dpg.mvNodeMiniMap_Location_BottomRight,
                                    tag="node_editor",callback=link_callback, delink_callback=delink_callback)
                
    

       
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
    