import h5py as h
import matplotlib.pyplot as plt
import sys
import numpy as np

def com(filename1,filename2,ele,property=None):
    minc = h.File(filename1)
    non_minc = h.File(filename2)
    t_minc=minc['time'][()]
    t_non_minc=non_minc['time'][()]
    if property is None:
        injTn=non_minc['cell_fields/fluid_temperature'][:,0]
        injT=minc['cell_fields/fluid_temperature'][:,0]
        injPn=non_minc['cell_fields/fluid_pressure'][:,0]
        injP=minc['cell_fields/fluid_pressure'][:,0]
        prodTn=non_minc['cell_fields/fluid_temperature'][:,-1]
        prodT=minc['cell_fields/fluid_temperature'][:,14]
        prodPn=non_minc['cell_fields/fluid_pressure'][:,-1]
        prodP=minc['cell_fields/fluid_pressure'][:,14]
        fig = plt.figure(figsize=(12,6))
        plt.subplot(221)
        plt.plot(t_minc*1.157407407407407e-5,injTn,'-', label='injection_single_porosity_T')
        plt.xlabel('time, days')
        plt.ylabel('cell_fields/fluid_temperature, ($^\circ$C)')
        plt.plot(t_non_minc*1.157407407407407e-5,injT,'',label='injection_MINC_T')
        plt.legend()
        plt.subplot(222)
        plt.plot(t_minc*1.157407407407407e-5,injPn*1e-5,'-', label='injection_single_porosity_P')
        plt.xlabel('time, days')
        plt.ylabel('cell_fields/fluid_pressure, bar')
        plt.plot(t_non_minc*1.157407407407407e-5,injP*1e-5,'',label='injection_MINC_P')
        plt.legend()
        plt.subplot(223)
        plt.plot(t_minc*1.157407407407407e-5,prodTn,'-', label='production_single_porosity_T')
        plt.xlabel('time, days')
        plt.ylabel('cell_fields/fluid_temperature, ($^\circ$C)')
        plt.plot(t_non_minc*1.157407407407407e-5,prodT,'',label='production_MINC_T')
        plt.legend()
        plt.subplot(224)
        plt.plot(t_minc*1.157407407407407e-5,prodPn*1e-5,'-', label='production_single_porosity_P')
        plt.xlabel('time, days')
        plt.ylabel('cell_fields/fluid_pressure, bar')
        plt.plot(t_non_minc*1.157407407407407e-5,prodP*1e-5,'',label='production_MINC_P')
        plt.legend()
    else:
        if sys.argv[3] =="injection":
            T_non_minc = non_minc[property][:,0]
            T_minc=minc[property][:,0]
        else:
            T_non_minc=non_minc[property][:,ele]
            n1=np.int(len(non_minc[property][ele,:]))
            prod=n1-1
            T_minc=minc[property][:,prod]
        plt.plot(t_minc*1.157407407407407e-5,T_minc,'-', label='MINC')
        plt.xlabel('time, days')
        plt.ylabel(property+' [:,'+sys.argv[3]+']')
        plt.plot(t_non_minc*1.157407407407407e-5,T_non_minc,'',label='Single porosity')
        plt.legend()
    plt.show()

if __name__=="__main__":
    filename1=sys.argv[1]
    filename2=sys.argv[2]
    if len(sys.argv)>3:
        property="cell_fields/fluid_"+sys.argv[4]
        if sys.argv[3]=="injection":
            ele=sys.argv[3]
        else:
            ele=np.int(sys.argv[3])
        com(filename1,filename2,ele,property)
    else:
        com(filename1,filename2,ele=None)