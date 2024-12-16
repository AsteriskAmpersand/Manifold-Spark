# -*- coding: utf-8 -*-
"""
Created on Mon Dec 16 14:34:22 2024

@author: Asterisk
"""
from Recipes import Recipe
from Facilities import Facilities
from ProductionGraph import ProductionGraphRecipeNode

from fractions import Fraction
import json

class ClosedRecipe(Recipe):
    def __init__(self,graph):
        self.graph = graph
        outputs = graph.total_outputs()
        inputs = graph.total_inputs()
        net_inputs, net_outputs = self.close(inputs,outputs)
        processing_time,balanced_inputs,balanced_outputs = self.balance(net_inputs,net_outputs)
        super().__init__(Facilities["Cyclical Recipe"],
               list(balanced_outputs.keys()),
               list(balanced_inputs.items()),
               processing_time,
               tuple(balanced_outputs.values()),
               active=False)

    def close(self,inputs,outputs):
        net_ins = {}
        net_outs = {}
        for res in inputs:
            if res in outputs:
                net = outputs[res] - inputs[res]
                if net < 0:
                    net_ins[res] = -net
                else:
                    net_outs[res] = net
            else:
                net_ins[res] = net
        for res in outputs:
           if res not in inputs:
               net_outs[res] = outputs[res]
        return net_ins,net_outs
    
    def balance(self,inputs,outputs):
        totality = set(inputs.values()).union(set(outputs.values()))
        maximality = max(map(lambda x: Fraction(x).denominator,totality))
        processing_time = maximality
        binputs = {key:val*processing_time for key,val in inputs.items()}
        boutputs = {key:val*processing_time for key,val in outputs.items()}
        return processing_time,binputs,boutputs
    