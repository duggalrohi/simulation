#!/usr/bin/python3

"""

reservoir.py

library to read in volsung reservoir data from Sigurd output files

"""

import math
import vtk

from volsung.sigurd import *

class Reservoir(Sigurd):
    """
    Reservoir object    
    """
    def __init__(self, hdffile, offset = (0,0,0), angle = 0):
        """
        Creates a grid object using the data in the hdffile and the path from where to read the data.
        offset and angle can be used to translate/rotate the grid. This can be useful when making slices in the x or y plane in order to align with the grid directions.
        """
        super().__init__(hdffile)
        self.gridPath = "/grid"
        self.__grid = self.baseGrid()
        self.translate(offset)
        self.rotate(angle)
        self.cellStateThreshold = 1             # use 1 to show enabled and fixed states, or 0 to just show enabled. 3 will show all cells.
        
    def translate(self, offset = (0,0,0)):
        """
        Translate the grid by the offset.
        Note: translating/rotating the grid will shift the positions of the wellbores.
        """
        trafo = vtk.vtkTransform()
        trafo.Translate(offset)
        tf = vtk.vtkTransformFilter()
        tf.SetTransform(trafo)
        tf.SetInputData(self.__grid)
        tf.Update()
        self.__grid.DeepCopy(tf.GetOutput())
        self.__buildLocator()
        
    def rotate(self, degrees_cw):
        """
        Rotates the grid by the clockwise angle in degrees.
        Note: translating/rotating the grid will shift the positions of the wellbores.
        """
        trafo = vtk.vtkTransform()
        trafo.RotateZ(-degrees_cw)
        tf = vtk.vtkTransformFilter()
        tf.SetTransform(trafo)
        tf.SetInputData(self.__grid)
        tf.Update()
        self.__grid.DeepCopy(tf.GetOutput())
        self.__buildLocator()

    def elevations(self):
        """
        Returns a unique list of cell centre elevations.
        This is a useful function when one wants to make a number of slice plots through the reservoir.
        But note if an undulated surface is present then one would want to use a threshold on the results.
        """
        raw = numpy.unique(self.hdfFile[self.gridPath + "/cells/Centre Z"][:])
        return numpy.sort(raw)

    def baseGrid(self):
        """
        Returns an empty vtkUnstructuredGrid. The only cell data array present is "Cell Id".
        """
        ug = vtk.vtkUnstructuredGrid()
        pts = vtk.vtkPoints()
        pts.SetDataTypeToDouble()
        ug.SetPoints(pts)
        try:
            X = self.hdfFile[self.gridPath + "/geometry/Vertex X"][:]
            Y = self.hdfFile[self.gridPath + "/geometry/Vertex Y"][:]
            Z = self.hdfFile[self.gridPath + "/geometry/Vertex Z"][:]
            ConnInfo = self.hdfFile[self.gridPath + "/geometry/Cell Connectivity Info"][:]
            ConnOff = self.hdfFile[self.gridPath + "/geometry/Cell Connectivity Offset"][:]
        except KeyError:
            # no gird present - may be a T2Fafnir mode file
            # so return the empty grid
            return ug
        # create the grid and insert the points
        for i in range(X.size):
            pts.InsertNextPoint(X[i], Y[i], Z[i])
        # create the cells and the Cell Id array
        ncells = ConnOff.size
        cidarr = vtk.vtkIntArray()
        cidarr.SetNumberOfComponents(1)
        cidarr.SetNumberOfTuples(ncells)
        cidarr.SetName("Cell Id")
        ug.GetCellData().AddArray(cidarr)
        for i in range(ncells):
            cell_type = ConnInfo[ConnOff[i]]
            nverts = ConnInfo[ConnOff[i] + 1]
            lst = vtk.vtkIdList()
            for j in range(nverts):
                lst.InsertNextId(ConnInfo[ConnOff[i] + 2 + j])
            cid = ug.InsertNextCell(cell_type, lst)
            cidarr.SetTuple1(i, cid)
        return ug
    
    def __buildLocator(self):
        """
        Using the current self.__grid build a locator structure which will work on all kind of cells.
        """
        # create tetras
        self.__tetraFilter = vtk.vtkDataSetTriangleFilter()
        self.__tetraFilter.TetrahedraOnlyOn()
        self.__tetraFilter.SetInputData(self.__grid)
        self.__tetraFilter.Update()
        # create the locator
        self.__locator = vtk.vtkCellLocator()
        self.__locator.SetDataSet(self.__tetraFilter.GetOutput())
        self.__locator.BuildLocator()

    def cellId(self, pos):
        """
        Returns the cell id for a given position (x,y,z).
        Returns -1 if the position is outside the grid.
        """
        id_raw = self.__locator.FindCell(pos)
        if id_raw < 0: return -1
        return int(self.__tetraFilter.GetOutput().GetCellData().GetArray("Cell Id").GetTuple1(id_raw))
    
    def elementIndex(self, cellid, layerid = 0):
        """
        Returns the index of the element given by cellid, layerid
        """
        CellId = self.hdfFile["/zones/zone0/reservoir/Elements/Cell Id"][:]
        LayerId = self.hdfFile["/zones/zone0/reservoir/Elements/Layer Id"][:]
        cids = numpy.where(CellId == cellid)[0]
        for c in cids:
            if LayerId[c] == layerid: return c
        return -1
    
    def mincGrid(self, layerId):
        """
        Looks into zone0 element data to determine which cell is associated with the desired layerId.
        Then returns a vtkUnstructuredGrid which is a sub grid from baseGrid.
        """
        CellId = self.hdfFile["/zones/zone0/reservoir/Elements/Cell Id"][:]
        LayerId = self.hdfFile["/zones/zone0/reservoir/Elements/Layer Id"][:]
        # create a selection source and fill in with desired cell indices
        source = vtk.vtkSelectionSource()
        source.SetContentType(vtk.vtkSelectionNode.INDICES)
        source.SetFieldType(vtk.vtkSelectionNode.CELL)
        for i in range(CellId.size):
            if LayerId[i] == layerId:
                source.AddID(0, CellId[i])
        # cut out the selection
        sf = vtk.vtkExtractSelection()
        sf.SetInputData(self.__grid)
        sf.SetSelectionConnection(source.GetOutputPort())
        sf.Update()
        return sf.GetOutput()
    
    def grid(self, zoneId, layerId):
        """
        Returns an unstructured grid filled with reservoir data for the desired zoneId and layerId.
        """
        if zoneId < 0: zoneId = self.numberOfZones() - 1        # select the last zone
        
        ug = self.mincGrid(layerId)
        elems = self.hdfFile["/zones/zone%d/reservoir/Elements" % zoneId]
        cidarr = ug.GetCellData().GetArray("Cell Id")
        # build a lookup index for the cell ids we require; doing this once saves time later on
        CellId = elems["Cell Id"][:]
        LayerId = elems["Layer Id"][:]
        ncells = cidarr.GetNumberOfTuples()
        index = {}
        for i in range(ncells):
            cid = cidarr.GetTuple1(i)
            testids = numpy.where(CellId == cid)[0]
            for j in testids:
                if LayerId[j] == layerId:
                    index[cid] = j
                    break
        # create arrays and fill in data
        for e in elems:
            # don't overwrite the cell ids - they should be the same though
            if e == "Cell Id": continue
            data = elems[e][:]
            # create new array
            arr = self.vtkDataArrayForType(data.dtype)
            # unsupported data type?
            if arr is None: continue
            arr.SetName(e)
            arr.SetNumberOfComponents(1)
            ug.GetCellData().AddArray(arr)
            # fill in the data
            if arr.IsNumeric():
                arr.SetNumberOfTuples(ncells)
                for i in range(ncells):
                    cid = cidarr.GetTuple1(i)
                    arr.SetTuple1(i, data[index[cid]])
            else:
                # must be strings
                arr.SetNumberOfValues(ncells)
                for i in range(ncells):
                    cid = cidarr.GetTuple1(i)
                    xx = data[index[cid]]
                    arr.SetValue(i, xx.decode("utf-8"))
        # done!
        return ug
    
    def slice(self, zoneId, layerId, origin, normal):
        """
        Returns a vtkPolyData slice plane through the grid for zoneId and layerId.
        origin and normal describe the plane
        """
        ug = self.grid(zoneId, layerId)
        plane = vtk.vtkPlane()
        plane.SetNormal(normal)
        plane.SetOrigin(origin)
        # create a threshold to remove unwanted cells, like disabled or fixed state
        thresh = vtk.vtkThreshold()
        thresh.SetInputData(ug)
        thresh.SetInputArrayToProcess(0, 0, 0, vtk.vtkDataObject.FIELD_ASSOCIATION_CELLS, "State");
        thresh.ThresholdByLower(self.cellStateThreshold)
        # create tetras for cutter to work with voronoi
        tf = vtk.vtkDataSetTriangleFilter()
        tf.SetInputConnection(thresh.GetOutputPort())
        tf.TetrahedraOnlyOn()
        slicer = vtk.vtkCutter()
        slicer.SetInputConnection(tf.GetOutputPort())
        slicer.SetCutFunction(plane)
        slicer.SetValue(0, 0.0)
        slicer.Update()
        return slicer.GetOutput()
    
    def sliceTriangleData(self, zoneId, layerId, origin, normal, arrname):
        """
        Returns triangle data for a slice through the reservoir.
        The return is (triangles, edges).
        triangles is a list consisting of (v0, v1, v2, data), whith v0, v1, v2 being (x,y,z) vertices of the triangle
        edges is the list of edges between the cells and is (v0, v1) with v0, v1 being (x,y,z) vertices of the edges
        """
        # first create the slice
        pd = self.slice(zoneId, layerId, origin, normal)
        # use a triangle filter to ensure only triangles are present
        tf = vtk.vtkTriangleFilter()
        tf.SetInputData(pd)
        tf.Update()
        trias = tf.GetOutput()
        pts = trias.GetPoints()
        # extract the triangles and their data
        arr = trias.GetCellData().GetArray(arrname)
        triangles = []
        for i in range(trias.GetNumberOfCells()):
            tria = trias.GetCell(i)
            v0 = pts.GetPoint(tria.GetPointId(0))
            v1 = pts.GetPoint(tria.GetPointId(1))
            v2 = pts.GetPoint(tria.GetPointId(2))
            data = arr.GetTuple1(i)
            triangles.append((v0, v1, v2, data))
        # extract the edges, but only those which have different Cell Id
        cidarr = trias.GetCellData().GetArray("Cell Id")
        edges = []
        edgeset = set()        # for determining unique edges
        for i in range(trias.GetNumberOfCells()):
            tria = trias.GetCell(i)
            cid_this = cidarr.GetTuple1(i)
            for j in range(tria.GetNumberOfEdges()):
                edge = tria.GetEdge(j)
                pid0 = edge.GetPointId(0)
                pid1 = edge.GetPointId(1)
                if pid0 > pid1:
                    pid0, pid1 = pid1, pid0
                # already in set, then ignore?
                if (pid0, pid1) in edgeset: continue
                # which original cells does this edge border onto?
                lst = vtk.vtkIdList()
                lst.InsertNextId(pid0)
                lst.InsertNextId(pid1)
                neighbors = vtk.vtkIdList()
                trias.GetCellNeighbors(i, lst, neighbors)
                if neighbors.GetNumberOfIds() == 1:
                    cid_other = cidarr.GetTuple1(neighbors.GetId(0))
                    # ignore edge if it belongs to the same cell id
                    if cid_other == cid_this: continue
                # store the edge
                v0 = pts.GetPoint(pid0)
                v1 = pts.GetPoint(pid1)
                edges.append((v0, v1))                
                edgeset.add((pid0, pid1))
        return triangles, edges

    def slicePlotTransformation(self, position, normal, up):
        """
        Auxiliary method to create a 3D -> 2D transformation for slices.
        """
        # determine the 3D -> 2D transformation
        # first work out the base vectors
        xd = [0,0,0]
        yd = [0,0,0]
        vtk.vtkMath.Cross(up, normal, xd)
        vtk.vtkMath.Normalize(xd)
        vtk.vtkMath.Cross(normal, xd, yd)
        vtk.vtkMath.Normalize(yd)
        # now create a landmark transform
        trafo = vtk.vtkLandmarkTransform()
        trafo.SetModeToAffine()
        source = vtk.vtkPoints()
        source.SetDataTypeToDouble()
        target = vtk.vtkPoints()
        target.SetDataTypeToDouble()
        source.InsertNextPoint(position[0], position[1], position[2])
        target.InsertNextPoint(0,0,0)
        source.InsertNextPoint(position[0] + xd[0], position[1] + xd[1], position[2] + xd[2])
        target.InsertNextPoint(1,0,0)
        source.InsertNextPoint(position[0] + yd[0], position[1] + yd[1], position[2] + yd[2])
        target.InsertNextPoint(0,1,0)
        source.InsertNextPoint(position[0] + normal[0], position[1] + normal[1], position[2] + normal[2])
        target.InsertNextPoint(0,0,1)
        source.InsertNextPoint(position[0] + xd[0] + yd[0], position[1] + xd[1] + yd[1], position[2] + xd[2] + yd[2])
        target.InsertNextPoint(1,1,0)
        trafo.SetSourceLandmarks(source)
        trafo.SetTargetLandmarks(target)
        trafo.Modified()
        return trafo
       
    def slicePlot(self, fig, ax, pos, zoneId, direction = "+z", arrname = "Temperature", layerId = 0, offset = 0.0, scale = 1.0, minimum = None, maximum = None, edgecolor = '#A0A0A0', cmap = 'jet', normal = (0,0,1), up = (0,0,1), scale_length = 1.0):
        """
        Creates a horizontal slice plot onto the matplotlib axes ax on the figure fig
        Parameter:
            pos                 coordinate for the plot; this will become x/y/z value depending on direction if direction is used. Else it needs to be a (x,y,z) tuple.
            zoneId              zone Id (time index)
            direction           +/-x, +/-y, +/-z direction for the slice. If you want to use pos/normal set direction to another string, like ""
            arrname             the data array name
            layerId             the MINC layer index
            offset, scale       used to transform the data, i.e. custom = SI * scale + offset
            minimum, maximum    minimum/maximum value for data range. If None then auto scale will be applied
            normal              normal (x,y,z) to be used if direction is not set
            up                  up direction to be used if direction is not set
            scale_length        scale for the lengths, i.e. x/y/z. Use this if you want to convert metres to feet etc.
        """
        if direction not in ["+x", "-x", "+y", "-y", "+z", "-z"]:
            position = pos
        # determine the directional parameters if direction is set
        if direction in ["+x", "-x"]:
            position = (pos, 0, 0)
            normal = (int(direction[0]+'1'), 0, 0)
            up = (0,0,1)
        if direction in ["+y", "-y"]:
            position = (0, pos, 0)
            normal = (0, int(direction[0]+'1'), 0)
            up = (0,0,1)
        if direction in ["+z", "-z"]:
            position = (0, 0, pos)
            normal = (0, 0, int(direction[0]+'1'))
            up = (0,1,0)
        # ensure normal and up are unity vectors
        normal_ = [normal[0], normal[1], normal[2]]
        vtk.vtkMath.Normalize(normal_)
        normal = normal_
        up_ = [up[0], up[1], up[2]]
        vtk.vtkMath.Normalize(up_)
        up = up_
        # perform the slice
        triangles, edges = self.sliceTriangleData(zoneId, layerId, position, normal, arrname)
        # create the 3D -> 2D transformation
        trafo = self.slicePlotTransformation(position, normal, up)
        # transform the data
        data = []
        patches = []
        for t in triangles:
            verts = numpy.zeros((3,2), dtype = numpy.float64)
            for i in range(3):
                vi = trafo.TransformDoublePoint(t[i])
                for j in range(2):
                    verts[i][j] = vi[j] * scale_length
            polygon = matplotlib.patches.Polygon(verts, True)
            patches.append(polygon)
            data.append(t[3] * scale + offset)
        # determine the maximum/minimum
        if minimum is None:
            minimum = min(data)
        if maximum is None:
            maximum = max(data)
        # plot the triangles
        pc = matplotlib.collections.PatchCollection(patches, zorder=0)
        pc.set_cmap(cmap)
        pc.set_clim(minimum, maximum)
        pc.set_array(numpy.array(data, dtype = numpy.float64))
        pc.set_edgecolor('face')
        ax.add_collection(pc)
        fig.colorbar(pc, ax=ax)
        # plot the edges
        if edgecolor is not None:
            for e in edges:
                pt0 = trafo.TransformDoublePoint(e[0])
                pt1 = trafo.TransformDoublePoint(e[1])
                l = matplotlib.lines.Line2D(numpy.array([pt0[0] * scale_length, pt1[0] * scale_length]), numpy.array([pt0[1] * scale_length, pt1[1] * scale_length]), linewidth = 1, color = edgecolor)
                ax.add_line(l)
    
    def __probePoints(self, ug, vtkpointset):
        # create a tetras so the following probe works with voronois
        tf = vtk.vtkDataSetTriangleFilter()
        tf.TetrahedraOnlyOn()
        tf.SetInputData(ug)
        # generate the probe filter
        pf = vtk.vtkProbeFilter()
        pf.SetInputData(vtkpointset)
        pf.SetSourceConnection(tf.GetOutputPort())
        pf.PassCellArraysOff()
        pf.PassPointArraysOff()
        pf.Update()
        # pass data over to vtkpointset
        vtkpointset.GetPointData().PassData(pf.GetOutput().GetPointData())
        # correct invalid points outside the grid to nan
        valid = pf.GetOutput().GetPointData().GetArray(pf.GetValidPointMaskArrayName())
        for i in range(vtkpointset.GetPointData().GetNumberOfArrays()):
            arr = vtkpointset.GetPointData().GetArray(i)
            if not arr.IsNumeric(): continue
            for j in range(valid.GetNumberOfTuples()):
                if valid.GetTuple1(j) != 1.0:
                    arr.SetTuple1(j, float('nan'))
    
    def probePoints(self, vtkpointset, zoneId, layerId = 0):
        """
        Probes all points in the vtkpointset and returns vtkpointset with new arrays from the probe.
        If vtkpointset is a list or iterable then all of them will be probed
        """
        ug = self.grid(zoneId, layerId)
        try:
            for ps in vtkpointset:
                self.__probePoints(ug, ps)
        except TypeError:
            self.__probePoints(ug, vtkpointset)
            
    def __interpolatePoints(self, ug, vtkpointset, kernel = None):
        """
        Interpolate the points in vtkpointset using source ug
        kernel is optional and needs to be of type vtk.vtkInterpolationKernel
        """
        # create a point set from the cells of the grid
        tf = vtk.vtkCellDataToPointData()
        tf.SetInputData(ug)
        # generate the interpolation filter
        pf = vtk.vtkPointInterpolator()
        pf.SetInputData(vtkpointset)
        pf.SetSourceConnection(tf.GetOutputPort())
        pf.PassCellArraysOff()
        pf.PassPointArraysOff()
        pf.SetNullValue(float('nan'))
        if kernel is None:
            pf.SetKernel(vtk.vtkShepardKernel())
            pf.GetKernel().SetNumberOfPoints(8)
            pf.GetKernel().SetKernelFootprintToNClosest()
        else:
            pf.SetKernel(kernel)
        pf.Update()
        # pass data over to vtkpointset
        vtkpointset.GetPointData().PassData(pf.GetOutput().GetPointData())
    
    def interpolatePoints(self, vtkpointset, zoneId, layerId = 0, kernel = None):
        """
        Interpolates all points in the vtkpointset and returns vtkpointset with new arrays from the interpolation.
        If vtkpointset is a list or iterable then all of them will be interpolated
        kernel is optional and needs to be of type vtk.vtkInterpolationKernel
        """
        ug = self.grid(zoneId, layerId)
        try:
            for ps in vtkpointset:
                self.__interpolatePoints(ug, ps, kernel = kernel)
        except TypeError:
            self.__interpolatePoints(ug, vtkpointset, kernel = kernel)
            
    def arraysFromVtkPoints(self, vtkpointset):
        """
        For all points in vtkpointset extract the point data as arrays.
        """
        # first the coordinates
        data = {"x" : [], "y" : [], "z" : []}
        for i in range(vtkpointset.GetNumberOfPoints()):
            pt = vtkpointset.GetPoints().GetPoint(i)
            data["x"].append(pt[0])
            data["y"].append(pt[1])
            data["z"].append(pt[2])
        # then the arrays
        for j in range(vtkpointset.GetPointData().GetNumberOfArrays()):
            ls = []
            arr = vtkpointset.GetPointData().GetArray(j) 
            data[arr.GetName()] = ls
            for i in range(vtkpointset.GetNumberOfPoints()):
                if arr.IsNumeric:
                    ls.append(arr.GetTuple1(i))
                else:
                    ls.append(arr.GetValue(i))
        # convert all lists to numpy arrays
        for k in data.keys():
            data[k] = numpy.array(data[k])
        return data
    
    def __probeCells(self, ug, vtkcellset):
        # create a tetras so the following probe works with voronois
        tf = vtk.vtkDataSetTriangleFilter()
        tf.TetrahedraOnlyOn()
        tf.SetInputData(ug)
        # create cell centres for the vtkcellset
        cf = vtk.vtkCellCenters()
        cf.SetInputData(vtkcellset)
        # generate the probe filter
        pf = vtk.vtkProbeFilter()
        pf.SetInputConnection(cf.GetOutputPort())
        pf.SetSourceConnection(tf.GetOutputPort())
        pf.PassCellArraysOff()
        pf.PassPointArraysOff()
        pf.Update()
        # pass data over to vtkcellset
        vtkcellset.GetCellData().PassData(pf.GetOutput().GetPointData())
        # correct invalid points outside the grid to nan
        valid = pf.GetOutput().GetPointData().GetArray(pf.GetValidPointMaskArrayName())
        for i in range(vtkcellset.GetCellData().GetNumberOfArrays()):
            arr = vtkcellset.GetCellData().GetArray(i)
            if not arr.IsNumeric(): continue
            for j in range(valid.GetNumberOfTuples()):
                if valid.GetTuple1(j) != 1:
                    arr.SetTuple1(j, float('nan'))
    
    def probeCells(self, vtkcellset, zoneId, layerId = 0):
        """
        Probes all cells in the vtkcellset and returns vtkcellset with new arrays from the probe.
        If vtkcellset is a list or iterable then all of them will be probed
        """
        ug = self.grid(zoneId, layerId)
        try:
            for cs in vtkcellset:
                self.__probeCells(ug, cs)
        except TypeError:
            self.__probeCells(ug, vtkcellset)
    
    def _averageArrays(self, arrays, arrname):
        data = {}
        data[arrname] = numpy.unique(arrays[arrname])
        n = data[arrname].size
        for k in arrays.keys():
            if k == arrname: continue
            l = []
            for i in range(n):
                index = numpy.where(arrays[arrname] == data[arrname][i])
                l.append(numpy.sum(arrays[k][index]) / (index[0].size * 1.0))
            data[k] = numpy.array(l)
        return data
    
    def probeWellTrack(self, wellGridGeometry, zoneId, layerId = 0, average = False, wriggle = 1.0):
        """
        Convenience function to probe the reservoir data with a welltrack.
        Returns the reservoir data along the welltrack in a dictionary, sorted by z-elevation of the welltrack.
        wriggle is used when average is False to generate points above/below the points in wellGridGeometry
                increase this value if the probe filter has problems generating a "step" function
        """
        probe = vtk.vtkPolyData()
        if average:
            # probe at the cell centres
            cf = vtk.vtkCellCenters()
            cf.SetInputData(wellGridGeometry)
            cf.Update()
            probe.SetPoints(cf.GetOutput().GetPoints())
        else:
            # probe a tiny bit above and below the cell faces
            pts = vtk.vtkPoints()
            pts.SetDataTypeToDouble()
            probe.SetPoints(pts)
            for i in range(wellGridGeometry.GetNumberOfPoints()):
                pt = wellGridGeometry.GetPoint(i)
                pts.InsertNextPoint(pt[0], pt[1], pt[2] + wriggle)
                pts.InsertNextPoint(pt[0], pt[1], pt[2] - wriggle)
        # perform the probe action
        self.probePoints(probe, zoneId, layerId)
        probe_arrays = self.arraysFromVtkPoints(probe)
        sort_index = numpy.argsort(probe_arrays["z"])
        for k in probe_arrays.keys():
            probe_arrays[k] = probe_arrays[k][sort_index]
        return probe_arrays

    def interpolateWellTrack(self, wellGridGeometry, zoneId, layerId = 0, kernel = None):
        """
        Convenience function to interpolate the reservoir data with a welltrack.
        Returns the reservoir data along the welltrack in a dictionary, sorted by z-elevation of the welltrack.
        kernel is optional and needs to be of type vtk.vtkInterpolationKernel
        """
        probe = vtk.vtkPolyData()
        probe.DeepCopy(wellGridGeometry)
        # perform the interpolate action
        self.interpolatePoints(probe, zoneId, layerId, kernel)
        probe_arrays = self.arraysFromVtkPoints(probe)
        sort_index = numpy.argsort(probe_arrays["z"])
        for k in probe_arrays.keys():
            probe_arrays[k] = probe_arrays[k][sort_index]
        return probe_arrays
