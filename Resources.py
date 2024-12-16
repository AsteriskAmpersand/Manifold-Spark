# -*- coding: utf-8 -*-
"""
Created on Fri Dec 13 02:13:06 2024

@author: Asterisk
"""
from util import resource_path
Resources = {}

class Resource():
    def __init__(self, name, recipes_i = None, recipes_o = None, icon = None):
        self.name = name
        if icon is None:
            base = "./Sparks/" if " Spark" in self.name else "./Resources/"
            self.icon = base+self.name+".png"
        else:
            self.icon = icon
        self.recipes_as_output = [] if recipes_i is None else recipes_i
        self.recipes_as_input = [] if recipes_o is None else recipes_o
        Resources[self.name] = self
        
    def __str__(self):
        return self.name
    
    def __hash__(self):
        return hash(self.name)
        
with open(resource_path("Resources.dat"),"r") as inf:
    for line in inf:
        Resource(line.strip().lstrip())