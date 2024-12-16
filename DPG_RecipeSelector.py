# -*- coding: utf-8 -*-
"""
Created on Mon Dec 16 10:17:59 2024

@author: Asterisk
"""
from Resources import Resources
from Facilities import Facilities
from ProductionGraph import BaseGraphs
from DPG_GraphOps import production_graph_to_node_graph,display_node

import dearpygui.dearpygui as dpg

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
        return resource_name
    return resource_name_generator



def recipe_key(recipe):
    output = next(iter(recipe.output_map.keys())).name
    if "Spark" in output:
        output = "-" + output
    return output
    
def recipe_select_callback(item,app_data,user_data):
    recipe = user_data
    target = "node_editor"
    dpg.delete_item(target,children_only = True)
    if recipe in BaseGraphs:
        terminal = BaseGraphs[recipe].copy()
        production_graph_to_node_graph(terminal,target,enabled = True)
        display_node(target,terminal)
        dpg.set_value("node_editor_name","[%s] %s"%(recipe.facility.name,facility_name_generator(recipe)))
        
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

def recipe_selector():
    with dpg.child_window(border = False,tag="recipe"):
        with dpg.tree_node(label="Base Chains",tag="recipe/base"):
            dpg.add_separator()
            with dpg.tree_node(label="By Facility",tag="recipe/base/facility"):
                populate_by_facility(Facilities)
            with dpg.tree_node(label="By Resource",tag="recipes/base/resource"):
                populate_by_resource(Resources)
        with dpg.tree_node(label="User Chains",tag="recipes/user"):
            pass