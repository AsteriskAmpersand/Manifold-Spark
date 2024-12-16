# -*- coding: utf-8 -*-
"""
Created on Fri Feb  9 11:39:51 2024

@author: Asterisk
"""
from fractions import Fraction

Resources = {}

class Resource():
    def __init__(self, name, recipes_i = [], recipes_o = [], icon = None):
        self.name = name
        if icon is None:
            base = "./Sparks/" if " Spark" in self.name else "./Resources/"
            self.icon = base+self.name+".png"
        else:
            self.icon = icon
        self.recipes_as_output = recipes_i
        self.recipes_as_input = recipes_o
        Resources[self.name] = self
        
    def __str__(self):
        return self.name
    
    def __hash__(self):
        return hash(self.name)
        

Resource(name = "Coral")
Resource(name = "Fluted Coral")
Resource(name = "Wooden Log")
Resource(name = "Timber")
Resource(name = "Tree Bark")
Resource(name = "Ladder")
Resource(name = "Leaves")
Resource(name = "Leaves (Leaf Knot)")
Resource(name = "Stone")
Resource(name = "Rope")
Resource(name = "Coal")
Resource(name = "Small Vial")
Resource(name = "Big Vial")
Resource(name = "Explosives")
Resource(name = "Fabric")
Resource(name = "Limestone")
Resource(name = "Fertiliser")
Resource(name = "Fertiliser (Enriched)",icon = Resources["Fertiliser"].icon)
Resource(name = "Wooden Panel")
Resource(name = "Wooden Blade")
Resource(name = "Pebbles")
Resource(name = "Stone Plate")
Resource(name = "Path Tile")
Resource(name = "Stone Wheel")
Resource(name = "Stone Spike")
Resource(name = "Quartz")
Resource(name = "Dowsing Stone")
Resource(name = "Stumpy Spark")
Resource(name = "Arty Spark")
Resource(name = "Crafty Spark")
Resource(name = "Carry Spark")
Resource(name = "Choppy Spark")
Resource(name = "Loamy Spark")
Resource(name = "Rocky Spark")
Resource(name = "Scouty Spark")
Resource(name = "Hauling Spark")
Resource(name = "Puffy Spark")
Resource(name = "Boomy Spark")
Resource(name = "Crashy Spark")
Resource(name = "Slashy Spark")
Resource(name = "Drilly Spark")
Resource(name = "Handy Spark")
Resource(name = "Burning Spark")
Resource(name = "Freezing Spark")
Resource(name = "Aetheric Shard")
Resource(name = "Aetheric Pellet")
Resource(name = "Aetheric Shard (Pellet)")
Resource(name = "Aetheric Clump")
Resource(name = "Miasma Vial")
Resource(name = "Raw Aether")
Resource(name = "Refined Aether")
Resource(name = "Aetheric Shard (Raw Aether)",icon=Resources["Aetheric Shard"].icon)
Resource(name = "Aetheric Shard (Refined Aether)",icon=Resources["Aetheric Shard"].icon)
Resource(name = "Miasma")
Resource(name = "Leaf Knot")
Resource(name = "Leaves (Leave Knot)",icon=Resources["Leaves"])
Resource(name = "Frozen Log")
Resource(name = "Frozen Stone")
Resource(name = "Stellar Ice")
Resource(name = "Copper Ore")
Resource(name = "Copper Ingot")
Resource(name = "Coral Seed")
Resource(name = "Dummy")
  

Facilities = {}

class Facility():
    def __init__(self,name,recipes = [], build_cost = [],icon = None, temp = 0):
        self.name = name
        self.build_cost = build_cost
        self.temperature = temp
        if icon is None:
            self.icon = "./Buildings/"+name.replace(" ","_") + ".png"
        else:
            self.icon = icon
        Facilities[self.name] = self
        self.recipes = recipes
        
    def __hash__(self):
        return hash(self.name)
    def __str__(self):
        return self.name
 
        
Facility(
    name = "Alchemy Lab",
    temp = 3
    )
Facility(
    name = "Aetheric Distiller",
    temp = 3
    )
Facility(
    name = "Cutter",
    temp = 3
    )
Facility(
    name = "Drill"
    )
Facility(
    name = "Furnace",
    temp = -3
    )
Facility(
    name = "Logger"
    )
Facility(
    name = "Loom",
    temp = 3
    )
Facility(
    name = "Miasma Collector",
    temp = 5
    )
Facility(
    name = "Miasma Collector (Rate Limited - Crafty)",
    temp = 5
    )
Facility(
    name = "Miasma Collector (Rate Limited - Handy)",
    temp = 5
    )
Facility(
    name = "Noxious Coral"
    )
Facility(
    name = "Sawbench",
    temp = -3
    )
Facility(
    name = "Spark Workbench",
    temp = -3
    )
Facility(
    name = "Spark Workstation",
    temp = 3
    )
Facility(
    name = "Stone Workshop",
    temp = 3
    )
Facility(
    name = "Stonecutter",
    temp = 3
    )
Facility(
    name = "Wood Workshop",
    temp = -3
    )
Facility(
    name = "Manual Collection per Second"
    )
Facility(
    name = "Plant Extractor",
    temp = -3
    )
Facility(
    name = "Greenhouse"
    )
Facility(
    name = "Ore Miner"
    )

class RecipeList():
    def __init__(self):
        self.recipes = {}
        self.ratios = {}
        
    def add(self,fac):
        self.recipes[fac.output] = fac
        
    def __getitem__(self,key):
        if key not in self.recipes:
            r = Recipe(
                    facility = Facilities['Manual Collection per Second'],
                    output = key,
                    inputs = [],
                    output_amount = 1,
                    processing_time = 1,
                    include = False
                    )
            r.calcRatios(RecipeList())
            return r
        return self.recipes[key]
    
    def calcRatios(self):
        #networks = {}
        for key in self.recipes:
            self.recipes[key].calcRatios(self)
            #networks[self.recipes[key]] = ratios
        for key in self.recipes:
            network = Network()
            self.ratios[key] = self.recipes[key].chainRate(network) +\
                                    self.recipes[key]
                  
    def __printDependencies__(self,fac,amount,tabs, cast_float = False):
        tabStr = "    "*tabs
        basics = [(fac,amount)] if not fac.network.recipes.items() else []
        stations = [(fac,amount)] if "Spark" in fac.name else []
        for inp, ratio in fac.network.recipes.items():
            Recipe = inp
            local_amount = amount * ratio
            strfunc = (lambda x: "%0.2f"%float(x)) if cast_float else to_str 
            print(tabStr+"%s %s"%(strfunc(local_amount),Recipe.fullname))
            b,s = self.__printDependencies__(Recipe,local_amount,tabs+1,cast_float)
            basics += b
            stations += s
        return basics, stations
            
            
    def printDependencies(self, cast_float = False):
        if not self.ratios:
            self.calcRatios()
        for key in self.recipes:
            tabs = 1
            Recipe = self.recipes[key]
            print("="*64)
            print("%s [%du/%ds] - %s"%(key,
                                   Recipe.output_amount,Recipe.processing_time,
                                   Recipe.fullname))
            print("-"*32)
            basics,stations = self.__printDependencies__(Recipe,
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
        Recipe = self.recipes[Resources[resource]]
        tabs = 1
        print("="*64)
        print("%s [%du/%ds] - %s"%(resource + " x%s"%str(scale),
                               Recipe.output_amount*scale,Recipe.processing_time,
                               "" if scale == 1 else "%sx "%to_str(scale) + Recipe.fullname))
        print("-"*32)
        self.__printDependencies__(Recipe,
                                   Fraction(scale),
                                   tabs,cast_float)
        print("="*64)
        print()
    
# Recipe Ratio		Input# x CraftRate / InputCraftRate		
        
Recipes = RecipeList()

def to_str(v):
    if type(v) is Fraction:
        if v.denominator == 1:
            return str(v.numerator)
        return "%d/%d"%(v.numerator,v.denominator)
    return str(v)

class Network():
    def __init__(self,dct=None):
        self.recipes = {}
        if type(dct) is Network:
            self.recipes = {k:v for k,v in dct.recipes.items()}
        elif type(dct) is Recipe:
            self.recipes[dct] = Fraction(1,1)
            
    def add(self,Recipe,amount):
        if type(amount) is int:
            amount = Fraction(amount,1)
        elif type(amount) is float:
            raise ValueError("Cannot add "+Recipe.name+" to network with float amount %f"%amount)
        if Recipe in self.recipes:
            self.recipes[Recipe] += amount
        else:
            self.recipes[Recipe] = amount
        return self
    
    def __str__(self):
        return '\n'.join({"%s\t%s"%(to_str(v),str(k)) for k,v in self.recipes.items()})
    
    def __repr__(self):
        return repr({repr(k):v for k,v in self.recipes.items()})
    
    def __add__(self,netOrFac):
        recipes = self.recipes
        if type(netOrFac) is Network:
            net = Network()
            fkeys = recipes.keys()
            raddkeys = netOrFac.recipes.keys()
            raddfac = netOrFac.recipes
            for key in set(fkeys).union(set(raddkeys)):
                amount = recipes[key] if key in fkeys else 0
                raddamount = raddfac[key] if key in raddkeys else 0
                net.add(key,amount+raddamount)         
        elif type(netOrFac) is Recipe:
            net = Network(self)
            net.add(netOrFac,1)
        return net
    
    def __mul__(self,mult):
        net = Network(self)
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
        n = Network()
        for Recipe,amount in self.recipes.items():
            n.add(Recipe,amount)
            try:
                n += amount * Recipe.network.full_network()
            except:
                print(Recipe)
                raise

        return n
        
class Recipe():
    def __init__(self,facility,output,inputs,processing_time,output_amount = 1,
                 include = True, temp = None, active = True):
        self.name = facility.name
        self.facility = facility
        self.craft_rate = Fraction(1,output_amount*processing_time)
        self.output = output
        self.output_amount = output_amount
        self.inputs = [(i,a) for i,a in inputs]#Do not divide by output amount, processing time already is doing this
        self.processing_time = Fraction(processing_time,1)#Fraction(processing_time,self.output_amount)
        self.network = None
        if temp is None:
            temp = facility.temperature
        self.temperature = temp
        if active:
            if include: 
                Recipes.add(self)
            facility.recipes.append(self)
            output.recipes_as_output.append(self)
            for (i,a) in self.inputs:
                i.recipes_as_input.append(self)
        
    def __hash__(self):
        return hash(self.fullname)
        
    def __add__(self,forn):
        if type(forn) is Network:
            return forn + self
        
    def __mul__(self,mul):
        n = Network()
        return n.add(self,mul)
    
    def __rmul__(self,mul):
        return mul*self
    
    def calcRatios(self,facl):
        n = Network()
        for i,a in self.inputs:
            craft_rate = facl[i].output_amount/facl[i].processing_time
            consume_rate = a / self.processing_time
            n.add(facl[i],consume_rate/craft_rate)
        self.network = n
        return n
    
    @property
    def fullname(self):
        return self.facility.name + " [%s]"%self.output
    
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


Recipe(
    facility = Facilities['Logger'],
    output = Resources["Wooden Log"],
    inputs = [],
    processing_time = 2
    )

Recipe(
    facility = Facilities['Logger'],
    output = Resources["Tree Bark"],
    inputs = [],
    processing_time = 2
    )

Recipe(
    facility = Facilities['Logger'],
    output = Resources["Leaves"],
    inputs = [],
    processing_time = 2
    )

#Full Ore Miner
Recipe(
    facility = Facilities['Ore Miner'],
    output = Resources["Copper Ore"],
    inputs = [],
    processing_time = 10,
    active = False
    )

#Ore Miner production speed is given by 60/(level+1)

#Depleted Ore Miner
Recipe(
    facility = Facilities['Ore Miner'],
    output = Resources["Copper Ore"],
    inputs = [],
    processing_time = 60
    )

Recipe(
    facility = Facilities['Sawbench'],
    output = Resources["Timber"],
    inputs = [(Resources["Wooden Log"],2)],
    processing_time = 16
    )

Recipe(
    facility = Facilities['Sawbench'],
    output = Resources["Wooden Panel"],
    inputs = [(Resources["Timber"],2)],
    processing_time = 8
    )

Recipe(
    facility = Facilities['Sawbench'],
    output = Resources["Tree Bark"],
    output_amount = 2,
    inputs = [(Resources["Wooden Log"],1)],
    processing_time = 8, active = False
    )

Recipe(
    facility = Facilities['Wood Workshop'],
    output = Resources["Wooden Blade"],
    inputs = [(Resources["Timber"],1),
              (Resources["Wooden Panel"],2)],
    processing_time = 48
    )

Recipe(
    facility = Facilities['Wood Workshop'],
    output = Resources["Ladder"],
    output_amount = 2,
    inputs = [(Resources["Wooden Log"],4),
              (Resources["Timber"],10)],
    processing_time = 32
    )

Recipe(
    facility = Facilities['Wood Workshop'],
    output = Resources["Explosives"],
    output_amount = 1,
    inputs = [(Resources["Fertiliser"],2),
              (Resources["Limestone"],4)],
    processing_time = 24
    )

Recipe(
    facility = Facilities['Stonecutter'],
    output = Resources["Pebbles"],
    output_amount = 2,
    inputs = [(Resources["Stone"],1)],
    processing_time = 32
    )

Recipe(
    facility = Facilities['Stonecutter'],
    output = Resources["Stone Plate"],
    output_amount = 1,
    inputs = [(Resources["Stone"],2)],
    processing_time = 32
    )

Recipe(
    facility = Facilities['Stonecutter'],
    output = Resources["Limestone"],
    output_amount = 3,
    inputs = [(Resources["Coral"],4)],
    processing_time = 16,
    active = False
    )

Recipe(
    facility = Facilities['Stonecutter'],
    output = Resources["Stone"],
    output_amount = 2,
    inputs = [(Resources["Limestone"],4)],
    processing_time = 8,
    active = False
    )

Recipe(
    facility = Facilities['Stonecutter'],
    output = Resources["Coral"],
    output_amount = 8,
    inputs = [(Resources["Fluted Coral"],1)],
    processing_time = 32,
    active = False
    )

Recipe(
    facility = Facilities['Stone Workshop'],
    output = Resources["Dowsing Stone"],
    output_amount = 3,
    inputs = [(Resources["Quartz"],1),
              (Resources["Rope"],1)],
    processing_time = 24
    )

Recipe(
    facility = Facilities['Stone Workshop'],
    output = Resources["Path Tile"],
    output_amount = 5,
    inputs = [(Resources["Limestone"],5),
              (Resources["Pebbles"],10)],
    processing_time = 32
    )

Recipe(
    facility = Facilities['Stone Workshop'],
    output = Resources["Stone Wheel"],
    output_amount = 2,
    inputs = [(Resources["Path Tile"],4),
              (Resources["Stone Plate"],2)],
    processing_time = 16
    )

Recipe(
    facility = Facilities['Stone Workshop'],
    output = Resources["Stone Spike"],
    output_amount = 4,
    inputs = [(Resources["Stone Plate"],4),
              (Resources["Wooden Blade"],1)],
    processing_time = 16
    )

Recipe(
    facility = Facilities['Spark Workbench'],
    output = Resources["Stumpy Spark"],
    inputs = [(Resources["Aetheric Shard"],1),
              (Resources["Wooden Log"],5)],
    processing_time = 32
    )

Recipe(
    facility = Facilities['Spark Workbench'],
    output = Resources["Arty Spark"],
    inputs = [(Resources["Stumpy Spark"],2),
              (Resources["Rope"],5)],
    processing_time = 32
    )

Recipe(
    facility = Facilities['Spark Workbench'],
    output = Resources["Crafty Spark"],
    inputs = [(Resources["Stumpy Spark"],2),
              (Resources["Wooden Panel"],2)],
    processing_time = 48
    )

Recipe(
    facility = Facilities['Spark Workbench'],
    output = Resources["Choppy Spark"],
    inputs = [(Resources["Stumpy Spark"],3),
              (Resources["Wooden Blade"],2)],
    processing_time = 64
    )

Recipe(
    facility = Facilities['Spark Workbench'],
    output = Resources["Carry Spark"],
    inputs = [(Resources["Crafty Spark"],1),
              (Resources["Timber"],4)],
    processing_time = 32
    )

Recipe(
    facility = Facilities['Spark Workbench'],
    output = Resources["Loamy Spark"],
    output_amount = 5,
    inputs = [(Resources["Aetheric Shard"],5),
              (Resources["Fertiliser"],3)],
    processing_time = 32
    )

Recipe(
    facility = Facilities['Spark Workstation'],
    output = Resources["Rocky Spark"],
    output_amount = 1,
    inputs = [(Resources["Stumpy Spark"],2),
              (Resources["Stone"],5)],
    processing_time = 32
    )

Recipe(
    facility = Facilities['Spark Workstation'],
    output = Resources["Scouty Spark"],
    output_amount = 1,
    inputs = [(Resources["Stumpy Spark"],1),
              (Resources["Dowsing Stone"],1)],
    processing_time = 32
    )

Recipe(
    facility = Facilities['Spark Workstation'],
    output = Resources["Hauling Spark"],
    output_amount = 1,
    inputs = [(Resources["Carry Spark"],2),
              (Resources["Stone Wheel"],4)],
    processing_time = 64
    )

Recipe(
    facility = Facilities['Spark Workstation'],
    output = Resources["Puffy Spark"],
    output_amount = 1,
    inputs = [(Resources["Rocky Spark"],1),
              (Resources["Fabric"],4)],
    processing_time = 32
    )

Recipe(
    facility = Facilities['Spark Workstation'],
    output = Resources["Boomy Spark"],
    output_amount = 1,
    inputs = [(Resources["Rocky Spark"],3),
              (Resources["Explosives"],5)],
    processing_time = 48
    )

Recipe(
    facility = Facilities['Spark Workstation'],
    output = Resources["Crashy Spark"],
    output_amount = 1,
    inputs = [(Resources["Boomy Spark"],2),
              (Resources["Stone Spike"],7)],
    processing_time = 64
    )

Recipe(
    facility = Facilities['Spark Workstation'],
    output = Resources["Slashy Spark"],
    output_amount = 1,
    inputs = [(Resources["Rocky Spark"],2),
              (Resources["Choppy Spark"],3)],
    processing_time =64
    )

Recipe(
    facility = Facilities['Cutter'],
    output = Resources["Fertiliser"],
    output_amount = 2,
    inputs = [(Resources["Leaves"],4)],
    processing_time = 24
    )

Recipe(
    facility = Facilities['Cutter'],
    output = Resources["Aetheric Pellet"],
    output_amount = 6,
    inputs = [(Resources["Aetheric Clump"],1)],
    processing_time = 128
    )

Recipe(
    facility = Facilities['Drill'],
    output = Resources["Stone"],
    output_amount = 1,
    inputs = [],
    processing_time = 2
    )

Recipe(
    facility = Facilities['Drill'],
    output = Resources["Quartz"],
    output_amount = 1,
    inputs = [],
    processing_time = 2
    )

Recipe(
    facility = Facilities['Drill'],
    output = Resources["Limestone"],
    output_amount = 1,
    inputs = [],
    processing_time = 2
    )

Recipe(
    facility = Facilities['Noxious Coral'],
    output = Resources["Miasma"],
    output_amount = 1,
    inputs = [],
    processing_time = 12 #Crafties
    )#Produces Miasma every 4 seconds

Recipe(
    facility = Facilities['Miasma Collector'],
    output = Resources["Miasma Vial"],
    output_amount = 2,
    inputs = [(Resources["Small Vial"],2),
              (Resources["Miasma"],2)],
    processing_time = 16,
    active = False
    )

Recipe(
    facility = Facilities['Miasma Collector (Rate Limited - Crafty)'],
    output = Resources["Miasma Vial"],
    output_amount = 2,
    inputs = [(Resources["Small Vial"],2),
              (Resources["Miasma"],2)],
    processing_time = Fraction(16*3,2),
    active = True
    )

Recipe(
    facility = Facilities['Miasma Collector (Rate Limited - Handy)'],
    output = Resources["Miasma Vial"],
    output_amount = 2,
    inputs = [(Resources["Small Vial"],2),
              (Resources["Miasma"],2)],
    processing_time = Fraction(16*5,2),
    active = False
    )

Recipe(
    facility = Facilities['Loom'],
    output = Resources["Rope"],
    output_amount = 1,
    inputs = [(Resources["Tree Bark"],1),
              (Resources["Leaves"],2)],
    processing_time = 16
    )

Recipe(
    facility = Facilities['Loom'],
    output = Resources["Fabric"],
    output_amount = 1,
    inputs = [(Resources["Tree Bark"],4),
              (Resources["Rope"],2)],
    processing_time = 8
    )

Recipe(
     facility = Facilities['Furnace'],
     output = Resources["Coal"],
     output_amount = 1,
     inputs = [(Resources["Wooden Log"],3 + Fraction(1,3))],
     processing_time = 8,
     include = False
     )#Wood burns every 8s, coal every 32

Recipe(
    facility = Facilities['Furnace'],
    output = Resources["Coal"],
    output_amount = Fraction(11,12),
    inputs = [(Resources["Wooden Log"],3)],
    processing_time = 8
    )

Recipe(
    facility = Facilities['Furnace'],
    output = Resources["Small Vial"],
    output_amount = 2,
    inputs = [(Resources["Quartz"],4),
              (Resources["Wooden Log"],Fraction(4,3))],
    processing_time = 32
    )

Recipe(
    facility = Facilities['Furnace'],
    output = Resources["Big Vial"],
    output_amount = 2,
    inputs = [(Resources["Quartz"],10),
              (Resources["Coal"],Fraction(19*128,3*10*60))],
    processing_time = 128
    )

Recipe(
    facility = Facilities['Furnace'],
    output = Resources["Quartz"],
    output_amount = 1,
    inputs = [(Resources["Limestone"],3),
              (Resources["Coal"],Fraction(19*8,3*10*60))],
    processing_time = 8,
    active = False
    )

Recipe(
    facility = Facilities['Aetheric Distiller'],
    output = Resources["Aetheric Shard (Pellet)"],
    output_amount = 6,
    inputs = [(Resources["Aetheric Pellet"],1)],
    processing_time = 48
    )

Recipe(
    facility = Facilities['Aetheric Distiller'],
    output = Resources["Aetheric Shard (Raw Aether)"],
    output_amount = 4,
    inputs = [(Resources["Raw Aether"],1)],
    processing_time = 48
    )

Recipe(
    facility = Facilities['Aetheric Distiller'],
    output = Resources["Aetheric Shard (Refined Aether)"],
    output_amount = 30,
    inputs = [(Resources["Refined Aether"],1)],
    processing_time = 128
    )

Recipe(
    facility = Facilities['Alchemy Lab'],
    output = Resources["Raw Aether"],
    output_amount = 1,
    inputs = [(Resources["Miasma Vial"],2),
              (Resources["Aetheric Shard"],1)],
    processing_time = 48
    )

Recipe(
    facility = Facilities['Alchemy Lab'],
    output = Resources["Refined Aether"],
    output_amount = 1,
    inputs = [(Resources["Raw Aether"],4),
              (Resources["Big Vial"],1)],
    processing_time = 64
    )


Recipes.calcRatios()
Recipes.printDependencies()