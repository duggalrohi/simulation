#!/usr/bin/python3

"""

reservoir1dfielddata.py

simple data table structure to read 1D reservoir field data from XML

"""

import h5py
import vtk
import numpy
import matplotlib
import math

from volsung.vectorfielddata import *

class Reservoir1DFieldData(VectorFieldData):
    """
    Reservoir1DFieldData object
    """
    
    def __init__(self):
        super().__init__()
        self._arrdict["pressure"] = "Pressure"
        self._arrdict["temperature"] = "Temperature"
        self._arrdict["z"] = "z"
        
    def _readXML(self, xmlnode):
        """
        Reads the data within xmlnode
        Raw data is in csv form.
        """
        super()._readXML(xmlnode)
        # sort everything by z-coordinate
        index = numpy.argsort(self.data["z"])
        for k in self.data.keys():
            self.data[k] = self.data[k][index]
