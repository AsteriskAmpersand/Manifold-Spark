# -*- coding: utf-8 -*-
"""
Created on Fri Dec 13 02:30:11 2024

@author: Asterisk
"""
from Resources import Resources
from Facilities import Facilities
from Recipes import Recipe,Recipes
from util import to_str

from fractions import Fraction

def find_compressor_recipe(resource):
    facility = Facilities["Compressor"]
    for recipe in facility.recipes:
        if recipe.inputs[0][0] == resource:
            return recipe
    raise
    
def recipeQuantity(outputRecipe,inputRecipe,resource,multiplier = 1):
    output_amount = outputRecipe.output_map[resource]
    craft_rate = output_amount/outputRecipe.processing_time
    for inp,amount in inputRecipe.inputs:
        if inp == resource:
            consume_rate = amount / inputRecipe.processing_time
    return multiplier * consume_rate/craft_rate

def fetchRecipe(resource):
    primitive = None
    raw = None
    if len(Recipes[resource]) == 2:
        return Recipes[resource][1]
    for rcp in Recipes[resource]:
        if rcp.primitive and not rcp.raw:
            primitive = rcp
        if rcp.raw:
            raw = rcp
    if primitive: return primitive
    if raw: return raw
    return Recipes[resource][0]
        
class ProductionGraphNode():
    pass
            
class ProductionGraphRecipeNode(ProductionGraphNode):
    def __init__(self,recipe, resource = None, outputs = None, quantity = None, parent = None):
        self.parent = parent
        if self.parent:
            self.parent.add(self)
        if quantity is None:
            quantity = Fraction(1)
        self.quantity = quantity
        self.recipe = recipe
        self.sockets_out = {}
        self.lock_set = False
        rcp_out = self.recipe.output
        if type(rcp_out) is not list:
            rcp_out = [rcp_out]
        if resource is None:
            resource = next(self.output_map.keys())
        self.resource = resource
        for rsr in self.recipe.output_map:
            self.sockets_out[rsr] = None #ProductionGraphRecipeNode(
        #                                find_compressor_recipe(rsr),
        #                                recipeQuantity(recipe,
        #                                               find_compressor_recipe(rsr),
        #                                               rsr,
        #                                               quantity))
        if outputs:
            for resource,node in outputs.items():
                if resource in self.sockets_out:
                    self.sockets_out[resource] = outputs[resource]
        self.sockets_in = {}
        for inp,_ in self.recipe.inputs:
            self.sockets_in[inp] = \
                           ProductionGraphRecipeNode(fetchRecipe(inp),
                                                     resource = inp,
                                                     outputs = {inp:self},
                                                     quantity = recipeQuantity(fetchRecipe(inp),
                                                                               recipe,inp,
                                                                               quantity),
                                                     parent = self.parent)
    def terminate(self,resource,endNode):
        if self.resource != resource:
            raise ValueError("Resource termination does not match graph node focus resource")
        self.sockets_out[self.resource]=endNode
        
    def _substitute_recipe(self,recipe):
        if self.resource not in recipe.output_map:
            raise ValueError("Replacement does not have target output")
        old_rate = self.quantity * self.recipe.output_map[self.resource] / self.recipe.processing_time
        new_rate = recipe.output_map[self.resource] / recipe.processing_time
        new_quantity = old_rate/new_rate
        nnode = ProductionGraphRecipeNode(recipe,resource = self.resource, 
                                  outputs = {self.resource:self.sockets_out[self.resource]},
                                  quantity = new_quantity, 
                                  parent = self.parent)
        sout = self.sockets_out[self.resource]
        if sout and self.resource in sout.sockets_in:
            sout.sockets_in[self.resource] = nnode
        self.remove()
        return nnode            
        
    def adjust_quantity(self,numerator,denominator,fset = False):
        old_quantity = self.quantity
        new_quantity = Fraction(numerator,denominator)
        if fset:
            self.quantity = new_quantity
            rate = Fraction(new_quantity, old_quantity)
        else:
            self.quantity *= new_quantity
            rate = new_quantity
        for rsr, node in self.sockets_in.items():
            if node is not None:
                node.adjust_quantity(rate.numerator,rate.denominator)
        return new_quantity
    
    def _substitute_node(self,node):
        res = self.resource
        old_production = Fraction(self.recipe.output_map[res]*self.quantity,self.recipe.processing_time)
        new_production = Fraction(node.recipe.output_map[res],node.recipe.processing_time)
        rate = old_production/new_production
        node.adjust_quantity(rate.numerator,rate.denominator,fset = True)
        target = self.sockets_out[self.resource]
        node.sockets_out[self.resource] = target  
        if target is not None:
            target.retarget(self,node)

        self.remove()
        return node
    
    def substitute(self,obj):
        #if type(obj) is ProductionGraph:
        #    self._substitute_graph(obj)
        if hasattr(obj,"terminal"):
            obj.terminal = self.terminal
        if type(obj) is Recipe:
            print("Recipe Substitution")
            return self._substitute_recipe(obj)
        if type(obj) is ProductionGraphRecipeNode:
            return self._substitute_node(obj.copy(self.parent))
    
    def remove(self):
        if self.parent:
            self.parent.remove(self)
        for val in self.sockets_in.values():
            if type(val) is ProductionGraphNode:
                val.remove()
                
    def copy(self, new_parent = None):
        if new_parent is None:
            new_parent = self.parent
        nnode = type(self)(self.recipe, 
                           resource = self.resource, 
                           outputs = None, 
                           quantity = self.quantity, 
                           parent = new_parent)
        for key in nnode.sockets_in:
            node_in = self.sockets_in[key]
            if node_in is not None:
                copied_input = node_in.copy(new_parent)
                nnode.sockets_in[key] = copied_input
                copied_input.sockets_out[key] = nnode
        return nnode
    
    def retarget(self,old,new):
        for key,val in self.sockets_in.items():
            if val == old:
                self.sockets_in[key] = new

    def header(self):
        result = ""
        def print(*args,sep = ' ',end = '\n'):
            nonlocal result
            result += sep.join(map(str,args)) + end
        print("="*64)
        recipe = self.recipe
        facility_amount = (to_str(self.quantity)+" ") if self.quantity != 1 else ""
        if type(recipe.output) is list:
            ix = 0
            main_amount = recipe.output_amount[ix]
            ln = "%s [%du/%ds]"%(recipe.output[0],
                               main_amount,recipe.processing_time)
            for idx,item in enumerate(recipe.output):
                if idx != ix:
                    nl = " + %s [%du/%ds]"%(item,
                                   recipe.output_amount[idx],recipe.processing_time)
                    if len(ln + nl) > 32:
                        print(ln)
                        ln = nl
                    else:
                        ln += nl
            print(ln)
            print(facility_amount+str(recipe.fullname))
        else:
            print("%s%s [%du/%ds] - %s"%(facility_amount,recipe.output,
                               recipe.output_amount,recipe.processing_time,
                               recipe.fullname))
        print("-"*32)
        return result

    def label(self):
        return "%s %s: %s" % (to_str(self.quantity),self.recipe.facility.name,
                              " + ".join(map(lambda x: "%d x %s"%(x[1],x[0].name), self.recipe.output_map.items())))
                          

    def serialize(self):
        header = self.header()
        output,basics,stations = self.__serialize__(1,"",self_line = False)
        basic = self.display_cumulative(basics,stations)
        return header + output + basic


    def __serialize__(self,depth,output,self_line = True):
        tabStr = "    "*depth
        fac = self.recipe.facility
        amount = self.quantity
        basics = [(fac,amount)] \
                    if not self.sockets_in.items() else []
        stations = [(fac,amount)] if "Spark" in fac.name else []
        if self_line:
            output += tabStr+"%s %s"%(to_str(amount),self.recipe.fullname) + "\n"
        for resource, socket in self.sockets_in.items():
            if socket is not None:
                output,b,s = socket.__serialize__(depth+1, output)
                basics += b
                stations += s
        return output,basics,stations

    def display_cumulative(self,basics,stations):
        cumul = ""
        if len(basics) > 1:
            cumulative = self.accumulate(basics)
            cumul += self.print_cumulative(cumulative,"Basic Building")
        if len(stations) > 1:
            cumulative = self.accumulate(stations)
            cumul += self.print_cumulative(cumulative,"Ancient Bases")
        return cumul
    
    def print_cumulative(self,cumulative,label):
        result = ""
        def print(*args,sep = ' ',end = '\n'):
            nonlocal result
            result += sep.join(map(str,args)) + end
        print()
        print("Total %s Requirements:"%label)
        for recipe in sorted(cumulative.keys(),key = lambda x: str(x)):
            print("\t",
                      "[%0.2f]"%cumulative[recipe],
                      "%9s"%str(cumulative[recipe]),
                      recipe)
        print()
        return result

    def accumulate(self,listing):
        cumulative = {}
        for recipe, amount in listing:
            if recipe not in cumulative:
                cumulative[recipe] = 0
            cumulative[recipe] += amount
        return cumulative
    
    def collect(self):
        nodes = self.__collect__(set())
        nodes = list(nodes)
        reverse_nodes = {node:ix for ix, node in enumerate(nodes)}
        return [
                   {"recipe":node.recipe.fullname,
                    "qNum":node.quantity.numerator,
                    "qDenom":node.quantity.denominator,
                    "resource":node.resource.name if node.resource else "",
                    "terminal":node.terminal,
                    "in":{sin.name:reverse_nodes[node] for sin,node in node.sockets_in.items() if node},
                    "out":{sout.name:reverse_nodes[node] for sout,node in node.sockets_out.items() if node}
                    } 
                for node in nodes if node
               ]
        
    def pack(self):
       return self.collect()
   
    @staticmethod 
    def unpack(data):
        recipe_fullname = data['recipe']
        recipe = Recipes.recipes_by_fullname[recipe_fullname]
        resource = Resources[data["resource"]] if data["resource"] else None
        quantity = Fraction(data["qNum"],data["qDenom"])
        return ProductionGraphRecipeNode(recipe, resource = resource, quantity = quantity)
    
    @staticmethod
    def UnpackNetwork(data):
        terminal = None
        nodes = [ProductionGraphRecipeNode.unpack(entry) for entry in data]
        for entry,node in zip(data,nodes):
            for res,target in entry["in"].items():
                resource = Resources[res]
                node.sockets_in[resource] = nodes[target]
            for res,target in entry["out"].items():
                resource = Resources[res]
                node.sockets_out[resource] = nodes[target]
            node.terminal = entry["terminal"]
            if node.terminal:
                terminal = node
        return terminal
    
    def __collect__(self,found = None):
        if found is None:
            found = set()
        found.add(self)
        for res,endpoint in self.sockets_out.items():
            if endpoint and endpoint not in found: endpoint.__collect__(found)
        for res,endpoint in self.sockets_in.items():
            if endpoint and endpoint not in found: endpoint.__collect__(found)
        return found
    
    def __hash__(self):
        return hash(repr(self))

"""
class ProductionGraphEndNode(ProductionGraphNode):
    def __init__(self, resource, terminalNode = None, rate = None, parent = None):
        self.resource = resource
        self.terminal = None
        if terminalNode is not None:
            rate = Fraction(terminalNode.quantity * terminalNode.recipe.output_map[resource],
                            terminalNode.recipe.processing_time)
            terminalNode.terminate(resource,self)
            self.terminal = terminalNode
        else:
            if rate is None:
                rate = Fraction(1)
            else:
                if type(rate) is float:
                    raise TypeError("Rate must be a Fraction")
                if type(rate) is int:
                    rate = Fraction(rate)
        self.rate = rate
        self.parent = parent
        if self.parent:
            parent.add_end_node(self)
    
    def retarget(self,old,new):
        if self.terminal == old:
            self.terminal = new
            self.rate = Fraction(old.quantity * old.recipe.output_map[self.resource],
                                 old.recipe.processing_time)
"""
            
BaseGraphs = {recipe:ProductionGraphRecipeNode(recipe,resource = resource)
              for resource in Recipes.recipes.keys()
              for recipe in Recipes.recipes[resource] 
              }