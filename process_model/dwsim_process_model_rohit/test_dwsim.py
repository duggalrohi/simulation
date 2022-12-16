import os
from os.path import expanduser
import pythoncom
pythoncom.CoInitialize()

import clr

from System.IO import Directory, Path, File
from System import String, Environment

dwsimpath = os.path.expanduser('~\\AppData\\Local\\DWSIM8\\') #"C:\\Users\\rohit\\AppData\\Local\\DWSIM8\\"

clr.AddReference(dwsimpath + "CapeOpen.dll")
clr.AddReference(dwsimpath + "DWSIM.Automation.dll")
clr.AddReference(dwsimpath + "DWSIM.Interfaces.dll")
clr.AddReference(dwsimpath + "DWSIM.GlobalSettings.dll")
clr.AddReference(dwsimpath + "DWSIM.SharedClasses.dll")
clr.AddReference(dwsimpath + "DWSIM.Thermodynamics.dll")
clr.AddReference(dwsimpath + "DWSIM.UnitOperations.dll")
clr.AddReference(dwsimpath + "DWSIM.Inspector.dll")
clr.AddReference(dwsimpath + "System.Buffers.dll")

from DWSIM.Interfaces.Enums.GraphicObjects import ObjectType
from DWSIM.Thermodynamics import Streams, PropertyPackages
from DWSIM.UnitOperations import UnitOperations
from DWSIM.Automation import Automation3
from DWSIM.GlobalSettings import Settings

Directory.SetCurrentDirectory(dwsimpath)

# create automation manager

interf = Automation3()

sim = interf.CreateFlowsheet()

# add water

water = sim.AvailableCompounds["Water"]

sim.SelectedCompounds.Add(water.Name, water)

# create and connect objects

m1 = sim.AddObject(ObjectType.MaterialStream, 50, 50, "inlet")
m2 = sim.AddObject(ObjectType.MaterialStream, 150, 50, "outlet")
e1 = sim.AddObject(ObjectType.EnergyStream, 100, 50, "power")
h1 = sim.AddObject(ObjectType.Heater, 100, 50, "heater")
h1 = h1.GetAsObject()

sim.ConnectObjects(m1.GraphicObject, h1.GraphicObject, -1, -1)
sim.ConnectObjects(h1.GraphicObject, m2.GraphicObject, -1, -1)
sim.ConnectObjects(e1.GraphicObject, h1.GraphicObject, -1, -1)

sim.AutoLayout()

# steam tables property package

stables = PropertyPackages.SteamTablesPropertyPackage()

sim.AddPropertyPackage(stables)

# set inlet stream temperature
# default properties: T = 298.15 K, P = 101325 Pa, Mass Flow = 1 kg/s
m1 = m1.GetAsObject()
m1.SetTemperature(300.0) # K
m1.SetMassFlow(100.0) # kg/s

# set heater outlet temperature

h1.CalcMode = UnitOperations.Heater.CalculationMode.OutletTemperature
h1.OutletTemperature = 400 # K

# request a calculation

Settings.SolverMode = 0

errors = interf.CalculateFlowsheet2(sim)

print(String.Format("Heater Heat Load: {0} kW", h1.DeltaQ))

# save file

fileNameToSave = Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.Desktop), "heatersample.dwxmz")

interf.SaveFlowsheet(sim, fileNameToSave, True)

# save the pfd to an image and display it

clr.AddReference(dwsimpath + "SkiaSharp.dll")
clr.AddReference("System.Drawing")

from SkiaSharp import SKBitmap, SKImage, SKCanvas, SKEncodedImageFormat
from System.IO import MemoryStream
from System.Drawing import Image
from System.Drawing.Imaging import ImageFormat

PFDSurface = sim.GetSurface()

bmp = SKBitmap(1024, 768)
canvas = SKCanvas(bmp)
canvas.Scale(1.0)
PFDSurface.UpdateCanvas(canvas)
d = SKImage.FromBitmap(bmp).Encode(SKEncodedImageFormat.Png, 100)
str = MemoryStream()
d.SaveTo(str)
image = Image.FromStream(str)
imgPath = Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.Desktop), "pfd.png")
image.Save(imgPath, ImageFormat.Png)
str.Dispose()
canvas.Dispose()
bmp.Dispose()

from PIL import Image

im = Image.open(imgPath)
im.show()



# ####-----------------Code 2---------------------####

# import clr
# clr.AddReference('DWSIM.Interfaces')
 
# from DWSIM import Interfaces
 
# cooler = Flowsheet.AddObject(Interfaces.Enums.GraphicObjects.ObjectType.Cooler, 100, 100, 'COOLER-001')
# heat_out = Flowsheet.AddObject(Interfaces.Enums.GraphicObjects.ObjectType.EnergyStream, 130, 150, 'HEAT_OUT')
# inlet = Flowsheet.AddObject(Interfaces.Enums.GraphicObjects.ObjectType.MaterialStream, 50, 100, 'INLET')
# outlet = Flowsheet.AddObject(Interfaces.Enums.GraphicObjects.ObjectType.MaterialStream, 150, 100, 'OUTLET')
 
# cooler.GraphicObject.CreateConnectors(1, 1)
# inlet.GraphicObject.CreateConnectors(1, 1)
# outlet.GraphicObject.CreateConnectors(1, 1)
# heat_out.GraphicObject.CreateConnectors(1, 1)
 
# Flowsheet.ConnectObjects(inlet.GraphicObject, cooler.GraphicObject, 0, 0)
# Flowsheet.ConnectObjects(cooler.GraphicObject, outlet.GraphicObject, 0, 0)
# Flowsheet.ConnectObjects(cooler.GraphicObject, heat_out.GraphicObject, 0, 0)
 
# # get inlet properties
# inlet_properties = inlet.GetPhase('Overall').Properties
 
# inlet_properties.temperature = 400 # K
# inlet_properties.pressure = 1000000 # Pa
# inlet_properties.massflow = 30 # kg/s
 
# # the following will define all compound mole fractions to the same value so the sum is equal to 1
# inlet.EqualizeOverallComposition()
 
# # set the cooler's outlet temperature to 300 K
# # http://dwsim.inforside.com.br/api_help57/html/T_DWSIM_UnitOperations_UnitOperations_Cooler.htm
# cooler.OutletTemperature = 300
 
# # set the cooler's calculation mode to 'outlet temperature'
# # http://dwsim.inforside.com.br/api_help57/html/T_DWSIM_UnitOperations_UnitOperations_Cooler_CalculationMode.htm
 
# clr.AddReference('DWSIM.UnitOperations')
# from DWSIM import UnitOperations
# cooler.CalcMode = UnitOperations.UnitOperations.Cooler.CalculationMode.OutletTemperature
 
# #calculate the flowsheet
# Flowsheet.RequestCalculation(None, False)
 
# #get the outlet stream temperature and cooler's temperature decrease
# deltat = cooler.DeltaT
# heat_flow = heat_out.EnergyFlow
 
# print('Cooler Temperature Drop (K):'+ str(deltat))
# print('Heat Flow (kW): ' + str(heat_flow))