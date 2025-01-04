# -*- coding: utf-8 -*-
"""
Created on Fri Dec 13 01:37:41 2024

@author: Asterisk
"""
from fractions import Fraction


TextRecipeList = []

class TextRecipe():
    def __init__(self,**kwargs):
        self.kwargs = kwargs
        TextRecipeList.append(self)

TextRecipe(
    facility = 'Logger',
    output = "Wooden Log",
    inputs = [],
    processing_time = 2
    )

TextRecipe(
    facility = 'Logger',
    output = "Tree Bark",
    inputs = [],
    processing_time = 2
    )

TextRecipe(
    facility = 'Logger',
    output = "Leaves",
    inputs = [],
    processing_time = 2
    )

#Full Ore Miner
TextRecipe(
    facility = 'Ore Miner',
    output = "Copper Ore",
    inputs = [],
    processing_time = 10,
    )

#Ore Miner production speed is given by 60/(level+1)

#Depleted Ore Miner
TextRecipe(
    facility = 'Ore Miner (Depleted)',
    output = "Copper Ore",
    inputs = [],
    processing_time = 60
    )

#Full Ore Miner
TextRecipe(
    facility = 'Overclocked Ore Miner',
    output = "Copper Ore",
    inputs = [],
    processing_time = 4,
    )

#Ore Miner production speed is given by 24/(level+1)

#Depleted Ore Miner
TextRecipe(
    facility = 'Overclocked Ore Miner (Depleted)',
    output = "Copper Ore",
    inputs = [],
    processing_time = 24
    )

TextRecipe(
    facility = 'Sawbench',
    output = "Timber",
    inputs = [("Wooden Log",2)],
    processing_time = 16
    )

TextRecipe(
    facility = 'Sawbench',
    output = "Wooden Panel",
    inputs = [("Timber",2)],
    processing_time = 8
    )

TextRecipe(
    facility = 'Sawbench',
    output = "Tree Bark",
    output_amount = 2,
    inputs = [("Wooden Log",1)],
    processing_time = 8
    )

TextRecipe(
    facility = 'Sawbench',
    output = "Leaves",
    output_amount = 10,
    inputs = [("Leaf Knot",1)],
    processing_time = 16
    )

TextRecipe(
    facility = 'Sawbench',
    output = "Stellar Ice",
    output_amount = 3,
    inputs = [("Frozen Log",1)],
    processing_time = 16
    )


TextRecipe(
    facility = 'Wood Workshop',
    output = "Wooden Blade",
    inputs = [("Timber",1),
              ("Wooden Panel",2)],
    processing_time = 48
    )

TextRecipe(
    facility = 'Wood Workshop',
    output = "Ladder",
    output_amount = 2,
    inputs = [("Wooden Log",4),
              ("Timber",10)],
    processing_time = 32
    )

TextRecipe(
    facility = 'Wood Workshop',
    output = "Explosives",
    output_amount = 1,
    inputs = [("Fertiliser",2),
              ("Limestone",4)],
    processing_time = 24
    )

TextRecipe(
    facility = 'Wood Workshop',
    output = "Fertiliser",
    output_amount = 4,
    inputs = [("Fertiliser",1),
              ("Stellar Ice",5)],
    processing_time = 24
    )

TextRecipe(
    facility = 'Stonecutter',
    output = "Pebbles",
    output_amount = 2,
    inputs = [("Stone",1)],
    processing_time = 32
    )

TextRecipe(
    facility = 'Stonecutter',
    output = "Stone Plate",
    output_amount = 1,
    inputs = [("Stone",2)],
    processing_time = 32
    )

TextRecipe(
    facility = 'Stonecutter',
    output = "Limestone",
    output_amount = 3,
    inputs = [("Coral",4)],
    processing_time = 16
    )

TextRecipe(
    facility = 'Stonecutter',
    output = "Stone",
    output_amount = 2,
    inputs = [("Limestone",4)],
    processing_time = 8
    )

TextRecipe(
    facility = 'Stonecutter',
    output = "Coral",
    output_amount = 8,
    inputs = [("Fluted Coral",1)],
    processing_time = 32
    )

TextRecipe(
    facility = 'Stonecutter',
    output = "Stellar Ice",
    output_amount = 6,
    inputs = [("Frozen Stone",2)],
    processing_time = 32
    )

TextRecipe(
    facility = 'Stone Workshop',
    output = "Dowsing Stone",
    output_amount = 3,
    inputs = [("Quartz",1),
              ("Rope",1)],
    processing_time = 24
    )

TextRecipe(
    facility = 'Stone Workshop',
    output = "Path Tile",
    output_amount = 5,
    inputs = [("Limestone",5),
              ("Pebbles",10)],
    processing_time = 32
    )

TextRecipe(
    facility = 'Stone Workshop',
    output = "Stone Wheel",
    output_amount = 2,
    inputs = [("Path Tile",4),
              ("Stone Plate",2)],
    processing_time = 16
    )

TextRecipe(
    facility = 'Stone Workshop',
    output = "Stone Spike",
    output_amount = 4,
    inputs = [("Stone Plate",4),
              ("Wooden Blade",1)],
    processing_time = 16
    )

TextRecipe(
    facility = 'Spark Workbench',
    output = "Stumpy Spark",
    inputs = [("Aetheric Shard",1),
              ("Wooden Log",5)],
    processing_time = 32
    )

TextRecipe(
    facility = 'Spark Workbench',
    output = "Arty Spark",
    inputs = [("Stumpy Spark",2),
              ("Rope",5)],
    processing_time = 32
    )

TextRecipe(
    facility = 'Spark Workbench',
    output = "Crafty Spark",
    inputs = [("Stumpy Spark",2),
              ("Wooden Panel",2)],
    processing_time = 48
    )

TextRecipe(
    facility = 'Spark Workbench',
    output = "Choppy Spark",
    inputs = [("Stumpy Spark",3),
              ("Wooden Blade",2)],
    processing_time = 64
    )

TextRecipe(
    facility = 'Spark Workbench',
    output = "Carry Spark",
    inputs = [("Crafty Spark",1),
              ("Timber",4)],
    processing_time = 32
    )

TextRecipe(
    facility = 'Spark Workbench',
    output = "Loamy Spark",
    output_amount = 5,
    inputs = [("Aetheric Shard",5),
              ("Fertiliser",3)],
    processing_time = 32
    )

TextRecipe(
    facility = 'Spark Workstation',
    output = "Rocky Spark",
    output_amount = 1,
    inputs = [("Stumpy Spark",2),
              ("Stone",5)],
    processing_time = 32
    )

TextRecipe(
    facility = 'Spark Workstation',
    output = "Scouty Spark",
    output_amount = 1,
    inputs = [("Stumpy Spark",1),
              ("Dowsing Stone",1)],
    processing_time = 32
    )

TextRecipe(
    facility = 'Spark Workstation',
    output = "Hauling Spark",
    output_amount = 1,
    inputs = [("Carry Spark",2),
              ("Stone Wheel",4)],
    processing_time = 64
    )

TextRecipe(
    facility = 'Spark Workstation',
    output = "Puffy Spark",
    output_amount = 1,
    inputs = [("Rocky Spark",1),
              ("Fabric",4)],
    processing_time = 32
    )

TextRecipe(
    facility = 'Spark Workstation',
    output = "Boomy Spark",
    output_amount = 1,
    inputs = [("Rocky Spark",3),
              ("Explosives",5)],
    processing_time = 48
    )

TextRecipe(
    facility = 'Spark Workstation',
    output = "Crashy Spark",
    output_amount = 1,
    inputs = [("Boomy Spark",2),
              ("Stone Spike",7)],
    processing_time = 64
    )

TextRecipe(
    facility = 'Spark Workstation',
    output = "Slashy Spark",
    output_amount = 1,
    inputs = [("Rocky Spark",2),
              ("Choppy Spark",3)],
    processing_time =64
    )

TextRecipe(
    facility = 'Spark Workshop',
    output = "Drilly Spark",
    output_amount = 3,
    inputs = [("Slashy Spark",6),
              ("Drill Bit",3),
              ("Aether Crystal",3)],
    processing_time =64,
    temp = 5
    )

TextRecipe(
    facility = 'Spark Workshop',
    output = "Handy Spark",
    output_amount = 1,
    inputs = [("Crafty Spark",5),
              ("Copper Ingot",4),
              ("Aether Crystal",1)],
    processing_time =64,
    temp = -5
    )

TextRecipe(
    facility = 'Spark Workshop',
    output = "Burning Spark",
    output_amount = 1,
    inputs = [("Lava Cap",5),
              ("Copper Ingot",8),
              ("Aether Crystal",1)],
    processing_time =64,
    temp = 5
    )

TextRecipe(
    facility = 'Spark Workshop',
    output = "Freezing Spark",
    output_amount = 1,
    inputs = [("Stellar Ice",10),
              ("Copper Ingot",8),
              ("Aether Crystal",1)],
    processing_time =64,
    temp = -5
    )

TextRecipe(
    facility = 'Cutter',
    output = "Fertiliser",
    output_amount = 2,
    inputs = [("Leaves",4)],
    processing_time = 24
    )

TextRecipe(
    facility = 'Cutter',
    output = "Aetheric Pellet",
    output_amount = 6,
    inputs = [("Aetheric Clump",1)],
    processing_time = 128
    )

TextRecipe(
    facility = 'Drill',
    output = "Stone",
    output_amount = 1,
    inputs = [],
    processing_time = 2
    )

TextRecipe(
    facility = 'Drill',
    output = "Quartz",
    output_amount = 1,
    inputs = [],
    processing_time = 2
    )

TextRecipe(
    facility = 'Drill',
    output = "Limestone",
    output_amount = 1,
    inputs = [],
    processing_time = 2
    )

TextRecipe(
    facility = 'Noxious Coral',
    output = "Miasma",
    output_amount = 1,
    inputs = [],
    processing_time = 4 #Stumpy
    )#Produces Miasma every 4 seconds

TextRecipe(
    facility = 'Noxious Coral (2 x Stumpy)',
    output = "Miasma",
    output_amount = 1,
    inputs = [],
    processing_time = 4 * 2 #Stumpy
    )#Penalty to adjust for everything else producing faster

TextRecipe(
    facility = 'Noxious Coral (2 x Crafty)',
    output = "Miasma",
    output_amount = 1,
    inputs = [],
    processing_time = 4 * 3 #Crafties
    )#Penalty to adjust for everything else producing faster

TextRecipe(
    facility = 'Noxious Coral (2 x Handy)',
    output = "Miasma",
    output_amount = 1,
    inputs = [],
    processing_time = 4 * 5 #Handy
    )#Penalty to adjust for everything else producing faster


TextRecipe(
    facility = 'Miasma Collector',
    output = "Miasma Vial",
    output_amount = 2,
    inputs = [("Small Vial",2),
              ("Miasma",2)],
    processing_time = 16
    )

TextRecipe(
    facility = 'Loom',
    output = "Rope",
    output_amount = 1,
    inputs = [("Tree Bark",1),
              ("Leaves",2)],
    processing_time = 16
    )

TextRecipe(
    facility = 'Loom',
    output = "Fabric",
    output_amount = 1,
    inputs = [("Tree Bark",4),
              ("Rope",2)],
    processing_time = 8
    )


TextRecipe(
    facility = 'Furnace',
    output = "Coal",
    output_amount = 1,
    inputs = [("Wooden Log",3)],
    processing_time = 8
    )

TextRecipe(
    facility = 'Furnace',
    output = "Small Vial",
    output_amount = 2,
    inputs = [("Quartz",4)],
    processing_time = 32
    )

TextRecipe(
    facility = 'Furnace',
    output = "Big Vial",
    output_amount = 2,
    inputs = [("Quartz",10)],
    processing_time = 128
    )

TextRecipe(
    facility = 'Furnace',
    output = "Quartz",
    output_amount = 1,
    inputs = [("Limestone",3)],
    processing_time = 8
    )


TextRecipe(
    facility = 'Furnace',
    output = "Drill Bit",
    output_amount = 2,
    inputs = [("Copper Ingot",2)],
    processing_time = 32,
    )

TextRecipe(
    facility = 'Furnace',
    output = "Copper Ingot",
    output_amount = 1,
    inputs = [("Copper Ore",4)],
    processing_time = 64,
    )

TextRecipe(
    facility = 'Furnace',
    output = "Copper Ingot",
    output_amount = 1,
    inputs = [("Copper Seed",3)],
    processing_time = 64,
    )

TextRecipe(
    facility = 'Furnace',
    output = "Copper Ingot",
    output_amount = 1,
    inputs = [("Copper Sap",1)],
    processing_time = 24
    )

TextRecipe(
    facility = 'Furnace',
    output = "Copper Seed",
    output_amount = 8,
    inputs = [("Copper Sap",1)],
    processing_time = 24,
    )

TextRecipe(
    facility = 'Aetheric Distiller',
    output = "Aetheric Shard",# (Pellet)
    output_amount = 6,
    inputs = [("Aetheric Pellet",1)],
    processing_time = 48
    )

TextRecipe(
    facility = 'Aetheric Distiller',
    output = "Aetheric Shard",# (Raw Aether)
    output_amount = 4,
    inputs = [("Raw Aether",1)],
    processing_time = 48
    )

TextRecipe(
    facility = 'Aetheric Distiller',
    output = "Aetheric Shard",# (Refined Aether)"],
    output_amount = 30,
    inputs = [("Refined Aether",1)],
    processing_time = 128
    )

TextRecipe(
    facility = 'Alchemy Lab',
    output = "Raw Aether",
    output_amount = 1,
    inputs = [("Miasma Vial",2),
              ("Aetheric Shard",1)],
    processing_time = 48
    )

TextRecipe(
    facility = 'Alchemy Lab',
    output = "Refined Aether",
    output_amount = 1,
    inputs = [("Raw Aether",4),
              ("Big Vial",1)],
    processing_time = 64
    )

TextRecipe(
    facility = 'Alchemy Lab',
    output = "Aetheric Pellet",
    output_amount = 2,
    inputs = [("Leaf Knot",1),
              ("Raw Aether",1)],
    processing_time = 64
    )

TextRecipe(
    facility = 'Alchemy Lab',
    output = "Aetheric Clump",
    output_amount = 2,
    inputs = [("Leaf Knot",1),
              ("Refined Aether",1)],
    processing_time = 64
    )

TextRecipe(
    facility = 'Alchemy Lab',
    output = "Stellar Fertiliser",
    output_amount = 2,
    inputs = [("Fertiliser",4),
              ("Stellar Leaves",1)],
    processing_time = 64
    )

TextRecipe(
    facility = 'Alchemy Lab',
    output = "Liquid Fertiliser",
    output_amount = 4,
    inputs = [("Fireshroom Cluster",2),
              ("Stellar Leaves",1)],
    processing_time = 64
    )

TextRecipe(
    facility = 'Alchemy Lab',
    output = "Aether Crystal",
    output_amount = 10,
    inputs = [("Aether Seed",1),
              ("Raw Aether",1)],
    processing_time = 64
    )

TextRecipe(
    facility = 'Geode Breaker',
    output = ["Volcanic Soil", "Coal","Glowshroom"],
    output_amount = (20,10,10),
    inputs = [("Bumpy Geode",3)],
    processing_time = 24*3
    )

TextRecipe(
    facility = 'Geode Breaker',
    output = ["Volcanic Soil", "Copper Ore","Glowshroom"],
    output_amount = (20,10,10),
    inputs = [("Shiny Geode",3)],
    processing_time = 24*3
    )


TextRecipe(
    facility = 'Geode Breaker',
    output = ["Volcanic Soil", "Copper Ore","Coal"],
    output_amount = (20,10,10),
    inputs = [("Cracked Geode",3)],
    processing_time = 24*3
    )

TextRecipe(
    facility = 'Geode Breaker',
    output = ["Volcanic Soil", "Coal",
              "Glowshroom", "Copper Ore"],
    output_amount = (200,Fraction(100*2,3),Fraction(100*2,3),Fraction(100*2,3)),
    inputs = [("Geode Cluster",3)],
    processing_time = 24*3*10
    )


TextRecipe(
    facility = 'Plant Extractor',
    output = ["Limestone","Coral"],
    output_amount = (3,3),
    inputs = [("Coral Seed",1)],
    processing_time = 64
    )

TextRecipe(
    facility = 'Plant Extractor',
    output = ["Copper Ore","Coal"],
    output_amount = (1,1),
    inputs = [("Copper Seed",2)],
    processing_time = 48,
    temp = 3
    )

TextRecipe(
    facility = 'Plant Extractor',
    output = ["Glowshroom","Lava Cap"],
    output_amount = (5,5),
    inputs = [("Fireshroom Cluster",2)],
    processing_time = 64
    )

TextRecipe(
    facility = 'Plant Extractor',
    output = ["Stellar Seed","Stellar Ice"],
    output_amount = (3,5),
    inputs = [("Stellar Leaves",2)],
    processing_time = 64
    )

TextRecipe(
    facility = 'Plant Extractor',
    output = ["Aetheric Clump","Aether Seed"],
    output_amount = (6,20),
    inputs = [("Aether Flower",1)],
    processing_time = 64,
    temp = 3
    )

TextRecipe(
    facility = 'Plant Extractor',
    output = ["Aether Seed","Aether Segment"],
    output_amount = (40,20),
    inputs = [("Aether Apple",1)],
    processing_time = 64,
    temp = 3
    )

TextRecipe(
    facility = 'Plant Extractor',
    output = ["Stone","Stellar Seed"],
    output_amount = (2,1),
    inputs = [("Stellar Ice",4)],
    processing_time = 64,
    temp = 3
    )

TextRecipe(
    facility = 'Plant Extractor',
    output = ["Copper Sap","Copper Seed"],
    output_amount = (20,10),
    inputs = [("Copper Cutting",1)],
    processing_time = 64,
    )

TextRecipe(
    facility = 'Plant Extractor',
    output = ["Aether Seed","Aether Crystal"],
    output_amount = (30,3),
    inputs = [("Aether Segment",1)],
    processing_time = 64,
    )

TextRecipe(
    facility = 'Greenhouse',
    output = "Leaf Knot",
    output_amount = 10,
    inputs = [("Leaves",40),
              ("Fertiliser",20)],
    processing_time = 640,
    temp = 3
    )

TextRecipe(
    facility = 'Greenhouse',
    output = "Coral Seed",
    output_amount = 20,
    inputs = [("Coral",20),
              ("Fertiliser",10)],
    processing_time = 320,
    temp = -3
    )

TextRecipe(
    facility = 'Greenhouse',
    output = "Fluted Coral",
    output_amount = 20,
    inputs = [("Coral Seed",10),
              ("Fertiliser",20)],
    processing_time = 320,
    temp = -3
    )

TextRecipe(
    facility = 'Greenhouse',
    output = "Copper Seed",
    output_amount = 20,
    inputs = [("Copper Ore",20),
              ("Volcanic Soil",20)],
    processing_time = 880,
    temp = 3
    )

TextRecipe(
    facility = 'Greenhouse',
    output = "Aether Flower",
    output_amount = 1,
    inputs = [("Aetheric Pellet",20),
              ("Fertiliser",30)],
    processing_time = 320,
    temp = -3
    )

TextRecipe(
    facility = 'Greenhouse',
    output = "Stellar Leaves",
    output_amount = 20,
    inputs = [("Stellar Seed",10),
              ("Volcanic Soil",20)],
    processing_time = 640,
    temp = -5
    )

TextRecipe(
    facility = 'Greenhouse',
    output = "Fireshroom Cluster",
    output_amount = 10,
    inputs = [("Glowshroom",20),
              ("Stellar Fertiliser",10)],
    processing_time = 640,
    temp = 5
    )

TextRecipe(
    facility = 'Arboretum Feeder',
    output = "Geode Cluster",
    output_amount = 5,
    inputs = [("Lava Cap",100),
              ("Coral Seed",400)],
    processing_time = 12800,
    temp = -3
    )

TextRecipe(
    facility = 'Arboretum Feeder',
    output = "Copper Cutting",
    output_amount = 5,
    inputs = [("Leaf Knot",200),
              ("Copper Seed",500)],
    processing_time = 25600,
    temp = -5
    )

TextRecipe(
    facility = 'Arboretum Feeder',
    output = "Aether Apple",
    output_amount = 5,
    inputs = [("Liquid Fertiliser",500),
              ("Aether Seed",500)],
    processing_time = 25600,
    temp = 0
    )