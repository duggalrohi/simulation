#!/usr/bin/python3

"""

sigurd.py

base class library to read in sigurd data from hdf5 files

"""

import h5py
import vtk
import numpy
import matplotlib
import datetime

class Sigurd(object):
    """
    Sigurd file object
    """
    def __init__(self, hdffile):
        self.hdfFile = hdffile
        # determine time zone information
        # do this once only to boost performance
        self.__times = []
        self.__timeStrings = []
        for i in range(1000000):
            try:
                zone = self.hdfFile["/zones/zone%d" % i]
                self.__times.append(zone.attrs['t'])
                self.__timeStrings.append(zone.attrs['time'].decode("utf-8"))
            except KeyError:
                break
        self.__times = numpy.array(self.__times)
        self.__timeStrings = numpy.array(self.__timeStrings)
        
    def numberOfZones(self):
        """
        Returns the number of zones in the hdf file.
        """
        return len(self.__times)
    
    def zoneTimes(self):
        """
        Returns an ordered list of zone times in seconds.
        """
        return self.__times.copy()
    
    def zoneTime(self, zoneId):
        """
        Returns the zone time in seconds
        """
        try:
            return self.__times[zoneId]
        except KeyError:
            return float('nan')
    
    def zoneTimeStr(self, zoneId, show_time = True):
        """
        Returns the zone time as string
        """
        try:
            zstr = self.__timeStrings[zoneId]
        except:
            return ""
        if not show_time:
            pos = zstr.index("T")
            if pos > 0:
                zstr = zstr[0:pos]
        return zstr
    
    def exitOk(self):
        """
        Returns true if the hdf file was properly exited.
        Will return false if the exit was not ok, which can indicate a hdf file corruption.
        """
        try:
            return self.hdfFile["/info"].attrs["exit-status"].decode("utf-8") == "ok"
        except:
            return False
    
    def endTimeReached(self):
        """
        Returns true if the model run reached the end time and closed the hdf file properly.
        """
        if not self.exitOk():
            return False
        try:
            return self.hdfFile["/info"].attrs["end-time-reached"].decode("utf-8") == "yes"
        except:
            return False
    
    def history(self, zonestr):
        """
        Returns the history over all zones of the quantity identified by zonestr.
        For example, to return a multi-dimensional array for pressure in elements zonestr would be:
            zonestr = "reservoir/Elements/Pressure"
        """
        l = []
        for i in range(self.numberOfZones()):
            l.append(self.hdfFile["/zones/zone%d/%s" % (i, zonestr)][:])
        return numpy.array(l)
    
    def attrHistory(self, zonestr, attr):
        """
        Returns the history over all zones of the attribute identified by zonestr and attr.
        For example, to return an array for the mass rate of recharge term "recharge" would be:
            zonestr = ""extramodules/recharge"
            attr = "Mass Rate"
        """
        l = []
        for i in range(self.numberOfZones()):
            l.append(self.hdfFile["/zones/zone%d/%s" % (i, zonestr)].attrs[attr])
        return numpy.array(l)
    
    def __toYearFrac(self, t):
        d = datetime.datetime.fromtimestamp(t)
        d0 = datetime.datetime(d.year, 1, 1)
        diy = 365.0
        # leap year?
        if d.year % 4 == 0:
            diy = 366.0
        return d.year + (d.timestamp() - d0.timestamp()) / (24 * 60 * 60 * diy)
    
    def toYearFrac(self, times):
        """
        Returns times (either scalar or array) to fractional year.
        Using fractional years is sometimes easier for calculations then datetime or seconds.
        """
        try:
            # is this iterable?
            yf = []
            for t in times:
                yf.append(self.__toYearFrac(t))
            return numpy.array(yf)
        except:
            # no, scalar!
            return self.__toYearFrac(times)
        
    def toDateTime(self, times):
        """
        Returns times (either scalar or array) to datetime
        """
        try:
            # is this iterable?
            yf = []
            for t in times:
                yf.append(datetime.datetime.fromtimestamp(t))
            return numpy.array(yf)
        except:
            # no, scalar!
            return datetime.datetime.fromtimestamp(times)

    def writeUnstructuredGrid(self, fname, ug):
        """
        Auxiliary method to write an unstructured grid to file.
        """
        writer = vtk.vtkXMLUnstructuredGridWriter()
        writer.SetFileName(fname)
        writer.SetInputData(ug)
        writer.Update()
        
    def writePolyData(self, fname, pd):
        """
        Auxiliary method to write a vtkPolyData grid to file.
        """
        writer = vtk.vtkXMLPolyDataWriter()
        writer.SetFileName(fname)
        writer.SetInputData(pd)
        writer.Update()
        
    def vtkDataArrayForType(self, dtype):
        """
        Auxiliary; returns a vtk array for the desired numpy dtype
        """
        if dtype == numpy.float32:
            return vtk.vtkFloatArray()
        if dtype == numpy.float64:
            return vtk.vtkDoubleArray()
        if dtype == numpy.int32:
            return vtk.vtkIntArray()
        if dtype == numpy.uint16:
            return vtk.vtkIntArray()
        if dtype == numpy.object:
            # this must be string array
            return vtk.vtkStringArray()
        return None
    
    def xmlInputText(self):
        """
        Returns the xml input text as stored in the hdf file.
        """
        try:
            txt_arr = self.hdfFile["/inputs/XML Input Text"][:]
            txt = ""
            for t in txt_arr: txt += chr(t)
            return txt
        except KeyError:
            return ""


    
