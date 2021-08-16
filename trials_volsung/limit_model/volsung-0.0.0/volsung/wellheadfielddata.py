#!/usr/bin/python3

"""

wellheadfielddata.py

simple data table structure to read wellhead field data from XML

"""

import h5py
import vtk
import numpy
import matplotlib
import math

from volsung.vectorfielddata import *

class WellheadFieldData(VectorFieldData):
    """
    WellheadFieldData object
    """
    
    def __init__(self):
        super().__init__()
        self._arrdict["pressure"] = "Pressure"
        self._arrdict["massrate"] = "Mass Rate"
        self._arrdict["enthalpy"] = "Enthalpy"
        self._hasMassFractions = True
