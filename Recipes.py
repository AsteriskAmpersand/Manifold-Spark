# -*- coding: utf-8 -*-
"""
Created on Fri Dec 13 02:15:40 2024

@author: Asterisk
"""
from fractions import Fraction
from Resources import Resources
from Facilities import Facilities
from util import to_str


class RecipeList():
    def __init__(self):
        self.recipes = {}
        self.ratios = {}
        self.recipes_by_fullname = {}
        
    def add(self,fac):
        if type(fac.output) is list:
            for output in fac.output:
                self.insert(output,fac)
        else:
            self.insert(fac.output,fac)

    def insert(self,resource,recipe):
        self.recipes_by_fullname[recipe.fullname] = recipe
        if resource not in self.recipes:
            self.recipes[resource] = []
        #if len(self.recipes[resource])>1:
        #    print("Repeated Recipe",resource)
        self.recipes[resource].append(recipe)

    def __getitem__(self,key):
        return self.recipes[key]
    
    def ratioHash(self,resource,recipe):
        return hash(str(resource)+str(recipe))
    
    def calcRatios(self):
        #networks = {}
        for key in self.recipes:
            for rcp in self.recipes[key]:
                rcp.calcRatios(self)
            #networks[self.recipes[key]] = ratios
        for key in self.recipes:
            #print(key)
            network = ProductionNetwork()
            for rcp in self.recipes[key]:
            #    self.ratios[key+rcp] = rcp.chainRate(network) +\
            #                            rcp
                self.ratios[self.ratioHash(key,rcp)] = rcp.chainRate(network)  
            
    def __printDependencies__(self,fac,amount,tabs, cast_float = False):
        tabStr = "    "*tabs
        basics = [(fac,amount)] if not fac.network.recipes.items() else []
        stations = [(fac,amount)] if "Spark" in fac.name else []
        for inp, ratio in fac.network.recipes.items():
            recipe = inp
            local_amount = amount * ratio
            strfunc = (lambda x: "%0.2f"%float(x)) if cast_float else to_str 
            print(tabStr+"%s %s"%(strfunc(local_amount),recipe.fullname))
            b,s = self.__printDependencies__(recipe,local_amount,tabs+1,cast_float)
            basics += b
            stations += s
        return basics, stations
            
            
    def printDependencies(self, cast_float = False):
        if not self.ratios:
            self.calcRatios()
        for key in self.recipes:
            for recipe in self.recipes[key]:
                if not recipe.raw:
                    tabs = 1
                    print("="*64)
                    if type(recipe.output) is list:
                        ix = recipe.output.index(key)
                        main_amount = recipe.output_amount[ix]
                        ln = "%s [%du/%ds]"%(key,
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
                        print(str(recipe.fullname))
                    else:
                        print("%s [%du/%ds] - %s"%(key,
                                           recipe.output_amount,recipe.processing_time,
                                           recipe.fullname))
                    print("-"*32)
                    basics,stations = self.__printDependencies__(recipe,
                                               Fraction(1,1),
                                               tabs, cast_float)
                    self.display_cumulative(basics,stations)
                    print("="*64)
                    print()
            
    def display_cumulative(self,basics,stations):
        if len(basics) > 1:
            cumulative = self.accumulate(basics)
            self.print_cumulative(cumulative,"Basic Building")
        if len(stations) > 1:
            cumulative = self.accumulate(stations)
            self.print_cumulative(cumulative,"Ancient Bases")
        
        return basics
    
    def print_cumulative(self,cumulative,label):
        print()
        print("Total %s Requirements:"%label)
        for recipe in sorted(cumulative.keys(),key = lambda x: str(x)):
            print("\t",
                      "[%0.2f]"%cumulative[recipe],
                      "%9s"%str(cumulative[recipe]),
                      recipe)
        print()        
    
    def accumulate(self,listing):
        cumulative = {}
        for recipe, amount in listing:
            if recipe not in cumulative:
                cumulative[recipe] = 0
            cumulative[recipe] += amount
        return cumulative
        
    
    def scaleDependencyChain(self,resource,scale,cast_float=False):
        recipe = self.recipes[Resources[resource]]
        tabs = 1
        print("="*64)
        print("%s [%du/%ds] - %s"%(resource + " x%s"%str(scale),
                               recipe.output_amount*scale,recipe.processing_time,
                               "" if scale == 1 else "%sx "%to_str(scale) + recipe.fullname))
        print("-"*32)
        self.__printDependencies__(recipe,
                                   Fraction(scale),
                                   tabs,cast_float)
        print("="*64)
        print()
    
# Recipe Ratio		Input# x CraftRate / InputCraftRate		
        
Recipes = RecipeList()

class Recipe():
    def __init__(self,facility,output,inputs,processing_time,output_amount = 1,
                 include = True, temp = None, active = True, raw = False):
        self.raw = raw
        self.name = facility.name
        self.facility = facility
        #if type(output_amount) is tuple:
        #    self.craft_rate = Fraction(1,max(output_amount*processing_time))
        #else:
        #    self.craft_rate = Fraction(1,output_amount*processing_time)
        self.output = output
        self.output_amount = output_amount
        self.inputs = [(i,a) for i,a in inputs]#Do not divide by output amount, processing time already is doing this
        self.primitive = len(self.inputs) == 0
        self.processing_time = Fraction(processing_time,1)#Fraction(processing_time,self.output_amount)
        self.network = None
        if temp is None:
            temp = facility.temperature
        self.temperature = temp
        if active:
            if include: 
                Recipes.add(self)
            facility.recipes.append(self)
            if type(output) is list:
                for suboutput in output:
                    suboutput.recipes_as_output.append(self)
            else:
                output.recipes_as_output.append(self)
            for (i,a) in self.inputs:
                i.recipes_as_input.append(self)
        
    @property
    def output_map(self):
        if type(self.output) is list:
            return {rsr:val for rsr,val in zip(self.output,self.output_amount)}
        else:
            return {self.output:self.output_amount}
        
    def __hash__(self):
        return hash(self.fullname)
        
    def __add__(self,forn):
        if type(forn) is ProductionNetwork:
            return forn + self
        
    def __mul__(self,mul):
        n = ProductionNetwork()
        return n.add(self,mul)
    
    def __rmul__(self,mul):
        return mul*self
    
    def calcRatios(self,facl):
        n = ProductionNetwork()
        for i,a in self.inputs:
            rcl = facl[i]
            if len(rcl) == 2:
                recipe = rcl[1]
            else:
                recipe = rcl[0]
            output_amount = recipe.output_map[i]
            craft_rate = output_amount/recipe.processing_time
            consume_rate = a / self.processing_time
            n.add(recipe,consume_rate/craft_rate)
        self.network = n
        return n
    
    @property
    def fullname(self):
        if type(self.output) is list:
            output = " + ".join([ amount +" "+itm for itm, amount in zip(map(str,self.output),map(str,self.output_amount))])
        else:
            output = "%d %s" % (self.output_amount,str(self.output))
        inp = " + ".join(map(lambda x: "%d %s" % (x[1],x[0].name), self.inputs))
        return self.facility.name + " [%s -> %s]"%(inp,output)
    
    def chainRate(self,network):
        if self.network is None:
            raise EnvironmentError("Cannot calculate full production dependencies without first calculating local")
        return self.network.full_network()
    
    def __str__(self):
        return self.fullname
    
    def __repr__(self):
        return "%s [%s -> %s {%ds}] "%(self.fullname,
                               ', '.join(("%s x%d"%(i,a) for i,a in self.inputs)),
                               self.output,self.processing_time)

for resource in Resources:
    Recipe(
            facility = Facilities['Manual Collection per Second'],
            output = Resources[resource],
            inputs = [],
            output_amount = 1,
            processing_time = 1,
            raw = True
            )
    Recipe(
            facility = Facilities['Compressor'],
            output = [],
            inputs = [(Resources[resource],1)],
            output_amount = (),
            processing_time = 2,
            raw = True
            )

class ProductionNetwork():
    def __init__(self,dct=None):
        self.recipes = {}
        if type(dct) is ProductionNetwork:
            self.recipes = {k:v for k,v in dct.recipes.items()}
        elif type(dct) is Recipe:
            self.recipes[dct] = Fraction(1,1)
            
    def add(self,recipe,amount):
        if type(amount) is int:
            amount = Fraction(amount,1)
        elif type(amount) is float:
            raise ValueError("Cannot add "+recipe.name+" to network with float amount %f"%amount)
        if recipe in self.recipes:
            self.recipes[recipe] += amount
        else:
            self.recipes[recipe] = amount
        return self
    
    def __str__(self):
        return '\n'.join({"%s\t%s"%(to_str(v),str(k)) for k,v in self.recipes.items()})
    
    def __repr__(self):
        return repr({repr(k):v for k,v in self.recipes.items()})
    
    def __add__(self,netOrFac):
        recipes = self.recipes
        if type(netOrFac) is ProductionNetwork:
            net = ProductionNetwork()
            fkeys = recipes.keys()
            raddkeys = netOrFac.recipes.keys()
            raddfac = netOrFac.recipes
            for key in set(fkeys).union(set(raddkeys)):
                amount = recipes[key] if key in fkeys else 0
                raddamount = raddfac[key] if key in raddkeys else 0
                net.add(key,amount+raddamount)         
        elif type(netOrFac) is Recipe:
            net = ProductionNetwork(self)
            net.add(netOrFac,1)
        return net
    
    def __mul__(self,mult):
        net = ProductionNetwork(self)
        if type(mult) is float:
            raise ValueError("Cannot multiply network with float amount %f"%mult)
        elif type(mult) is int:
            mult = Fraction(mult,1)
        for key,amount in self.recipes.items():
            net.recipes[key] *= mult
        return net
    
    def __rmul__(self,mult):
        return self*mult
    
    def full_network(self):
        n = ProductionNetwork()
        for recipe,amount in self.recipes.items():
            n.add(recipe,amount)
            try:
                n += amount * recipe.network.full_network()
            except:
                print(recipe)
                raise
        return n
    
import RecipeData

for text_recipe in RecipeData.TextRecipeList:
    dic = text_recipe.kwargs 
    dic['facility'] = Facilities[dic['facility']]
    dico = dic['output']
    dic['output'] = list(map(lambda x: Resources[x],dico)) if type(dico) is list else Resources[dico]
    dic['inputs'] = list(map(lambda x: (Resources[x[0]],x[1]), dic['inputs']))
    Recipe(**text_recipe.kwargs)
    
Recipes.calcRatios()