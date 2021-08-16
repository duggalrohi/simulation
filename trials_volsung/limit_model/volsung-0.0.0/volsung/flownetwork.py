#!/usr/bin/python3

"""

flownetwork.py

library to read in volsung flownetwork data from Sigurd output files

"""

import h5py
import vtk
import numpy
import matplotlib

from volsung.sigurd import *
from volsung.flownetworkportobject import *
from volsung.reginwell import *

class FlowNetwork(Sigurd):
    """
    FlowNetwork object    
    """
    def __init__(self, hdffile):
        """
        Creates the FlowNetwork using the hdffile provided
        """
        super().__init__(hdffile)
        self.__createObjects()
        self.__readObjectData()
        
    def __createObjects(self):
        """
        Create all objects from zone0
        """
        self.portObjects = []
        try:
            for o in self.hdfFile["/zones/zone0/flownetwork/objects"]:
                node = self.hdfFile["/zones/zone0/flownetwork/objects/" + o]
                # get the class name
                try:
                    class_name = node.attrs["class"].decode("utf-8")
                except KeyError:
                    class_name = ""         # use generic port object
                # generate specific class
                if class_name == "":
                    obj = FlowNetworkPortObject(o)
                elif class_name == "FNPO_ReginProducer":
                    obj = ReginWell(o)
                else:
                    # todo once we created more differentiated subclasses
                    obj = FlowNetworkPortObject(o)
                self.portObjects.append(obj)
        except KeyError:
            # no flownetwork here, may be a T2Fafnir mode file
            pass
            
    def __readObjectData(self):
        """
        Calls on all portObjects to read their data from the hdf file
        """
        if (len(self.portObjects) == 0):
            return
        # first read the static data from zone0
        for obj in self.portObjects:
            obj._readStaticData(self.hdfFile)
        # then read the zone data
        for i in range(self.numberOfZones()):
            # create a copy in memory of the port table; it is much faster to load from there
            porttable = {}
            for n in self.hdfFile["/zones/zone%d/flownetwork/Ports" % i]:
                porttable[n] = self.hdfFile["/zones/zone%d/flownetwork/Ports/%s" % (i, n)][:]
            for obj in self.portObjects:
                obj._readZoneData(self.hdfFile, i, porttable)

    def portObject(self, name):
        """
        Returns the port object for the given name.
        """
        for obj in self.portObjects:
            if obj.name == name: return obj
        return None
    
    def portObjectNames(self):
        """
        Returns the names of the port objects.
        """
        l = []
        for obj in self.portObjects:
            l.append(obj.name)
        return l
    
    def plotWellTracks(self, fig, ax, zoneId = 0, linewidth = 5, color = '#000000', fontsize = 0, labeloffset = (0,0)):
        """
        Plot all available welltracks onto ax
        """
        for obj in self.portObjects:
            obj.plotWellTrack(fig, ax, zoneId = zoneId, linewidth = linewidth, color = color, fontsize = fontsize, labeloffset = labeloffset)
