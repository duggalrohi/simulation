#!/usr/bin/python3

"""

vectorfielddata.py

simple abstract data table structure to read timed vector field data from xml

"""

import h5py
import vtk
import numpy
import matplotlib
import math

class VectorFieldData(object):
    """
    Reservoir1DFieldData object
    """
    
    def __init__(self):
        self.data = {}
        # note: subclasses must define the following dictionary
        #       which contains xml tags key, array name as value
        #       all of them must contain the Time array name
        self._arrdict = {"time" : "Time"}
        self._hasMassFractions = False
        
    def __vecarr(self, node):
        s = int(node.attrib["size"])
        if s <= 0:
            return numpy.array([], dtype = numpy.float32)
        l = [float('nan')] * s
        for n in node:
            if n.tag == 'v':
                index = int(n.attrib["index"])
                l[index] = float(n.text)
        return numpy.array(l, dtype = numpy.float32)
        
    def _readXML(self, xmlnode):
        """
        Reads the data within xmlnode
        Raw data is in csv form.
        """
        self.data.clear()
        for k in self._arrdict.keys():
            self.data[self._arrdict[k]] = self.__vecarr(xmlnode.find(k))
        # optional: read mass fractions
        if self._hasMassFractions:
            for n in xmlnode.find("massfraction"):
                self.data[n.tag.upper()] = self.__vecarr(n)
        
    def __closestTime(self, time):
        tc = float('nan')
        diff = 1e+308
        for t in self.data["Time"]:
            d = abs(t - time)
            if math.isnan(d): continue
            if d < diff:
                tc = t
                diff = d
        return tc
        
    def timeSlice(self, time = float('nan')):
        """
        Return a time slice through the data.
        If time is nan then all data is returned.
        Else only data which belongs to the closest time found is returned.
        """
        if math.isnan(time):
            return self.data
        index = numpy.where(self.data["Time"] == self.__closestTime(time))
        data = {}
        for k in self.data.keys():
            data[k] = self.data[k][index]
        return data
