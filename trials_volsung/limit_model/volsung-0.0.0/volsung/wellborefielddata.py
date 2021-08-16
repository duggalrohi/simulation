#!/usr/bin/python3

"""

wellborefielddata.py

simple data table structure to read wellbore field data from XML

"""

import h5py
import vtk
import numpy
import matplotlib
import math

from volsung.vectorfielddata import *

class WellboreFieldData(VectorFieldData):
    """
    WellboreFieldData object
    """
    
    def __init__(self):
        super().__init__()
        self._arrdict["pressure"] = "Pressure"
        self._arrdict["elevation"] = "z"
        self._arrdict["temperature"] = "Temperature"
        self._arrdict["elevation"] = "z"
        self._arrdict["gasmassfraction"] = "Gas Mass Fraction"
        self._arrdict["velocity"] = "Velocity"
        self._arrdict["velocityliquid"] = "Velocity (liquid)"
        self._arrdict["velocitygas"] = "Velocity (gas)"
