#!/usr/bin/python3

"""

flownetworkport.py

library to define flow network port classes

"""

import h5py
import vtk
import numpy
import matplotlib

from volsung.flowratetable import *

class FlowNetworkPort(object):
    """
    Class describing a port.
    """
    def __init__(self, portId, tableId):
        """
        Creates a new port.
        portId is the input/output port id within an object.
        tableId is the index in the hdf table from which to read data.
        """
        self.portId = portId
        self.tableId = tableId
        self.data = []
        self.historyFlowRate = FlowRateTable()
        
    def _readHDFTableData(self, hdffile, zoneId, porttable = None):
        """
        Read data from hdf table for given zoneId
        Data is stored sequentially, i.e. this method needs to be called sequentially with correct zoneId
        For efficiency purposes the port table for the zone can be passed in as a dictionary
        """
        node = hdffile["/zones/zone%d/flownetwork/Ports" % zoneId]
        zone_dict = {}
        it = node
        if porttable is not None:
            it = porttable.keys()
        for n in it:
            if n in ["Port Id", "Port Object Id", "Port Object Name", "Port Type"]: continue
            if porttable is not None:
                zone_dict[n] = porttable[n][self.tableId]
            else:
                zone_dict[n] = node[n][self.tableId]
        self.data.append(zone_dict)
        
    def _readXML(self, node):
        """
        Read in additional data from xml input node pointing into this object
        """
        self.historyFlowRate._readXML(node.find("fielddata").find("flowratetable"))

    def zoneHistory(self, arrname):
        """
        Returns the ordered zone data for the quantity given in arrname
        """
        d = []
        for s in self.data:
            try:
                d.append(s[arrname])
            except KeyError:
                d.append(float('nan'))
        return numpy.array(d)
    
    def fieldHistory(self, arrname):
        """
        Returns the field history data for arrname
        """
        return self.historyFlowRate.data[arrname]


class OutputPort(FlowNetworkPort):
    """
    Class describing an output port.
    """
    def __init__(self, portId, tableId):
        super().__init__(portId, tableId)
        
class InputPort(FlowNetworkPort):
    """
    Class describing an input port.
    """
    def __init__(self, portId, tableId):
        super().__init__(portId, tableId)
