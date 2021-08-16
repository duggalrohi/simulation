#!/usr/bin/python3

"""

volsung.py

library to read in Volsung models consisting of a set of 

a) a Sigurd output file (hdf5)
b) a Brynhild input file (xml) [optional]

The model class can be used to create special tasks which need the interaction of the input/output data.

If you don't specify a Brynhild input file then the xml file will be loaded from the xml data stored in the Results.sigurd file instead.

"""

from volsung.brynhild import *
from volsung.sigurd import *
from volsung.reservoir import *
from volsung.flownetwork import *
from volsung.sources import *

class VolsungModel(object):
    """
    Volsung model class
    """
    
    def __init__(self, results_fname = "Results.sigurd", brynhild_fname = ""):
        self.hdfFile = h5py.File(results_fname, "r")
        self.reservoir = Reservoir(self.hdfFile)
        self.sources = Sources(self.hdfFile)
        self.flowNetwork = FlowNetwork(self.hdfFile)
        if brynhild_fname != "":
            self.brynhild = Brynhild(brynhild_fname)
        else:
            self.brynhild = Brynhild()
            self.brynhild._setXMLText(self.reservoir.xmlInputText())
            
        # let the objects in the flow network read additional data from brynhild
        for obj in self.flowNetwork.portObjects:
            obj._readXML(self.brynhild.flowNetworkObjectNode(obj.objectId))
            
