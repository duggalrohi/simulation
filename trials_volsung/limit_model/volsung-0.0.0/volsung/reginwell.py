#!/usr/bin/python3

"""

reginwell.py

library to define regin well port object

"""

import h5py
import vtk
import numpy
import matplotlib

from volsung.flownetworkportobject import *
from volsung.datatable import *
from volsung.wellheadfielddata import *
from volsung.wellborefielddata import *

class ReginWell(FlowNetworkPortObject):
    """
    Class describing a port.
    """
    def __init__(self, name):
        super().__init__(name)
        # simulation data
        self.__wellheaddata = DataTable()
        self.__wellboredata = DataTable()
        self.__feedzonedata = DataTable()
        # field data
        self.wellheadFieldData = WellheadFieldData()
        self.wellboreFieldData = WellboreFieldData()
        
    def _readStaticData(self, hdffile):
        super()._readStaticData(hdffile)
        
    def _readZoneData(self, hdffile, zoneId, porttable = None):
        super()._readZoneData(hdffile, zoneId, porttable)
        zonepath = "/zones/zone%d/flownetwork/objects/" + self.name + "/wellboremodel"
        self.__wellheaddata._readHDFTableData(hdffile, zoneId, zonepath + "/wellheadprofile")
        self.__wellboredata._readHDFTableData(hdffile, zoneId, zonepath + "/wellboreprofile")
        self.__feedzonedata._readHDFTableData(hdffile, zoneId, zonepath + "/feedzonecollection")
        
    def _readXML(self, node):
        """
        Read in additional data from xml input node pointing into this object
        """
        super()._readXML(node)
        self.wellheadFieldData._readXML(node.find("wellboremodel").find("wellheadprofile").find("wellheadprofilefielddata"))
        self.wellboreFieldData._readXML(node.find("wellboremodel").find("wellboreprofile").find("wellboreprofilefielddata"))
    
    def wellheadData(self, zoneId, arrname):
        """
        Returns the wellhead data for the zoneId and array name.
        """
        return self.__wellheaddata.data[zoneId][arrname]
    
    def wellboreData(self, zoneId, arrname):
        """
        Returns the wellbore data for the zoneId and array name.
        """
        return self.__wellboredata.data[zoneId][arrname]
    
    def feedzoneData(self, zoneId, arrname):
        """
        Returns the feedzone data for the zoneId and array name.
        """
        return self.__feedzonedata.data[zoneId][arrname]
    
    
