#!/usr/bin/python3

"""

datatable.py

simple data table structure

"""

import h5py
import vtk
import numpy
import matplotlib

class DataTable(object):
    """
    Class describing a simple data table for zone data
    """
    def __init__(self):
        """
        Constructor
        """
        self.data = []
        
    def _readHDFTableData(self, hdffile, zoneId, zonepath = "/zones/zone%d/flownetwork/Ports", ignore = []):
        """
        Read data from hdf table for given zoneId
        Data is stored sequentially, i.e. this method needs to be called sequentially with correct zoneId
        Note the zonepath acts as a template.
        """
        node = hdffile[zonepath % zoneId]
        zone_dict = {}
        for n in node:
            if n in ignore: continue
            zone_dict[n] = node[n][:]
        self.data.append(zone_dict)
        
    def history(self, arrname):
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