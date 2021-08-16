#!/usr/bin/python3

"""

brynhild.py

library to work on Brynhild xml input files.

"""

import xml.etree.ElementTree

class Brynhild(object):
    """
    Brynhild xml input file class
    """
    def __init__(self, fname = ""):
        if fname != "":
            self.__xml = xml.etree.ElementTree.parse(fname)
        else:
            self.__xml = xml.etree.ElementTree        # make this an empty tree so we can still work with it
            
    def _setXMLText(self, txt):
        if (len(txt) > 0):
            self.__xml = xml.etree.ElementTree.fromstring(txt)
        else:
            self.__xml = xml.etree.ElementTree        # make this an empty tree so we can still work with it
        
    def flowNetworkObjectNode(self, objectId):
        """
        returns the xml node containing the flow network port object with given id
        """
        # find parent node
        pn = self.__xml.findall('.//flownetworkobjects')[0]
        # iterate over all flow network port objects and test them
        for n in pn:
            try:
                if objectId == int(n.find("id").text):
                    return n
            except:
                pass
        return None
