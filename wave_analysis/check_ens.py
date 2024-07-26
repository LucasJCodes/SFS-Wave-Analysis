#!/usr/bin/env python3

#SBATCH -J check_ens.py
#SBATCH -o check_ens_out
#SBATCH -e check_ens_error
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

#This is a test program that exists soley to print out various calculated ensembles to check their dimensions are right.
#An ensemble dashboard of sorts.

import sys
sys.path.append("/work2/noaa/marine/ljones/SFS-Wave-Analysis/wave_analysis/")

from metplot import data_range
import cartopy.crs as ccrs
from metplot import cont_levels
import matplotlib.pyplot as plt
import xarray as xr

def main():

    VARIABLE = "850Height"

    print(VARIABLE + " waves 1997")
    waves1997 = xr.open_mfdataset("/work2/noaa/marine/ljones/SFS-Wave-Analysis/wave_analysis/ensembles/" + VARIABLE + "1997w_ensemble.nc")
    print(waves1997)

    print(VARIABLE + " no waves 1997")
    nowaves1997 = xr.open_mfdataset("/work2/noaa/marine/ljones/SFS-Wave-Analysis/wave_analysis/ensembles/" + VARIABLE + "1997now_ensemble.nc")
    print(nowaves1997)

    print(VARIABLE + " waves 2015")
    waves2015 = xr.open_mfdataset("/work2/noaa/marine/ljones/SFS-Wave-Analysis/wave_analysis/ensembles/" + VARIABLE + "2015w_ensemble.nc")
    print(waves2015)

    print(VARIABLE + " no waves 2015")
    nowaves2015 = xr.open_mfdataset("/work2/noaa/marine/ljones/SFS-Wave-Analysis/wave_analysis/ensembles/" + VARIABLE + "2015now_ensemble.nc")
    print(nowaves2015)

    print(VARIABLE + " waves 2020")
    waves2020 = xr.open_mfdataset("/work2/noaa/marine/ljones/SFS-Wave-Analysis/wave_analysis/ensembles/" + VARIABLE + "2020w_ensemble.nc")
    print(waves2020)

    print(VARIABLE + " no waves 2020")
    nowaves2020 = xr.open_mfdataset("/work2/noaa/marine/ljones/SFS-Wave-Analysis/wave_analysis/ensembles/" + VARIABLE + "2020now_ensemble.nc")
    print(nowaves2020)

if __name__ == "__main__":
    main()
