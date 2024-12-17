# -*- coding: utf-8 -*-
"""
Created on Mon Dec 16 10:07:30 2024

@author: Asterisk
"""
from DPG_Common import UserGraphs,UserClosures

import dearpygui.dearpygui as dpg
from fractions import Fraction
import DPG_Common as Com

X_BASE = 600
Y_BASE = 250
HORIZONTAL = -250
VERTICAL = 125

def horizontal():
    return HORIZONTAL * Com.CURRENT_SCALE[0]

def vertical():
    return VERTICAL * Com.CURRENT_SCALE[1]

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
    
def substitute_recipe_callback(sender,_,user_data):
    prod_node,replacement = user_data
    
    nxt = prod_node.sockets_out[prod_node.resource]
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
    nxt = nprod_node.sockets_out[nprod_node.resource]
    return nprod_node
    
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
    if num < 1:
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

def substitution_menu(sender, app_data, user_data):
    pos = dpg.get_mouse_pos(local=False)
    with dpg.window(label="Right click window", modal=False, no_title_bar=True, popup = True, pos = pos) as pup:
        populate_substitution(pup,None,user_data)

def populate_substitution(sender,app_data,user_data):
    prod_node = user_data
    facs = [sub.name for sub in prod_node.resource.recipes_as_output]
    for substitute in prod_node.resource.recipes_as_output:
        label = substitute.facility.name
        if facs.count(label) > 1:
            label += " (%s)"%substitute.inputs[0][0].name
        dpg.add_button(label = label, user_data = (prod_node,substitute), callback = substitute_recipe_callback)
    dpg.add_separator()
    for user_chain,node in UserGraphs.items():
        if prod_node.resource in node.recipe.output_map:
            label = user_chain
            dpg.add_button(label = label, user_data = (prod_node,node), callback = substitute_recipe_callback)
    dpg.add_separator()
    for closure_name,recipe in UserClosures.items():
        if prod_node.resource in recipe.output_map:
            label = "Closure[%s]"%closure_name
            def closure_callback(s,a,u):
                nprod_node = substitute_recipe_callback(s,a,u)
                dpg.set_item_label(nprod_node.visual_node,label)                
            dpg.add_button(label = label, user_data = (prod_node,recipe), callback = closure_callback)
            

def build_visual_node(prod_node):
    enabled = prod_node.terminal
    if not enabled:
        with dpg.item_handler_registry() as handler:
            dpg.add_item_clicked_handler(button=dpg.mvMouseButton_Right, callback=substitution_menu,user_data=prod_node)
            dpg.bind_item_handler_registry(prod_node.visual_node,handler)

    with dpg.node_attribute(attribute_type = dpg.mvNode_Attr_Static):
        with dpg.group(horizontal = True):
            node_amount = Fraction(prod_node.quantity)
            num,denom = node_amount.numerator,node_amount.denominator
            att_num = dpg.add_input_int(label="", default_value = num,min_value = 0, 
                                        user_data = prod_node,
                                        enabled = enabled, width = 40, min_clamped = True,
                                        callback = ratio_change, step = 0)
            att_sep = dpg.add_text(default_value="/")
            att_denom = dpg.add_input_int(label="", min_value = 1, default_value = denom,
                                          user_data = prod_node,
                                          enabled = enabled, width = 40, min_clamped = True,
                                          callback = ratio_change, step = 0)
            prod_node.visual_num = att_num
            prod_node.visual_denom = att_denom
            prod_node.visual_components["quantity"] = [att_num,att_sep,att_denom]

def build_visual_sockets(prod_node,target,target_socket):
    sockets = []
    prod_node.visual_components["input_socket_text"] = []
    for inp in prod_node.recipe.inputs:
        with dpg.node_attribute(attribute_type = dpg.mvNode_Attr_Input) as inp_socket:
            sockets.append(inp_socket)
            txt = dpg.add_text(default_value = "%2d x  %s"%(inp[1],inp[0].name))
            prod_node.visual_components["input_socket_text"].append(txt)
    amounts = prod_node.recipe.output_amount if type(prod_node.recipe.output) is list else [prod_node.recipe.output_amount]
    output_sockets = []
    prod_node.visual_components["output_socket_text"] = []
    for output,amount in zip(prod_node.recipe.output_map.keys(),amounts):
        with dpg.node_attribute(attribute_type = dpg.mvNode_Attr_Output) as out_socket:
            output_sockets.append(out_socket)
            txt = dpg.add_text(default_value = "%s x %2d"%(output.name,amount))
            prod_node.visual_components["output_socket_text"].append(txt)
            if target_socket and target_socket[0] == output:
                dpg.add_node_link(out_socket,target_socket[1],parent=target)
    prod_node.visual_output_sockets = output_sockets    
    return sockets

def production_graph_to_node_graph(prod_node,target,x=X_BASE,y=Y_BASE,target_socket = None,enabled = False):
    prod_node.visual = [target,x,y,target_socket]
    prod_node.visual_target = target,
    prod_node.visual_target_socket = target_socket
    prod_node.visual_components = {}
    with dpg.node(parent = target, label=prod_node.recipe.facility.name,
                  user_data = prod_node,pos = (x, y)) as node:
        prod_node.terminal = enabled
        prod_node.visual_node = node
        build_visual_node(prod_node)
        sockets = build_visual_sockets(prod_node,target,target_socket)
        for dsp,(inp,nnode) in enumerate(prod_node.sockets_in.items()):
            y,child = production_graph_to_node_graph(nnode,target,x+horizontal(),y+vertical()*(dsp>0),(inp,sockets[dsp]))
    return y,node

def display_node(target,terminal_node):
    with dpg.node(parent = target, label="Output",
                  user_data = terminal_node, pos = (X_BASE- horizontal(), Y_BASE - vertical())) as node:
        vis = []
        for (output,amount),out_socket in zip(terminal_node.recipe.output_map.items(),terminal_node.visual_output_sockets):
            with dpg.node_attribute(attribute_type = dpg.mvNode_Attr_Input) as inp_socket:
                rate = Fraction(amount,terminal_node.recipe.processing_time)*terminal_node.quantity
                frac = dpg.add_text(default_value = "%s [%d/%d u/s]"%(output.name,rate.numerator,rate.denominator))
                fl = dpg.add_text(default_value = "%0.2f u/min"%(rate*60))
                dpg.add_node_link(out_socket, inp_socket, parent=target)
                vis.append((frac,fl))
        terminal_node.visual_display_node = vis

    
def load_graph(graph):
    target = "node_editor"
    Com.reset_zoom()
    dpg.delete_item(target,children_only = True)
    production_graph_to_node_graph(graph, target, enabled = True)
    display_node(target,graph)   