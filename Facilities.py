# -*- coding: utf-8 -*-
"""
Created on Fri Dec 13 02:13:55 2024

@author: Asterisk
"""
from Resources import Resources
from util import resource_path

Facilities = {}

class Facility():
    def __init__(self,name,recipes = None, build_cost = [],icon = None, temp = 0):
        self.name = name
        self.build_cost = build_cost
        self.temperature = temp
        if icon is None:
            self.icon = "./Buildings/"+name.replace(" ","_") + ".png"
        else:
            self.icon = icon
        Facilities[self.name] = self
        if recipes is None:
            recipes = []
        self.recipes = recipes
        
    def __hash__(self):
        return hash(self.name)
    def __str__(self):
        return self.name
 
        
with open(resource_path("Facility.dat"),"r") as inf:
    for line in inf:
        name,temp,build_cost = line.strip().lstrip().split(",")
        temp = None if not temp else int(temp)
        build_cost = [] if not build_cost else map(lambda x: Resources[x], eval(build_cost))
        Facility(name,temp = temp,build_cost = build_cost)