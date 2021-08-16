#!/usr/bin/python3

"""

sources.py

library to read in volsung sources/sink data from Sigurd output files

"""

import h5py
import vtk
import numpy
import matplotlib

from volsung.sigurd import *

class SourceSinkData(object):
    def __init__(self, tableId):
        self.tableId = tableId
        self.data = []
        
    def _readStaticData(self, hdffile):
        """
        Read static data from zone0.
        """
        node = hdffile["/zones/zone0/reservoir/SourcesSinks"]
        self.elementId = node["Element Id"][self.tableId]
        self.name = (node["Name"][self.tableId]).decode("utf-8")
        self.parentName = node["Parent Name"][self.tableId]
    
        
    def _readZoneData(self, hdffile, zoneId):
        """
        Read data from hdf table for given zoneId
        Data is stored sequentially, i.e. this method needs to be called sequentially with correct zoneId
        """
        node = hdffile["/zones/zone%d/reservoir/SourcesSinks" % zoneId]
        zone_dict = {}
        for n in node:
            if n in ["Element Id", "Name", "Parent Name"]: continue
            zone_dict[n] = node[n][self.tableId]
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

class Sources(Sigurd):
    """
    Sources/Sinks object    
    """
    def __init__(self, hdffile):
        """
        Creates the Sources/Sinks using the hdffile provided
        """
        super().__init__(hdffile)
        self.__createSources()
        self.__readSourceData()

    def __createSources(self):
        """
        Create all sources from zone0
        """
        self.sourceData = []
        nsources = self.hdfFile["/zones/zone0/reservoir/SourcesSinks/Name"][:].size
        for i in range(nsources):
            self.sourceData.append(SourceSinkData(i))
            
    def __readSourceData(self):
        """
        Calls on all sourceData to read their data from the hdf file
        """
        # first read the static data from zone0
        for obj in self.sourceData:
            obj._readStaticData(self.hdfFile)
        # then read the zone data
        for i in range(self.numberOfZones()):
            for obj in self.sourceData:
                obj._readZoneData(self.hdfFile, i)
                
    def names(self):
        """
        Returns a list with source data names.
        """
        l = []
        for obj in self.sourceData:
            l.append(obj.name)
        return l
    
    def data(self, name):
        """
        Returns the source data for the given name.
        """
        for obj in self.sourceData:
            if obj.name == name:
                return obj
        return None
    
