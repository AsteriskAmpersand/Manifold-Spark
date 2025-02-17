# -*- coding: utf-8 -*-
"""
Created on Fri Dec 13 02:17:17 2024

@author: Asterisk
"""
from fractions import Fraction
import os
import sys

def to_str(v):
    if type(v) is Fraction:
        if v.denominator == 1:
            return str(v.numerator)
        return "%d/%d"%(v.numerator,v.denominator)
    return str(v)

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, os.path.join(".", relative_path))
    return os.path.join(".", relative_path)