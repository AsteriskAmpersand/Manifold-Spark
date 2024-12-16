# -*- coding: utf-8 -*-
"""
Created on Fri Dec 13 01:57:18 2024

@author: Asterisk
"""


"""
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
    #active = False
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
    processing_time = 8, 
    #active = False
    )

Recipe(
    facility = Facilities['Sawbench'],
    output = Resources["Leaves (Leaf Knot)"],
    output_amount = 10,
    inputs = [(Resources["Leaf Knot"],1)],
    processing_time = 16
    )

Recipe(
    facility = Facilities['Sawbench'],
    output = Resources["Stellar Ice"],
    output_amount = 3,
    inputs = [(Resources["Frozen Log"],1)],
    processing_time = 16
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
    facility = Facilities['Wood Workshop'],
    output = Resources["Fertiliser"],
    output_amount = 4,
    inputs = [(Resources["Fertiliser"],1),
              (Resources["Stellar Ice"],5)],
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
    #active = False
    )

Recipe(
    facility = Facilities['Stonecutter'],
    output = Resources["Stone"],
    output_amount = 2,
    inputs = [(Resources["Limestone"],4)],
    processing_time = 8,
    #active = False
    )

Recipe(
    facility = Facilities['Stonecutter'],
    output = Resources["Coral"],
    output_amount = 8,
    inputs = [(Resources["Fluted Coral"],1)],
    processing_time = 32,
    #active = False
    )

Recipe(
    facility = Facilities['Stonecutter'],
    output = Resources["Stellar Ice"],
    output_amount = 6,
    inputs = [(Resources["Frozen Stone"],2)],
    processing_time = 32
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
    facility = Facilities['Spark Workshop'],
    output = Resources["Drilly Spark"],
    output_amount = 3,
    inputs = [(Resources["Slashy Spark"],6),
              (Resources["Drill Bit"],3),
              (Resources["Aether Crystal"],3)],
    processing_time =64,
    temp = 5
    )

Recipe(
    facility = Facilities['Spark Workshop'],
    output = Resources["Handy Spark"],
    output_amount = 1,
    inputs = [(Resources["Crafty Spark"],5),
              (Resources["Copper Ingot"],4),
              (Resources["Aether Crystal"],1)],
    processing_time =64,
    temp = -5
    )

Recipe(
    facility = Facilities['Spark Workshop'],
    output = Resources["Burning Spark"],
    output_amount = 1,
    inputs = [(Resources["Lava Cap"],5),
              (Resources["Copper Ingot"],8),
              (Resources["Aether Crystal"],1)],
    processing_time =64,
    temp = 5
    )

Recipe(
    facility = Facilities['Spark Workshop'],
    output = Resources["Freezing Spark"],
    output_amount = 1,
    inputs = [(Resources["Stellar Ice"],10),
              (Resources["Copper Ingot"],8),
              (Resources["Aether Crystal"],1)],
    processing_time =64,
    temp = -5
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
    processing_time = 4 #Crafties
    )#Produces Miasma every 4 seconds

Recipe(
    facility = Facilities['Noxious Coral (2 x Stumpy)'],
    output = Resources["Miasma"],
    output_amount = 1,
    inputs = [],
    processing_time = 4 * 2 #Crafties
    )#Penalty to adjust for everything else producing faster

Recipe(
    facility = Facilities['Noxious Coral (2 x Crafty)'],
    output = Resources["Miasma"],
    output_amount = 1,
    inputs = [],
    processing_time = 4 * 2 #Crafties
    )#Penalty to adjust for everything else producing faster

Recipe(
    facility = Facilities['Noxious Coral (2 x Handy)'],
    output = Resources["Miasma"],
    output_amount = 1,
    inputs = [],
    processing_time = 4 * 2 #Crafties
    )#Penalty to adjust for everything else producing faster


Recipe(
    facility = Facilities['Miasma Collector'],
    output = Resources["Miasma Vial"],
    output_amount = 2,
    inputs = [(Resources["Small Vial"],2),
              (Resources["Miasma"],2)],
    processing_time = 16,
    active = True
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
    inputs = [(Resources["Wooden Log"],3)],
    processing_time = 8
    )

Recipe(
    facility = Facilities['Furnace'],
    output = Resources["Small Vial"],
    output_amount = 2,
    inputs = [(Resources["Quartz"],4)],
    processing_time = 32
    )

Recipe(
    facility = Facilities['Furnace'],
    output = Resources["Big Vial"],
    output_amount = 2,
    inputs = [(Resources["Quartz"],10)],
    processing_time = 128
    )

Recipe(
    facility = Facilities['Furnace'],
    output = Resources["Quartz"],
    output_amount = 1,
    inputs = [(Resources["Limestone"],3)],
    processing_time = 8,
    active = False
    )


Recipe(
    facility = Facilities['Furnace'],
    output = Resources["Drill Bit"],
    output_amount = 2,
    inputs = [(Resources["Copper Ingot"],2)],
    processing_time = 32,
    )

Recipe(
    facility = Facilities['Furnace'],
    output = Resources["Copper Ingot"],
    output_amount = 1,
    inputs = [(Resources["Copper Ore"],4)],
    processing_time = 64,
    )

Recipe(
    facility = Facilities['Furnace'],
    output = Resources["Copper Ingot"],
    output_amount = 1,
    inputs = [(Resources["Copper Seed"],3)],
    processing_time = 64,
    )

Recipe(
    facility = Facilities['Furnace'],
    output = Resources["Copper Ingot"],
    output_amount = 1,
    inputs = [(Resources["Copper Sap"],1)],
    processing_time = 24,
    active = False
    )

Recipe(
    facility = Facilities['Furnace'],
    output = Resources["Copper Seed"],
    output_amount = 8,
    inputs = [(Resources["Copper Sap"],1)],
    processing_time = 24,
    )

Recipe(
    facility = Facilities['Aetheric Distiller'],
    output = Resources["Aetheric Shard"],# (Pellet)
    output_amount = 6,
    inputs = [(Resources["Aetheric Pellet"],1)],
    processing_time = 48
    )

Recipe(
    facility = Facilities['Aetheric Distiller'],
    output = Resources["Aetheric Shard"],# (Raw Aether)
    output_amount = 4,
    inputs = [(Resources["Raw Aether"],1)],
    processing_time = 48
    )

Recipe(
    facility = Facilities['Aetheric Distiller'],
    output = Resources["Aetheric Shard"],# (Refined Aether)"],
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

Recipe(
    facility = Facilities['Alchemy Lab'],
    output = Resources["Aetheric Pellet"],
    output_amount = 2,
    inputs = [(Resources["Leaf Knot"],1),
              (Resources["Raw Aether"],1)],
    processing_time = 64
    )

Recipe(
    facility = Facilities['Alchemy Lab'],
    output = Resources["Aetheric Clump"],
    output_amount = 2,
    inputs = [(Resources["Leaf Knot"],1),
              (Resources["Refined Aether"],1)],
    processing_time = 64
    )

Recipe(
    facility = Facilities['Alchemy Lab'],
    output = Resources["Stellar Fertiliser"],
    output_amount = 2,
    inputs = [(Resources["Fertiliser"],4),
              (Resources["Stellar Leaves"],1)],
    processing_time = 64
    )

Recipe(
    facility = Facilities['Alchemy Lab'],
    output = Resources["Liquid Fertiliser"],
    output_amount = 4,
    inputs = [(Resources["Fireshroom Cluster"],2),
              (Resources["Stellar Leaves"],1)],
    processing_time = 64
    )

Recipe(
    facility = Facilities['Alchemy Lab'],
    output = Resources["Aether Crystal"],
    output_amount = 10,
    inputs = [(Resources["Aether Seed"],1),
              (Resources["Raw Aether"],1)],
    processing_time = 64
    )

Recipe(
    facility = Facilities['Geode Breaker'],
    output = [Resources["Volcanic Soil"], Resources["Coal"],Resources["Glowshroom"]],
    output_amount = (20,10,10),
    inputs = [(Resources["Bumpy Geode"],3)],
    processing_time = 24
    )

Recipe(
    facility = Facilities['Geode Breaker'],
    output = [Resources["Volcanic Soil"], Resources["Copper Ore"],Resources["Glowshroom"]],
    output_amount = (20,10,10),
    inputs = [(Resources["Shiny Geode"],3)],
    processing_time = 24
    )


Recipe(
    facility = Facilities['Geode Breaker'],
    output = [Resources["Volcanic Soil"], Resources["Copper Ore"],Resources["Coal"]],
    output_amount = (20,10,10),
    inputs = [(Resources["Cracked Geode"],3)],
    processing_time = 24
    )

Recipe(
    facility = Facilities['Geode Breaker'],
    output = [Resources["Volcanic Soil"], Resources["Coal"],
              Resources["Glowshroom"], Resources["Copper Ore"]],
    output_amount = (200,Fraction(100*2,3),Fraction(100*2,3),Fraction(100*2,3)),
    inputs = [(Resources["Geode Cluster"],3)],
    processing_time = 24
    )


Recipe(
    facility = Facilities['Plant Extractor'],
    output = [Resources["Limestone"],Resources["Coral"]],
    output_amount = (3,3),
    inputs = [(Resources["Coral Seed"],3)],
    processing_time = 64
    )

Recipe(
    facility = Facilities['Plant Extractor'],
    output = [Resources["Copper Ore"],Resources["Coal"]],
    output_amount = (1,1),
    inputs = [(Resources["Copper Seed"],2)],
    processing_time = 48,
    temp = 3
    )

Recipe(
    facility = Facilities['Plant Extractor'],
    output = [Resources["Glowshroom"],Resources["Lava Cap"]],
    output_amount = (5,5),
    inputs = [(Resources["Fireshroom Cluster"],2)],
    processing_time = 64
    )

Recipe(
    facility = Facilities['Plant Extractor'],
    output = [Resources["Stellar Seed"],Resources["Stellar Ice"]],
    output_amount = (3,5),
    inputs = [(Resources["Stellar Leaves"],2)],
    processing_time = 64
    )

Recipe(
    facility = Facilities['Plant Extractor'],
    output = [Resources["Aetheric Clump"],Resources["Aether Seed"]],
    output_amount = (6,20),
    inputs = [(Resources["Aether Flower"],1)],
    processing_time = 64,
    temp = 3
    )

Recipe(
    facility = Facilities['Plant Extractor'],
    output = [Resources["Aether Seed"],Resources["Aether Segment"]],
    output_amount = (40,20),
    inputs = [(Resources["Aether Apple"],1)],
    processing_time = 64,
    temp = 3
    )

Recipe(
    facility = Facilities['Plant Extractor'],
    output = [Resources["Stone"],Resources["Stellar Seed"]],
    output_amount = (2,1),
    inputs = [(Resources["Stellar Ice"],4)],
    processing_time = 64,
    temp = 3
    )

Recipe(
    facility = Facilities['Plant Extractor'],
    output = [Resources["Copper Sap"],Resources["Copper Seed"]],
    output_amount = (20,10),
    inputs = [(Resources["Copper Cutting"],1)],
    processing_time = 64,
    )

Recipe(
    facility = Facilities['Plant Extractor'],
    output = [Resources["Aether Seed"],Resources["Aether Crystal"]],
    output_amount = (30,3),
    inputs = [(Resources["Aether Segment"],1)],
    processing_time = 64,
    )

Recipe(
    facility = Facilities['Greenhouse'],
    output = Resources["Leaf Knot"],
    output_amount = 10,
    inputs = [(Resources["Leaves"],40),
              (Resources["Fertiliser"],20)],
    processing_time = 640,
    temp = 3
    )

Recipe(
    facility = Facilities['Greenhouse'],
    output = Resources["Coral Seed"],
    output_amount = 20,
    inputs = [(Resources["Coral"],20),
              (Resources["Fertiliser"],10)],
    processing_time = 320,
    temp = -3
    )

Recipe(
    facility = Facilities['Greenhouse'],
    output = Resources["Fluted Coral"],
    output_amount = 20,
    inputs = [(Resources["Coral Seed"],10),
              (Resources["Fertiliser"],20)],
    processing_time = 320,
    temp = -3
    )

Recipe(
    facility = Facilities['Greenhouse'],
    output = Resources["Copper Seed"],
    output_amount = 20,
    inputs = [(Resources["Copper Ore"],20),
              (Resources["Volcanic Soil"],20)],
    processing_time = 880,
    temp = 3
    )

Recipe(
    facility = Facilities['Greenhouse'],
    output = Resources["Aether Flower"],
    output_amount = 1,
    inputs = [(Resources["Aetheric Pellet"],20),
              (Resources["Fertiliser"],30)],
    processing_time = 320,
    temp = -3
    )

Recipe(
    facility = Facilities['Greenhouse'],
    output = Resources["Stellar Leaves"],
    output_amount = 20,
    inputs = [(Resources["Stellar Seed"],10),
              (Resources["Volcanic Soil"],20)],
    processing_time = 640,
    temp = -5
    )

Recipe(
    facility = Facilities['Greenhouse'],
    output = Resources["Fireshroom Cluster"],
    output_amount = 10,
    inputs = [(Resources["Glowshroom"],20),
              (Resources["Stellar Fertiliser"],10)],
    processing_time = 640,
    temp = 5
    )

Recipe(
    facility = Facilities['Arboretum'],
    output = Resources["Geode Cluster"],
    output_amount = 5,
    inputs = [(Resources["Lava Cap"],100),
              (Resources["Coral Seed"],400)],
    processing_time = 12800,
    temp = -3
    )

Recipe(
    facility = Facilities['Arboretum'],
    output = Resources["Copper Cutting"],
    output_amount = 5,
    inputs = [(Resources["Leaf Knot"],200),
              (Resources["Copper Seed"],500)],
    processing_time = 25600,
    temp = -5
    )

Recipe(
    facility = Facilities['Arboretum'],
    output = Resources["Aether Apple"],
    output_amount = 5,
    inputs = [(Resources["Liquid Fertiliser"],500),
              (Resources["Aether Seed"],500)],
    processing_time = 25600,
    temp = 0
    )
"""