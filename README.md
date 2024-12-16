<p align="center">
  <img src="https://github.com/AsteriskAmpersand/Manifold-Spark/blob/main/ManifoldSpark.png" alt="Manifold Spark"/>
</p>

# Manifold Spark - Oddsparks Supply Chain Optimizer
This utility allows customizing supply lines and automatically optimizes the ratios involved. As of the latest update, Hot and Cold, supply chains now have cycles and variants as well as the potential for self-feeding. This program allows constructing, saving and loading custom production chains and automatically identifying the optimal ratios. Additionally users can define cyclical chains that assume self feeding (up to a degree).

# Requirements
Python 3.2+, wingui32, win32con, dearpygui

# Usage
At the moment there's no precompiled executable so running the source through a local python install is the most direct way of getting it working. 

Select a base chain and you can edit non-final machines by right clickign and performing substitutions. You can save chains and load. If a chain's raw inputs (Manual Collection per Second) and un-taken outputs are the same then, when saved as a user recipe it also can be used in cyclic mode.
