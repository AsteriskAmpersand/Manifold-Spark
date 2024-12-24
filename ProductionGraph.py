# -*- coding: utf-8 -*-
"""
Created on Fri Dec 13 02:30:11 2024

@author: Asterisk
"""
from Resources import Resources
from Facilities import Facilities
from Recipes import Recipe,Recipes,CyclicalRecipes
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
    @staticmethod
    def unpack(data):
        if "type" in data:
            if data["type"] == "Merger":
                return MergerNode.unpack(data)
            elif data["type"] == "Recipe":
                return RecipeNode.unpack(data)
            else:
                raise TypeError("Type %s does not have an unpacking method"%data["type"])
        else:
            return RecipeNode.unpack(data)
        
    def pack(self):
        nodes,reverse_nodes = self.collect()
        return [node.__pack__(nodes,reverse_nodes) for node in nodes]
        
    def collect(self):
        nodes = self.__collect__(set())
        nodes = list(nodes)
        reverse_nodes = {node:ix for ix, node in enumerate(nodes)}
        return nodes, reverse_nodes

    def __collect__(self,found = None):
        if found is None:
            found = set()
        found.add(self)
        for res,endpoint in self.sockets_out.items():
            if endpoint and endpoint not in found: endpoint.__collect__(found)
        for _,endpoint in self.get_input_sockets():
            if endpoint and endpoint not in found: endpoint.__collect__(found)
        return found
        
    @staticmethod
    def UnpackNetwork(data):
        terminal = None
        nodes = [ProductionGraphNode.unpack(entry) for entry in data]
        """
        for ix,(node,entry) in enumerate(zip(nodes,data)): 
            if isinstance(node,RecipeNode):
                frint(ix,"[%s]"%(",".join(map(str,entry["in"].values()))),
                      node.recipe.fullname,
                      "[%s]"%(",".join(map(str,entry["out"].values()))),
                      "*" if "terminal" in entry and entry["terminal"] else "")
            else:
                frint(ix,"[%s]"%(",".join(map(str,entry["in"]))),
                      "Merger %s/%s"%(node.ratio.numerator,node.ratio.denominator),
                      "[%s]"%(",".join(map(str,entry["out"].values()))))
        """
        for entry,node in zip(data,nodes):
            node.set_sockets(entry,nodes)
            node.terminal = entry["terminal"] if "terminal" in entry else False
            if node.terminal:
                terminal = node
        return terminal
    
    def remove(self):
        if self.parent:
            self.parent.remove(self)
        for val in self.sockets_in.values():
            if type(val) is ProductionGraphNode:
                val.remove()
                                   
    def __hash__(self):
        return hash(repr(self))
    
        
class MergerNode(ProductionGraphNode):
    def __init__(self, resource, ratio = None, parent = None, quantity = None, output = None):
        self.parent = parent
        if self.parent:
            self.parent.add(self)
        self.resource = resource
        self.sockets_out = {resource:output}
        self.sockets_in = [RecipeNode(fetchRecipe(self.resource),
                            resource = self.resource,
                            outputs = {self.resource:self},
                            quantity = Fraction(1),
                            parent = self.parent) for _ in range(2)]
        if ratio is None:
            ratio = Fraction(1)
        if ratio < 0 or ratio > 1:
            raise ValueError("Merger cannot have weights under 0 or over 1")
        self.ratio = Fraction(ratio)
        self.quantity = Fraction(1) if quantity is None else quantity

    def __pack__(self,nodes,reverse_nodes):
        return {
         "resource":self.resource.name if self.resource else "",
         "ratio_num":self.ratio.numerator,
         "ratio_denom":self.ratio.denominator,
         "qNum":self.quantity.numerator,
         "qDenom":self.quantity.denominator,
         "in":[reverse_nodes[node] for node in self.sockets_in if node],
         "out":{sout.name:reverse_nodes[node] for sout,node in self.sockets_out.items() if node},
         "type":"Merger"
         } 
   
    @staticmethod 
    def unpack(data):
        resource = Resources[data["resource"]]
        ratio = Fraction(data["ratio_num"],data["ratio_denom"])
        quantity = Fraction(data["qNum"],data["qDenom"])
        return MergerNode(resource, ratio = ratio, quantity = quantity)
    
    def set_sockets(self,entry,nodelist):
        self.sockets_in = [nodelist[ix] for ix in entry["in"]]
        for res,target in entry["out"].items():
            resource = Resources[res]
            self.sockets_out[resource] = nodelist[target]
        
    def copy(self, new_parent = None):
        if new_parent is None:
            new_parent = self.parent
        nnode = type(self)(self.resource,self.ratio,new_parent,self.quantity)
        sockets_in = []
        for node_in in self.sockets_in:
            if node_in is not None:
                copied_input = node_in.copy(new_parent)
                sockets_in.append(copied_input)
                copied_input.sockets_out[self.resource] = nnode
            else:
                sockets_in.append(node_in)
        nnode.sockets_in = sockets_in
        return nnode
    
    def get_input_sockets(self):
        return [(self.resource,inp) for inp in self.sockets_in]

    def adjust_ratio(self, num, denom):
        self.ratio = Fraction(num,denom)
        self.adjust_quantity(resource = self.resource, resource_target = self.quantity)
    
    def adjust_quantity(self,*args,resource = None, resource_target = None, **kwargs):
        if self.resource != resource:
            raise ValueError("Merger Node cannot adjust for resources it is not configured to merge")
        if resource_target is None:
            raise ValueError("Resource target cannot be none for Merger Node")
        self.quantity = resource_target
        node = self.sockets_in[0]
        node.adjust_quantity(resource = resource, resource_target = resource_target * self.ratio)
        node = self.sockets_in[1]
        node.adjust_quantity(resource = resource, resource_target = resource_target * (1-self.ratio))
        
    
    def set_top(self,inp):
        if inp.resource != self.resource:
            raise ValueError("Input Resource Mismatch")
        self.sockets_in[0] = inp
    
    def set_bottom(self,inp):
        if inp.resource != self.resource:
            raise ValueError("Input Resource Mismatch")
        self.sockets_in[1] = inp
        
    def total_inputs(self):
        inputs = defaultdict(lambda: 0)
        for ix,(res,node) in enumerate(self.get_input_sockets()):
            if node:
                if hasattr(node,"recipe") and node.recipe.raw:
                    inputs[self.resource] += Fraction(node.recipe.output_map[res]*node.quantity,node.recipe.processing_time)
                else:
                    inps = node.total_inputs()
                    for res in inps:
                        inputs[res] += inps[res]
        return inputs
                
    def total_outputs(self):
        outputs = defaultdict(int)
        for res,node in self.get_input_sockets():
            if node:
                outs = node.total_outputs()
                for key in outs:
                    outputs[key] += outs[key]
        return outputs

    def substitute(self,obj):
        if isinstance(obj,Recipe):
            nn = RecipeNode(obj,resource = self.resource, outputs = self.sockets_out,
                            quantity = 1, parent = self.parent)
        elif isinstance(obj,RecipeNode):
            nn = obj.copy(self.parent)
            obj.resource = self.resource
            obj.sockets_out[self.resource] = self.sockets_out[self.resource]
        else:
            raise NotImplementedError("Substitution not implemented for type %s"%type(obj))
        self.sockets_out[self.resource].retarget(self,nn)
        nn.adjust_quantity(resource = self.resource, resource_target = self.quantity)
        return nn
        
    def __serialize__(self,depth,output,self_line = True,input_scale = {}):
        if self.ratio == 1:
            return self.sockets_in[0].__serialize__(depth,output,self_line,input_scale)
        elif self.ratio == 0:
            return self.sockets_in[1].__serialize__(depth,output,self_line,input_scale)
        tabStr = "    "*depth
        basics = []
        stations = []
        if self_line:
            recipename = "%s Input Flow Merger"%self.resource.name
            output += tabStr+"%s"%(recipename) + "\n"
        for resource, socket in self.get_input_sockets():
            if socket is not None:
                output,b,s = socket.__serialize__(depth+1, output,input_scale = input_scale)
                basics += b
                stations += s
        return output,basics,stations
    
    def retarget(self,old,new):
        for ix,(key,val) in enumerate(self.get_input_sockets()):
            if val == old:
                self.sockets_in[ix] = new

class RecipeNode(ProductionGraphNode):
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
                           RecipeNode(fetchRecipe(inp),
                                                     resource = inp,
                                                     outputs = {inp:self},
                                                     quantity = recipeQuantity(fetchRecipe(inp),
                                                                               recipe,inp,
                                                                               quantity),
                                                     parent = self.parent)

    def get_input_sockets(self):
        return list(self.sockets_in.items())

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
                if hasattr(node,"recipe") and node.recipe.raw:
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
        nnode = RecipeNode(recipe,resource = self.resource, 
                                  outputs = {self.resource:self.sockets_out[self.resource]},
                                  quantity = new_quantity, 
                                  parent = self.parent)
        sout = self.sockets_out[self.resource]
        if sout:
            sout.retarget(self,nnode)
        self.remove()
        return nnode        
    
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
    
    def _substitute_merger(self,obj):
        res = obj.resource
        q = Fraction(self.recipe.output_map[res]*self.quantity,self.recipe.processing_time)
        merger = MergerNode(res,obj.ratio,parent = self.parent,output=self.sockets_out[res])
        cpy = self.copy()
        merger.set_top(cpy)
        merger.adjust_quantity(resource = res,resource_target = q)
        target = self.sockets_out[res]
        if target is not None:
            target.retarget(self,merger)
            cpy.sockets_out[merger.resource] = merger
        self.remove()
        return merger

    def substitute(self,obj):
        #if type(obj) is ProductionGraph:
        #    self._substitute_graph(obj)
        if isinstance(obj,Recipe):
            return self._substitute_recipe(obj)
        if isinstance(obj,RecipeNode):
            if hasattr(obj,"terminal"):
                obj.terminal = self.terminal
            return self._substitute_node(obj.copy(self.parent))
        if isinstance(obj,MergerNode):
            return self._substitute_merger(obj)
        raise NotImplementedError("Substitution not implemented for type %s"%type(obj))
        
    def adjust_quantity(self,numerator=1,denominator=1,resource = None, resource_target = None, fset = False):
        if fset:
            new_quantity = Fraction(numerator,denominator)
        else:
            new_quantity = resource_target / Fraction(self.recipe.output_map[resource],self.recipe.processing_time)
        self.quantity = new_quantity
        for rsr, node in self.sockets_in.items():
            if node is not None:
                node.adjust_quantity(resource = rsr, resource_target = self.recipe.input_map[rsr]*self.quantity/self.recipe.processing_time)
        return new_quantity
                
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
   
    def __pack__(self,nodes,reverse_nodes):
        return {"recipe":self.recipe.fullname,
         "qNum":self.quantity.numerator,
         "qDenom":self.quantity.denominator,
         "resource":self.resource.name if self.resource else "",
         "terminal":self.terminal if hasattr(self,"terminal") else False,
         "in":{sin.name:reverse_nodes[node] for sin,node in self.sockets_in.items() if node},
         "out":{sout.name:reverse_nodes[node] for sout,node in self.sockets_out.items() if node},
         "type":"Recipe"
         } 
   
    @staticmethod 
    def unpack(data):
        recipe_fullname = data['recipe']
        if recipe_fullname in Recipes.recipes_by_fullname:
            recipe = Recipes.recipes_by_fullname[recipe_fullname]
        else:
            recipe = CyclicalRecipes[recipe_fullname]
        resource = Resources[data["resource"]] if data["resource"] else None
        quantity = Fraction(data["qNum"],data["qDenom"])
        return RecipeNode(recipe, resource = resource, quantity = quantity)


    def set_sockets(self,entry,nodelist):
        for res,target in entry["in"].items():
            resource = Resources[res]
            self.sockets_in[resource] = nodelist[target]
        for res,target in entry["out"].items():
            resource = Resources[res]
            self.sockets_out[resource] = nodelist[target]
    
    def retarget(self,old,new):
        for key,val in self.get_input_sockets():
            if val == old:
                self.sockets_in[key] = new
    

            
BaseGraphs = {recipe:RecipeNode(recipe,resource = resource)
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
        g = RecipeNode.UnpackNetwork(jn)
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