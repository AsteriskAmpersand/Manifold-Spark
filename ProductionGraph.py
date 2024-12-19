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
from collections import defaultdict

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
            self.sockets_out[rsr] = None
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
                           
    def total_outputs(self):
        outputs = defaultdict(int)
        for res,node in self.sockets_out.items():
            if node is None:
                outputs[res] += Fraction(self.recipe.output_map[res]*self.quantity,self.recipe.processing_time)
        for res,node in self.sockets_in.items():
            if node:
                outs = node.total_outputs()
                for key in outs:
                    outputs[key] += outs[key]
        return outputs
    
    def total_inputs(self):
        inputs = defaultdict(lambda: 0)
        for res,node in self.sockets_in.items():
            if node:
                if node.recipe.raw:
                    inputs[res] += Fraction(node.recipe.output_map[res]*node.quantity,node.recipe.processing_time)
                else:
                    inps = node.total_inputs()
                    for key in inps:
                        inputs[key] += inps[key]
        return inputs
    
    def closure(self):
        outputs = self.total_outputs()
        inputs = self.total_inputs()
        net_ins = defaultdict(int)
        net_outs = defaultdict(int)
        for res in set(outputs.keys()).union(set(inputs.keys())):
            net = outputs[res] - inputs[res]
            if net < 0:
                net_ins[res] = -net
            elif net > 0:
                net_outs[res] = net
        return net_ins,net_outs
    
    def closure_equivalence(self,resource):
        outputs = self.total_outputs()
        _,closure_outputs = self.closure()
        if closure_outputs[resource] <= 0:
            return self.quantity
        return Fraction(outputs[resource],closure_outputs[resource])*self.quantity
    
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
        if isinstance(obj,Recipe):
            return self._substitute_recipe(obj)
        if isinstance(obj,ProductionGraphRecipeNode):
            return self._substitute_node(obj.copy(self.parent))
        raise NotImplementedError("Substitution not implemented for type %s"%type(obj))
    
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

    def header(self,output = None):
        result = ""
        def print(*args,sep = ' ',end = '\n'):
            nonlocal result
            result += sep.join(map(str,args)) + end
        print("="*64)
        recipe = self.recipe
        facility_amount = (to_str(self.quantity)+" ") if self.quantity != 1 else ""
        if output is None:
            output = recipe.output_map
        if isinstance(output,dict):
            if output:
                res = next(iter(output.keys()))
                if self.resource:
                    if self.resource in output:
                        res = self.resource
                main_amount = Fraction(output[res]*self.quantity,recipe.processing_time)
                
                ln = "%s [%du/%ds]"%(res.name,
                                   main_amount.numerator,
                                   main_amount.denominator)
                for resx,amt in output.items():
                    if resx != res:
                        nl = " + %s [%du/%ds]"%(resx.name,
                                       output[resx],recipe.processing_time)
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
    
    def serialize_closure(self):
        nins,nouts = self.closure()
        tins,touts = self.total_inputs(),self.total_outputs()
        rin_ratio = {key:(nins[key] if (key in nins or key in nouts) else 0)/tins[key] 
                     for key in tins if tins[key] != nins[key]}
        per_fac_out = {r:Fraction(o*self.recipe.processing_time,self.quantity) for r,o in nouts.items()}
        header = self.header(per_fac_out)
        output,basics,stations = self.__serialize__(1,"",self_line = False,input_scale = rin_ratio)
        basic = self.display_cumulative(basics,stations)
        return header + output + basic


    def __serialize__(self,depth,output,self_line = True,input_scale = {}):
        tabStr = "    "*depth
        fac = self.recipe.facility.name
        if self.recipe.raw:
            if self.resource in input_scale:
                if input_scale[self.resource] <= 0:
                    fac = "%s Self-Supply from Outputs"%self.resource
                else:
                    fac += " + Self-Supply"
        if len(self.recipe.output_map) == 1:
            fac += " (%s)"%self.recipe.output
        adj = input_scale[self.resource] if self.recipe.raw and self.resource in input_scale else 1
        amount = self.quantity * adj
        basics = [(fac,amount)] \
                    if not self.sockets_in.items() and amount else []
        stations = [(fac,amount)] if "Spark" in fac else []
        if self_line:
            recipename = self.recipe.fullname
            if self.recipe.raw and self.resource in input_scale:
                if input_scale[self.resource]:
                    recipename += " + Self-Supplied"
                else:
                    recipename = "Self-Supplied"
            output += tabStr+"%s %s"%(to_str(amount) if amount else "%s Fully"%self.resource.name,
                                      recipename) + "\n"
        for resource, socket in self.sockets_in.items():
            if socket is not None:
                output,b,s = socket.__serialize__(depth+1, output,input_scale = input_scale)
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

            
BaseGraphs = {recipe:ProductionGraphRecipeNode(recipe,resource = resource)
              for resource in Recipes.recipes.keys()
              for recipe in Recipes.recipes[resource] 
              }
if __name__ in "__main__":
    """
    for r in BaseGraphs:
        if "Plant" in r.facility.name:
            w = r
            
    BGL = list(BaseGraphs.keys())
    import random
    for _ in range(20):
        ix = random.randint(0,len(BaseGraphs))
        i = BGL[ix]
        w = BaseGraphs[i]
        print(w.serialize())
        print(dict(map(lambda x: (x[0].name,x[1]), w.total_outputs().items())))
        print(dict(map(lambda x: (x[0].name,x[1]), w.total_inputs().items())))
        print()
        print()

    import json
    from Recipes import ClosedRecipe
    with open(r'D:/Oddsparks/Scripts/Oddsparks-Production-Editor/test_recipes/Closed Coral.json') as inf:
        jn = json.load(inf)
        g = ProductionGraphRecipeNode.UnpackNetwork(jn)
        r = ClosedRecipe(g)
"""
    for r in BaseGraphs:
        if "Furnace" in r.facility.name:
            for re,a in r.output_map.items():
                if re.name == "Copper Seed":
                    s = BaseGraphs[r]
    print(s.serialize())
    print(s.serialize_closure())
    a = s.closure_equivalence(Resources["Copper Seed"])
    s.adjust_quantity(a.numerator,a.denominator,fset=True)
    print(s.serialize_closure())