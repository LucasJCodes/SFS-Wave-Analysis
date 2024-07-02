#!/usr/bin/env python3

#SBATCH -J var_test.py
#SBATCH -o var_test_out
#SBATCH -e var_test_error
#SBATCH -q debug
#SBATCH -A marine-cpu
#SBATCH --ntasks=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=0
#SBATCH -t 05:00

############################
#Author: Lucas Jones, Hollings Scholar Intern at NOAA EMC
#Date: 7/2/24
############################

import xarray as xr
import numpy as np

def main():

    nwpath = "/work2/noaa/marine/ljones/SFS-Wave-Analysis/wave_analysis/ensembles/SST1997now_ensemble.nc"
    wpath = "/work2/noaa/marine/ljones/SFS-Wave-Analysis/wave_analysis/ensembles/SST1997w_ensemble.nc"

    #read in data
    waves_in = xr.open_mfdataset(wpath)["WTMP_surface"] - 273.15  #convert to deg C
    waves = waves_in.sel(time = (waves_in.time.dt.hour == 12))  #only the 12z times

    nowaves_in = xr.open_mfdataset(nwpath)["WTMP_surface"] - 273.15 #convert to deg C
    nowaves = nowaves_in.sel(time = (nowaves_in.time.dt.hour == 12)) #only the 12z times

    #calculate the difference between waves and no waves
    diff = waves - nowaves

    print("waves ", np.var(waves).values)
    print("no waves ", np.var(nowaves).values)

if __name__ == "__main__":
    main()
