#!/usr/bin/python3

"""

signy.py

base class library to work with the Signy thermodynamic table tool

"""

import subprocess
import os
import sys
import shutil

class PhaseParameter(object):
    """
    Class holding phase properties
    """
    def __init__(self, components):
        self.SpecificFraction = float('nan')
        self.Saturation = float('nan')
        self.Enthalpy = float('nan')
        self.Density = float('nan')
        self.Viscosity = float('nan')
        self.MassFraction = {}.copy()
        for c in components:
            self.MassFraction[c] = float('nan')

class ThermodynamicTable(object):
    """
    Abstract base class for all thermodynamic tables
    """
    def __init__(self, table_type, components, phases):
        self.__TableType = table_type
        self.__Components = components
        self.__Phases = phases
        self.__initParameters()
        self.__signyOutput = ""
        
    def __initParameters(self):
        self.Pressure = float('nan')
        self.Enthalpy = float('nan')
        self.Temperature = float('nan')
        self.Density = float('nan')
        self.SurfaceTension = float('nan')
        self.MassFraction = {}.copy()
        # component mass fractions
        for c in self.__Components:
            self.MassFraction[c] = float('nan')
        # phase parameters
        self.Phase = {}.copy()
        for p in self.__Phases:
            self.Phase[p] = PhaseParameter(self.__Components)
        # common transition points
        self.BoilingPressure = float('nan')
        self.SaturationPressure = float('nan')
        self.EvaporationPressure = float('nan')
            
    def __startSignyProcess(self, args):
        """
        Attempts to start the Signy process and returns it.
        Raises an exception if Signy can't be started.        
        """
        # create a list of candidates for running Signy
        candidates = []
        
        # is the VOLSUNGPATH environment variable set? if so then use that location for signy
        vpath = ''
        try:
            vpath = os.environ['VOLSUNGPATH']
            if sys.platform == 'linux':
                candidates.append(vpath + '/signy')
            else:
                candidates.append(vpath + '/Signy.exe')
        except:
            pass
        # linux: add more default candidates
        if sys.platform == 'linux':
            candidates += ['volsung.signy', 'signy']
        
        # now iterate through the candidates and return the process if we're able to start it
        for c in candidates:
            if shutil.which(c) is None:
                continue
            cmd = '"' + c + '" ' + ' '.join(args)           # use '"' to ensure white space in path are not a problem
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True, stderr=subprocess.STDOUT)
            return p
        raise FileNotFoundError("Could not launch signy; is the VOLSUNGPATH environmental variable set correctly? Current value is '%s'." % vpath)
        return None
            
    def __setTable(self, args):
        """
        Generic setter method for calling the Signy tool and reading back the results
        """
        args.append("--table %s" % self.__TableType)
        args.append("--command")

        # start the running process        
        p = self.__startSignyProcess(args)

        # collate the output from the process        
        self.__signyOutput = ""
        while p.poll() is None:
            l = p.stdout.readline().decode("utf-8").strip("\n") # This blocks until it receives a newline.
            self.__signyOutput += l + "\n"
            
        # all ok?
        if p.returncode == 0:
            self.__processSignyOutput()
            return True
        else:
            # invalidate all parameters
            self.__initParameters()
            return False
        
    def __processSignyOutput(self):
        """
        Processes the Signy output, under the assumption that it is valid
        """
        lines = self.__signyOutput.split("\n")
        process_bulk = False
        process_phase = False
        current_phase = ""
        process_transition = False
        for i in range(len(lines)):
            l = lines[i].strip()            # remove whitespace, in particular \r in windows
            # detect headers
            if l.find("Bulk Properties") == 0:
                process_bulk = True
                process_phase = False
                process_transition = False
                continue
            if l.find("Phase Properties - ") == 0:
                process_bulk = False
                process_phase = True
                current_phase = l[19:]
                process_transition = False
                continue
            if l.find("Phase Transition Information") == 0:
                process_bulk = False
                process_phase = False
                process_transition = True
                continue
            # detect data lines
            ls = l.split("=")
            if len(ls) != 2:
                continue
            if process_bulk:
                if ls[0].find('Pressure') == 0:
                    self.Pressure = float(ls[1])
                    continue
                if ls[0].find('Enthalpy') == 0:
                    self.Enthalpy = float(ls[1])
                    continue
                if ls[0].find('Temperature') == 0:
                    self.Temperature = float(ls[1])
                    continue
                if ls[0].find('Density') == 0:
                    self.Density = float(ls[1])
                    continue
                if ls[0].find('Surface Tension') == 0:
                    self.SurfaceTension = float(ls[1])
                    continue
                for c in self.__Components:
                    if ls[0].find('X%s' % c) == 0:
                        self.MassFraction[c] = float(ls[1])
                        continue
            if process_phase:
                if ls[0].find('Spec. Fraction') == 0:
                    self.Phase[current_phase].SpecificFraction = float(ls[1])
                    continue
                if ls[0].find('Saturation') == 0:
                    self.Phase[current_phase].Saturation = float(ls[1])
                    continue
                if ls[0].find('Enthalpy') == 0:
                    self.Phase[current_phase].Enthalpy = float(ls[1])
                    continue
                if ls[0].find('Density') == 0:
                    self.Phase[current_phase].Density = float(ls[1])
                    continue
                if ls[0].find('Viscosity') == 0:
                    self.Phase[current_phase].Viscosity = float(ls[1])
                    continue
                for c in self.__Components:
                    if ls[0].find('X%s' % c) == 0:
                        self.Phase[current_phase].MassFraction[c] = float(ls[1])
                        continue
            if process_transition:
                # find the common transitions
                if ls[0].find('Boiling Pressure') == 0:
                    self.BoilingPressure = float(ls[1])
                    continue
                if ls[0].find('Saturation Pressure') == 0:
                    self.SaturationPressure = float(ls[1])
                    continue
                if ls[0].find('Evaporation Pressure') == 0:
                    self.EvaporationPressure = float(ls[1])
                    continue
                # subclasses can add more transitions
                self._processFurtherTransitions(ls[0], ls[1])
                
    def _processFurtherTransitions(self, marker, value_str):
        """
        Subclasses can process additional phase transitions by overriding this method.
        """
        return
       
        
    def output(self):
        """
        Returns the output from the last call to Signy.
        This can be helpful for debugging errors.
        """
        return self.__signyOutput
            
    def set_phX(self, p, h, X = {}):
        """
        Set thermodynamic properties using pressure, enthalpy and mass fractions
        Set component mass fractions like X = {"XAir" : 0.1, "XNaCl" : 0.01}
        """
        args = ["--setter phX"]
        args.append("--pressure {}".format(p))
        args.append("--enthalpy {}".format(h))
        for x in X:
            args.append("--{0} {1}".format(x, X[x]))
        return self.__setTable(args)
        
    def set_pTX(self, p, T, X = {}):
        """
        Set thermodynamic properties using pressure, temperature and mass fractions
        Set component mass fractions like X = {"XAir" : 0.1, "XNaCl" : 0.01}
        """
        args = ["--setter pTX"]
        args.append("--pressure {}".format(p))
        args.append("--temperature {}".format(T))
        for x in X:
            args.append("--{0} {1}".format(x, X[x]))
        return self.__setTable(args)
        
    def set_pxX(self, p, q, X = {}):
        """
        Set thermodynamic properties using pressure, quality and mass fractions
        Set component mass fractions like X = {"XAir" : 0.1, "XNaCl" : 0.01}
        """
        args = ["--setter pxX"]
        args.append("--pressure {}".format(p))
        args.append("--quality {}".format(q))
        for x in X:
            args.append("--{0} {1}".format(x, X[x]))
        return self.__setTable(args)
        
    def set_TxX(self, T, q, X = {}):
        """
        Set thermodynamic properties using temperature, quality and mass fractions
        Set component mass fractions like X = {"XAir" : 0.1, "XNaCl" : 0.01}
        """
        args = ["--setter TxX"]
        args.append("--temperature {}".format(T))
        args.append("--quality {}".format(q))
        for x in X:
            args.append("--{0} {1}".format(x, X[x]))
        return self.__setTable(args)

class TT_Salt_NCG(ThermodynamicTable):
    """
    Abstract base class for tables containing salt and NCG
    """
    def __init__(self, table_type, salt, ncg):
        super().__init__(table_type, ["H2O", salt, ncg], ["liquid", "gas", "solid"])
        self.SaltSolubility = float('nan')

    def _processFurtherTransitions(self, marker, value_str):
        super()._processFurtherTransitions(marker, value_str)
        if marker.find('Salt Solubility') == 0:
            self.SaltSolubility = float(value_str)

# ----------------------------------------------------------------------------------------
#
# Available thermodynamic tables
#
# ----------------------------------------------------------------------------------------
        
        
class TT_IAPWSIF97(ThermodynamicTable):
    """
    Thermodynamic table for pure H2O
    """
    def __init__(self):
        super().__init__("TT_IAPWSIF97", ["H2O"], ["liquid", "gas"])

class TT_CO2(ThermodynamicTable):
    """
    Thermodynamic table for H2O + CO2
    """
    def __init__(self):
        super().__init__("TT_CO2", ["H2O", "CO2"], ["liquid", "gas"])

class TT_Air(ThermodynamicTable):
    """
    Thermodynamic table for H2O + Air
    """
    def __init__(self):
        super().__init__("TT_Air", ["H2O", "Air"], ["liquid", "gas"])

class TT_NaCl(ThermodynamicTable):
    """
    Thermodynamic table for H2O + NaCl
    """
    def __init__(self):
        super().__init__("TT_NaCl", ["H2O", "NaCl"], ["liquid", "gas", "solid"])
        self.SaltSolubility = float('nan')

    def _processFurtherTransitions(self, marker, value_str):
        super()._processFurtherTransitions(marker, value_str)
        if marker.find('Salt Solubility') == 0:
            self.SaltSolubility = float(value_str)

class TT_NaCl_CO2(TT_Salt_NCG):
    """
    Thermodynamic table for H2O + NaCl + CO2
    """
    def __init__(self):
        super().__init__("TT_NaCl_CO2", "NaCl", "CO2")

class TT_NaCl_Air(TT_Salt_NCG):
    """
    Thermodynamic table for H2O + NaCl + Air
    """
    def __init__(self):
        super().__init__("TT_NaCl_Air", "NaCl", "Air")


#
# code for testing purposes
#
if __name__ == "__main__":
    table = TT_NaCl_CO2()
    print(table.set_phX(1.23e5, 34e3, X = {"XCO2" : 0.04, "XNaCl" : 0.01}))
    print(table.Phase['gas'].Density)
    print(table.set_pTX(1.01325e5, 373.15, X = {"XCO2" : 0.04, "XNaCl" : 0.01}))
    print(table.Phase['gas'].Density)
    print(table.set_pxX(1.01325e5, 0.5, X = {"XCO2" : 0.04, "XNaCl" : 0.01}))
    print(table.Phase['gas'].Density)
    print(table.set_TxX(373.15, 0.5, X = {"XCO2" : 0.04, "XNaCl" : 0.01}))
    print(table.Phase['gas'].Density)
