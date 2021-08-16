#!/usr/bin/python3

"""

flownetworkportobject.py

library to define flow network port object base class

"""

import h5py
import vtk
import numpy
import matplotlib

from volsung.flownetworkport import *
from volsung.reservoir1dfielddata import *

class FlowNetworkPortObject(object):
    """
    Base class for FlowNetworkPortObjects.
    The base class can be used for generic objects; subclasses can be used where
    more functionality is needed
    """
    def __init__(self, name):
        self.name = name
        self.inputPorts = []
        self.outputPorts = []
        self.activeStatus = []                  # active status 0 or 1 by zone index
        self.wellGridGeometry = []              # well/grid geometry data by zone index
        self.reservoir1DFieldData = None
        
    def _readStaticData(self, hdffile):
        """
        Read static data from hdffile provided.
        """
        node = hdffile["/zones/zone0/flownetwork/objects/" + self.name]
        self.objectId = node.attrs["Object Id"]
        # create the input/output ports
        self.inputPorts = []
        self.outputPorts = []
        # auxiliary - unsorted ports
        ips = {}
        ops = {}
        for i in range(hdffile["/zones/zone0/flownetwork/Ports/Port Object Id"][:].size):
            objid = hdffile["/zones/zone0/flownetwork/Ports/Port Object Id"][i]
            if objid != self.objectId: continue
            t = hdffile["/zones/zone0/flownetwork/Ports/Port Type"][i]
            pid = hdffile["/zones/zone0/flownetwork/Ports/Port Id"][i]
            if t == 79:
                ops[pid] = OutputPort(pid, i)
            else:
                ips[pid] = InputPort(pid, i)
        for k in sorted(ips.keys()):
            self.inputPorts.append(ips[k])
        for k in sorted(ops.keys()):
            self.outputPorts.append(ops[k])
        
    def __readZoneWellGridGeometryInfo(self, hdffile, zoneId):
        """
        Read the well/grid geometry info and return it as vtkPolyData or None
        """
        wggi = None
        try:
            wggi_grp = hdffile["/zones/zone%d/flownetwork/objects/%s/Well Grid Geometry Info" % (zoneId, self.name)]
            
            # read the data into memory - faster than reading individually from disk
            CellConnectivityOffset = wggi_grp["Cell Connectivity Offset"][:]
            CellConnectivityInfo = wggi_grp["Cell Connectivity Info"][:]
            CellsCellId = wggi_grp["Cells Cell Id"][:]
            PointsCellId = wggi_grp["Points Cell Id"][:]
            X = wggi_grp["X"][:]
            Y = wggi_grp["Y"][:]
            Z = wggi_grp["Z"][:]
            
            # create the vtkPolyData containing the geometric information
            ncells = CellConnectivityOffset.size
            npts = X.size

            wggi = vtk.vtkPolyData()
            pts = vtk.vtkPoints()
            pts.SetDataTypeToDouble()
            wggi.SetPoints(pts)
            wggi.Allocate(ncells)
            
            ccid_arr = vtk.vtkIntArray()
            ccid_arr.SetName("Cells Cell Id")
            ccid_arr.SetNumberOfComponents(1)
            ccid_arr.SetNumberOfTuples(ncells)
            wggi.GetCellData().AddArray(ccid_arr)
            
            pcid_arr = vtk.vtkIntArray()
            pcid_arr.SetName("Points Cell Id")
            pcid_arr.SetNumberOfComponents(1)
            pcid_arr.SetNumberOfTuples(npts)
            wggi.GetCellData().AddArray(pcid_arr)
            
            for i in range(npts):
                pts.InsertNextPoint(X[i], Y[i], Z[i])
                pcid_arr.SetTuple1(i, PointsCellId[i])
                
            for i in range(ncells):
                t = CellConnectivityInfo[CellConnectivityOffset[i]]
                n = CellConnectivityInfo[CellConnectivityOffset[i] + 1]
                lst = vtk.vtkIdList()
                for j in range(n):
                    lst.InsertNextId(CellConnectivityInfo[CellConnectivityOffset[i] + 2 + j])
                wggi.InsertNextCell(t, lst)
                ccid_arr.SetTuple1(i, CellsCellId[i])
        except:
            pass
        return wggi
        
    def _readZoneData(self, hdffile, zoneId, porttable = None):
        """
        Read zone data.
        This method needs to be called sequentially with correct zoneId
        For efficiency purposes the port table for the zone can be passed in as a dictionary
        """
        # read own status data
        objgroup = hdffile["/zones/zone%d/flownetwork/objects/%s" % (zoneId, self.name)]
        self.activeStatus.append(objgroup.attrs["active"])
        # read the port data
        for port in self.inputPorts: port._readHDFTableData(hdffile, zoneId, porttable)
        for port in self.outputPorts: port._readHDFTableData(hdffile, zoneId, porttable)
        # read the well grid geometry info, if present
        self.wellGridGeometry.append(self.__readZoneWellGridGeometryInfo(hdffile, zoneId))
        
    def _readXML(self, node):
        """
        Read in additional data from xml input node pointing into this object
        """
        for port in node.find("inputports"):
            self.inputPorts[int(port.attrib["portid"])]._readXML(port)
        for port in node.find("outputports"):
            self.outputPorts[int(port.attrib["portid"])]._readXML(port)
        # read in reservoir 1D field data if present
        if node.find("reservoir1dfielddata") is not None:
            self.reservoir1DFieldData = Reservoir1DFieldData()
            self.reservoir1DFieldData._readXML(node.find("reservoir1dfielddata"))
            
    def wellTrack(self, zoneId):
        """
        Returns a dictionary containing the welltrack data for zoneId
        """
        track = self.wellGridGeometry[zoneId]
        if track is None:
            return {"x" : numpy.array([]), "y" : numpy.array([]), "z" : numpy.array([])}
        X = []
        Y = []
        Z = []
        for i in range(track.GetNumberOfPoints()):
            pt = track.GetPoints().GetPoint(i)
            X.append(pt[0])
            Y.append(pt[1])
            Z.append(pt[2])
        X = numpy.array(X)
        Y = numpy.array(Y)
        Z = numpy.array(Z)
        index = numpy.argsort(Z)
        X = X[index]
        Y = Y[index]
        Z = Z[index]
        return {"x" : X, "y" : Y, "z" : Z}
        
    def plotWellTrack(self, fig, ax, zoneId = 0, linewidth = 5, color = "#000000", fontsize = 0, labeloffset = (0,0)):
        """
        If welltrack is present, plot it onto ax's XY plane
        If fontsize is not 0 then names will be plotted as well.
        """
        track = self.wellTrack(zoneId)
        if track is None: return
        ax.plot(track["x"], track["y"], "-", linewidth=linewidth, color = color)
        if track["x"].size > 0:
            # add a disc to first/last track point
            ax.plot(track["x"][0], track["y"][0], "o", markersize=(linewidth // 2) * 2 , color = color)
            ax.plot(track["x"][-1], track["y"][-1], "o", markersize=(linewidth // 2) * 2, color = color)
            # add name to plot?
            if fontsize != 0:
                ax.text(track["x"][0]+labeloffset[0], track["y"][0]+labeloffset[1], self.name, horizontalalignment='left', verticalalignment='bottom', fontsize = fontsize, color = color)
            
    def plotWellTrackFieldData(self, f, ax, z, time, arrname, offset = 0.0, scale = 1.0, radius = 10.0, zoneId = -1, fontsize = 0, labeloffset = (0,0), labelcolor = "#000000"):
        """
        If welltrack is present plot field data value for given elevation z and time slice parameter time.
        Note that the field data must consist of unique z-elevations for the interpolation to z to work.
        The colormap will be chosen from the first collection, i.e. it needs to exist beforehand.
        """
        track = self.wellTrack(zoneId)
        if track is None: return
        # don't plot if welltrack does not have this elevation
        if track["z"].size == 0: return
        if z > numpy.max(track["z"]): return
        if z < numpy.min(track["z"]): return
        # determine the x/y coordinates for the track
        try:
            x = numpy.interp(z, track["z"], track["x"])
            y = numpy.interp(z, track["z"], track["y"])
        except:
            # can't plot
            return
        # determine the value for the given elevation
        value = float('nan')
        if self.reservoir1DFieldData:
            fd = self.reservoir1DFieldData.timeSlice(time)
            try:
                fdz = fd["z"]
                fdv = fd[arrname]
                value = numpy.interp(z, fdz, fdv)
            except:
                pass
        # calculate custom value
        value = value * scale + offset            
        # plot the disc
        patches = []
        disc = matplotlib.patches.Circle((x,y), radius = radius)
        patches.append(disc)
        pc = matplotlib.collections.PatchCollection(patches, zorder = len(ax.collections)+2)
        if not math.isnan(value):
            try:
                pc.set_cmap(ax.collections[0].colorbar.cmap)
                pc.set_clim(ax.collections[0].get_clim())
                pc.set_array(numpy.array([value]))
            except:
                pc.set_color("#FFFFFF")
        else:
            # color for nan
            pc.set_color("#FFFFFF")
        pc.set_edgecolor('#000000')
        ax.add_collection(pc)
        # add name to plot?
        if fontsize != 0:
            ax.text(x+labeloffset[0], y+labeloffset[1], self.name, horizontalalignment='left', verticalalignment='bottom', fontsize = fontsize, color = labelcolor)
