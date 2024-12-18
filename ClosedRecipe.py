# -*- coding: utf-8 -*-
"""
Created on Mon Dec 16 14:34:22 2024

@author: Asterisk
"""
from Recipes import Recipe
from Facilities import Facilities
from ProductionGraph import ProductionGraphRecipeNode

from collections import defaultdict
from fractions import Fraction
import json

class ClosedRecipe(Recipe):
    def __init__(self,graph):
        self.graph = graph
        net_inputs, net_outputs = graph.closure()
        processing_time,balanced_inputs,balanced_outputs = self.balance(net_inputs,net_outputs)
        super().__init__(Facilities["Cyclical Recipe"],
               list(balanced_outputs.keys()),
               list(balanced_inputs.items()),
               processing_time,
               tuple(balanced_outputs.values()),
               active=False)
    
    def balance(self,inputs,outputs):
        totality = set(inputs.values()).union(set(outputs.values()))
        maximality = max(map(lambda x: Fraction(x).denominator,totality))
        processing_time = maximality
        binputs = {key:val*processing_time for key,val in inputs.items()}
        boutputs = {key:val*processing_time for key,val in outputs.items()}
        return processing_time,binputs,boutputs