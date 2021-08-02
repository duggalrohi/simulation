ptf #
<!DOCTYPE Brynhild>
<root volsung-version="1.7.0">
 <brynhildmainwindow class="AslaugMainWindow"><thermodynamictable class="TT_IAPWSIF97"></thermodynamictable>
  <simulator>Sigurd</simulator>
  <equationofstate>EOS_IAPWSIF97</equationofstate>
  <numberofaqueoustracers>0</numberofaqueoustracers>
  <hdf5reservoirviewer class="HDF5ReservoirViewer"><minclayer>0</minclayer>
   <cellarrayname>Pressure</cellarrayname>
   <projectionazimuth>0</projectionazimuth>
   <projectioninclination>0</projectioninclination>
   <cellopacity>1</cellopacity>
   <cellstateselector>0</cellstateselector>
   <cellcontoursvisible>0</cellcontoursvisible>
   <cellcontoursarrayname></cellcontoursarrayname>
   <cellcontourscolourtype>0</cellcontourscolourtype>
   <ncellcontours>10</ncellcontours>
   <cellcontoursopacity>1</cellcontoursopacity>
   <cellcontourscustomcolourarrayname></cellcontourscustomcolourarrayname>
   <cellvectorsvisible>0</cellvectorsvisible>
   <cellvectorsarrayname></cellvectorsarrayname>
   <cellvectorscustomcolourarrayname></cellvectorscustomcolourarrayname>
   <cellvectorsrelativethreshold>0.90000000000000002</cellvectorsrelativethreshold>
   <cellvectorsrelativescale>0.10000000000000001</cellvectorsrelativescale>
   <cellvectorscolourtype>0</cellvectorscolourtype>
   <provisionalgridvisible>1</provisionalgridvisible>
   <provisionalwelltracksvisible>1</provisionalwelltracksvisible>
   <wellboreradiusfactor>1</wellboreradiusfactor>
   <wellborecolourtype>0</wellborecolourtype>
   <colorlookuptabledb class="ColorLookupTableDB"><colorlookuptabledata class="ColorLookupTableData" name="Pressure"><quantity>9</quantity>
     <lowervaluecolor><r>0</r>
      <g>0</g>
      <b>255</b>
      <alpha>255</alpha>
     </lowervaluecolor>
     <uppervaluecolor><r>255</r>
      <g>0</g>
      <b>0</b>
      <alpha>255</alpha>
     </uppervaluecolor>
     <ncolors>256</ncolors>
     <lowervalue>0</lowervalue>
     <uppervalue>1</uppervalue>
     <usevaluerange>0</usevaluerange>
    </colorlookuptabledata>
    <colorlookuptabledata class="ColorLookupTableData" name="Temperature"><quantity>4</quantity>
     <lowervaluecolor><r>0</r>
      <g>0</g>
      <b>255</b>
      <alpha>255</alpha>
     </lowervaluecolor>
     <uppervaluecolor><r>255</r>
      <g>0</g>
      <b>0</b>
      <alpha>255</alpha>
     </uppervaluecolor>
     <ncolors>256</ncolors>
     <lowervalue>0</lowervalue>
     <uppervalue>1</uppervalue>
     <usevaluerange>0</usevaluerange>
    </colorlookuptabledata>
   </colorlookuptabledb>
  </hdf5reservoirviewer>
  <simulationrunwidget><isrunningremote>0</isrunningremote>
  </simulationrunwidget>
  <flownetwork class="FlowNetwork"><pressuretolerance>1000</pressuretolerance>
   <flownetworkobjects></flownetworkobjects>
   <flownetworkoptimizer class="FNO_TPSAAN"><generateoutput>0</generateoutput>
    <nthreads>32</nthreads>
    <maxiter>10000</maxiter>
    <swapinterval>200</swapinterval>
   </flownetworkoptimizer>
   <ambientconditions class="AmbientConditions"><annualcycle>1</annualcycle>
    <temperaturetable></temperaturetable>
   </ambientconditions>
  </flownetwork>
  <gridcontainer class="GridContainer"><watch>0</watch>
   <gridfilename>grid.vgrid</gridfilename>
   <gridgenerator class="GG_Tartan"><z>0,10,20,30,40,50,60,70,80,90,100,110,120,130,140,150,160,170,180,190,200</z>
    <azimuth>0</azimuth>
    <basepoint>0,0,0</basepoint>
    <useundulatedsurface>0</useundulatedsurface>
    <surfaceglobalcoordinates>1</surfaceglobalcoordinates>
    <pointlist3d class="PointList3D"><x></x>
     <y></y>
     <z></z>
    </pointlist3d>
    <x>0,10</x>
    <y>0,10</y>
   </gridgenerator>
  </gridcontainer>
  <brynhildsimulatorsettingscontainer class="BrynhildSimulatorSettingsContainer"><outputfilename>Results.sigurd</outputfilename>
   <usegpu>0</usegpu>
   <gpuid>0</gpuid>
   <loglevel>1</loglevel>
   <uselogport>0</uselogport>
   <logport>2050</logport>
   <usebacktracking>1</usebacktracking>
   <translator>None</translator>
   <initialstatesettingscontainer class="InitialStateSettingsContainer"><loadfromfile>0</loadfromfile>
    <initialstatefilename></initialstatefilename>
    <porosityfromfile>0</porosityfromfile>
    <saveinterval>10</saveinterval>
    <statesavefilename>SAVE.fafnir</statesavefilename>
   </initialstatesettingscontainer>
   <outputlinearsystem>0</outputlinearsystem>
   <matrixequilibratorpretty>Matrix On</matrixequilibratorpretty>
   <residual class="Residual"><reltol>1.0000000000000001e-05</reltol>
    <abstol>1</abstol>
    <absmaxtol>0.0001</absmaxtol>
   </residual>
   <connections class="Connections"><permweight>0</permweight>
    <mobweight>0</mobweight>
    <gravweight>0</gravweight>
    <conductivityinterpolation>0</conductivityinterpolation>
    <cellareaweight>0</cellareaweight>
    <cellconnectivitylayer0>0</cellconnectivitylayer0>
    <cellconnectivitylayer1>3</cellconnectivitylayer1>
    <cellconnectivitylayerother>3</cellconnectivitylayerother>
   </connections>
   <linearsolversettingscontainer class="LinearSolverSettingsContainer"><solvertype>BiCGStab</solvertype>
    <reltol>9.9999999999999995e-07</reltol>
    <abstol>0</abstol>
    <relmaxiter>0.10000000000000001</relmaxiter>
    <ginsburgfactor>0.20000000000000001</ginsburgfactor>
    <backupsolvertype>None</backupsolvertype>
    <backuprelmaxiter>0.10000000000000001</backuprelmaxiter>
   </linearsolversettingscontainer>
   <steadystatesettingscontainer class="SteadyStateSettingsContainer"><usesteadystatedetection>0</usesteadystatedetection>
    <majorcomponentcriterion>1e-14</majorcomponentcriterion>
    <minorcomponentcriterion>9.9999999999999998e-13</minorcomponentcriterion>
    <energycomponentcriterion>1e-14</energycomponentcriterion>
   </steadystatesettingscontainer>
  </brynhildsimulatorsettingscontainer>
  <propcontainer class="PropContainer"></propcontainer>
  <timestepcontrol class="TimeStepControl"><starttime>0</starttime>
   <endtime>1577790000</endtime>
   <maxnumbersteps>9999</maxnumbersteps>
   <starttimestep>1</starttimestep>
   <maxtimestep>100000000000</maxtimestep>
   <mintimestep>0.001</mintimestep>
   <expansionfactor>2</expansionfactor>
   <reductionfactor>0.25</reductionfactor>
   <specialtimes></specialtimes>
   <printtimes></printtimes>
   <printinitialstate>1</printinitialstate>
   <printnsteps>99999</printnsteps>
   <printonwarnings>1</printonwarnings>
   <printonerrors>1</printonerrors>
   <nrfastconverge>3</nrfastconverge>
   <calibrationtime>1e+30</calibrationtime>
   <maxcalibrationtimestep>1</maxcalibrationtimestep>
   <scenariotime>2e+30</scenariotime>
   <maxscenariotimestep>1</maxscenariotimestep>
  </timestepcontrol>
  <lithologydb class="LithologyDB"><relativepermeabilities><relativepermeability class="RP_Grant" name="default"><slresidual>0.29999999999999999</slresidual>
     <sgresidual>0.050000000000000003</sgresidual>
    </relativepermeability>
   </relativepermeabilities>
   <capillarypressures><capillarypressure class="CP_None" name="default"></capillarypressure>
   </capillarypressures>
   <permeabilitymodifications><PermeabilityModification class="PM_None" name="default"></PermeabilityModification>
   </permeabilitymodifications>
   <lithologyunits><lithologyunit class="LithologyUnit" name="default"><elementstate>0</elementstate>
     <type>0</type>
     <fracturespacings>100,100,100</fracturespacings>
     <color><r>238</r>
      <g>238</g>
      <b>236</b>
      <alpha>255</alpha>
     </color>
     <isinitialized>1</isinitialized>
     <layers nlayers="1"><lithologyunit class="LithologyUnitLayer" name="Fracture" index="0"><volumefraction>1</volumefraction>
       <initialstate><useouterinitialstate>0</useouterinitialstate>
        <usehydrostaticcorrection>0</usehydrostaticcorrection>
        <hydrostaticbaseelevation>0</hydrostaticbaseelevation>
        <initialstate><thermodynamictable class="TT_IAPWSIF97"><p>101325</p>
          <h>80000</h>
          <xh2o>1</xh2o>
         </thermodynamictable>
        </initialstate>
       </initialstate>
       <useouterrockproperties>0</useouterrockproperties>
       <rockproperties class="RockProperties" name="default@Fracture"><density>2600</density>
        <porosity>0.050000000000000003</porosity>
        <specificheat>1000</specificheat>
        <wetconductivity>2</wetconductivity>
        <dryconductivity>2</dryconductivity>
        <compressibility>0</compressibility>
        <expansivity>0</expansivity>
        <permeability><impermeable>0</impermeable>
         <mainaxis>1.0000000000000001e-15,1.0000000000000001e-15,1e-13</mainaxis>
         <rotationangles>0,0,0</rotationangles>
        </permeability>
        <relativepermeability>default</relativepermeability>
        <capillarypressure>default</capillarypressure>
        <permeabilitymodification>default</permeabilitymodification>
       </rockproperties>
      </lithologyunit>
     </layers>
    </lithologyunit>
   </lithologyunits>
  </lithologydb>
  <geologymodel class="LayerGeologyModel"><GeologyModelBarriers size="0"></GeologyModelBarriers>
   <defaultunit>default</defaultunit>
   <geologymodellayers size="0"></geologymodellayers>
   <GeologyModelLayers size="0"></GeologyModelLayers>
  </geologymodel>
  <boundaryconditioncontainer class="BoundaryConditionContainer"><boundarycondition class="BCES_Atmosphere" id="0"><enabled>1</enabled>
    <name>Atmosphere</name>
    <color><r>255</r>
     <g>255</g>
     <b>255</b>
     <alpha>255</alpha>
    </color>
    <actorvisible>1</actorvisible>
    <actoropacity>1</actoropacity>
    <initialstate><thermodynamictable class="TT_IAPWSIF97"><p>5000000</p>
      <h>88612.832354742073</h>
      <xh2o>1</xh2o>
     </thermodynamictable>
    </initialstate>
    <emissivity>0.61199999999999999</emissivity>
   </boundarycondition>
   <boundarycondition class="BCS_GridBottom" id="1"><enabled>1</enabled>
    <name>Bottom Source</name>
    <color><r>255</r>
     <g>255</g>
     <b>255</b>
     <alpha>255</alpha>
    </color>
    <actorvisible>1</actorvisible>
    <actoropacity>1</actoropacity>
    <ratesareabsolute>1</ratesareabsolute>
    <flowratetable class="FlowRateTable"><tablerow><time>-1e+30</time>
      <flowrate><p>0</p>
       <h>#ENTHALPY                  #</h>
       <w>1</w>
       <q>0</q>
       <xh2o>1</xh2o>
      </flowrate>
     </tablerow>
    </flowratetable>
   </boundarycondition>
  </boundaryconditioncontainer>
  <extramodulecontainer class="ExtraModuleContainer"></extramodulecontainer>
 </brynhildmainwindow>
</root>
