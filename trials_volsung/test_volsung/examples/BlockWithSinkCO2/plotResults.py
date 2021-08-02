#!/usr/bin/python3

"""

Plot the results from the single block with sink, CO2

"""

from volsung.volsungmodel import *
from t2listing import *
from matplotlib import pyplot as plt
import numpy as np

model = VolsungModel("./Brynhild/Results.sigurd", "./Brynhild/SingleBlockWithSinkCO2.brynhild")
t2l = t2listing("./T2/TOUGH2.out")

# extract transient data
# volsung
times_v = model.reservoir.zoneTimes()
T_v = np.transpose(model.reservoir.history("/reservoir/Elements/Temperature"))[0] - 273.15
SG_v = np.transpose(model.reservoir.history("/reservoir/Elements/Saturation (gas)"))[0]
XCO2_liq_v = np.transpose(model.reservoir.history("/reservoir/Elements/XCO2 (liquid)"))[0]
XCO2_gas_v = np.transpose(model.reservoir.history("/reservoir/Elements/XCO2 (gas)"))[0]

# TOUGH2
times_t2, T_t2 = t2l.history([('e', '  a 1', 'T')])
times_t2, SG_t2 = t2l.history([('e', '  a 1', 'SG')])
times_t2, XCO2_liq_t2 = t2l.history([('e', '  a 1', 'XCO2(liq)')])
times_t2, XCO2_gas_t2 = t2l.history([('e', '  a 1', 'XCO2(gas)')])

# plot T, SG in a single plot
plt.figure()
ax1 = plt.subplot(1,1,1)
ax2 = ax1.twinx()
h2, = ax1.plot(times_t2, T_t2, "dr", markersize=6)
h1, = ax1.plot(times_v, T_v, "-b", linewidth=2)
h4, = ax2.plot(times_t2, SG_t2, "Dr", markersize=6)
h3, = ax2.plot(times_v, SG_v, "--b", linewidth=2)
plt.title("Single Block with Sink, $CO_2$", fontweight='bold')
ax1.set_xlabel("t [s]")
ax1.set_ylabel("T [$^\circ C$]")
ax2.set_ylabel("SG")
plt.legend([h1, h2, h3, h4], ["Volsung T", "TOUGH2 T", "Volsung SG", "TOUGH2 SG"], loc = "center left")
plt.savefig("BlockWithSink-T-SG.png", dpi=900)

# plot XCO2s in single plot
plt.figure()
ax1 = plt.subplot(1,1,1)
ax2 = ax1.twinx()
h2, = ax1.plot(times_t2, XCO2_liq_t2, "dr", markersize=6)
h1, = ax1.plot(times_v, XCO2_liq_v, "-b", linewidth=2)
h4, = ax2.plot(times_t2, XCO2_gas_t2, "Dr", markersize=6)
h3, = ax2.plot(times_v, XCO2_gas_v, "--b", linewidth=2)
plt.title("Single Block with Sink, $CO_2$", fontweight='bold')
ax1.set_xlabel("t [s]")
ax1.set_ylabel("$XCO_2 (liq)$")
ax2.set_ylabel("$XCO_2 (gas)$")
plt.legend([h1, h2, h3, h4], ["Volsung $XCO_2$ (liq)", "TOUGH2 $XCO_2$ (liq)", "Volsung $XCO_2$ (gas)", "TOUGH2 $XCO_2$ (gas)"])
plt.savefig("BlockWithSink-XCO2.png", dpi=900)
