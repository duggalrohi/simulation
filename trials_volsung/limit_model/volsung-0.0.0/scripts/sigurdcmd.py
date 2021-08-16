#!/usr/bin/python3

"""

sigurdcmd.py - a command line tool to work with .sigurd output files

"""

from volsung.volsungmodel import *
import argparse
import h5py
import sys

class SigurdCmd(object):
    def __init__(self, results_fname = 'Results.sigurd', brynhild_fname = ''):
        self.VolsungModel = VolsungModel(results_fname, brynhild_fname)
        
    def printZoneInfo(self):
        print("Zone Information:")
        print("")
        for i in range(self.VolsungModel.reservoir.numberOfZones()):
            print("zone id %5d: %s" % (i, self.VolsungModel.reservoir.zoneTimeStr(i)))
        print("")
        
    def generateIncon(self, zoneid):
        if (zoneid < 0) or (zoneid >= self.VolsungModel.reservoir.numberOfZones()):
            print("Illegal zone id, valid zone ids/times are:")
            print()
            self.printZoneInfo()
            return
        fname = 'INCON.fafnir'
        print("Generating file %s from zone id %d..." % (fname, zoneid))
        print("The time for zone id %d: %s" % (zoneid, self.VolsungModel.reservoir.zoneTimeStr(zoneid)))
        # create the INCON file
        hdf = h5py.File(fname, "w")
        self.VolsungModel.reservoir.hdfFile.copy("/zones/zone%d/reservoir/SaveState" % zoneid, hdf, shallow=False, expand_soft=True, expand_external=True, expand_refs=True, without_attrs=False)
        hdf.close()
        print("...done!")
        

if __name__ == "__main__":
    parser = argparse.ArgumentParser("sigurdcmd")
    # for setting up the data
    parser.add_argument('resultsfile', nargs='?', default='Results.sigurd', help='The hdf output file from sigurd, e.g. Results.sigurd.')
    parser.add_argument('--brynhild', dest='brynhildfile', default='', help='The optional brynhild input file; usually read in from the hdf output file if present there.')
    # commands to execute
    parser.add_argument('--zones', action='store_true', default=False, help='Print the zone information.')
    parser.add_argument('--incon-zone', dest = 'inconzone', default='-1', help='Generate an INCON.fafnir file using the primary variables stored in the zone id supplied to this argument.')
    
    args = parser.parse_args()

    if len(sys.argv) == 1:
        # no arguments given, use help argument
        parser.print_help(sys.stderr)
        sys.exit(0)
    
    # create the command tool
    sigurdcmd = SigurdCmd(args.resultsfile, args.brynhildfile)    
    
    # execute desired commands
    if args.zones:
        sigurdcmd.printZoneInfo()
    
    inconzone = int(args.inconzone)
    if inconzone >= 0:
        sigurdcmd.generateIncon(inconzone)
