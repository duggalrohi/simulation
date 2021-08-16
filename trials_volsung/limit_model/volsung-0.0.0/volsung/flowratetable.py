#!/usr/bin/python3

"""

flowratetable.py

simple data table structure to read a flow rate table from XML

"""

import h5py
import vtk
import numpy
import matplotlib

class FlowRateTable(object):
    """
    A Flow Rate Table object
    """
    
    def __init__(self):
        self.data = {}
        
    def _readXML(self, xmlnode):
        """
        Reads the data within xmlnode
        """
        self.data.clear()
        self.data["Time"] = []
        self.data["Pressure"] = []
        self.data["Energy Rate"] = []
        self.data["Mass Rate"] = []
        self.data["Enthalpy"] = []
        for tablerow in xmlnode:
            time = float(tablerow.find("time").text)
            self.data["Time"].append(time)
            for q in tablerow.find("flowrate"):
                val = float(q.text)
                if q.tag == "p":
                    self.data["Pressure"].append(val)
                    continue
                if q.tag == "q":
                    self.data["Energy Rate"].append(val)
                    continue
                if q.tag == "w":
                    self.data["Mass Rate"].append(val)
                    continue
                if q.tag == "h":
                    self.data["Enthalpy"].append(val)
                    continue
                if q.tag[0] == "x":
                    # mass fraction, special treatement
                    xname = q.tag.upper()
                    try:
                        self.data[xname].append(val)
                    except:
                        self.data[xname] = [val]
        # convert all to numpy arrays
        for k in self.data.keys():
            self.data[k] = numpy.array(self.data[k])
                
    