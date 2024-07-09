#!/usr/bin/env python3

#SBATCH -J ostia_weekly.py
#SBATCH -o ostia_weekly_out
#SBATCH -e ostia_weekly_error
#SBATCH -q debug
#SBATCH -A marine-cpu
#SBATCH --ntasks=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=0
#SBATCH -t 05:00

############################
#Author: Lucas Jones, Hollings Scholar Intern at NOAA EMC
#Date: 7/8/24
############################

#This program graphs ensemble mean wave - no wave differences and differences between the OSTIA truth data set and waves/no waves
#in weekly segments

import sys
sys.path.append("/work2/noaa/marine/ljones/SFS-Wave-Analysis/wave_analysis/")

from metplot import data_range
import cartopy.crs as ccrs
from metplot import cont_levels
import datetime as dt
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import xarray as xr
import xesmf as xe

def main():

#constants holding the number of rows and columns in the final figure (used outside figure creation)
    NROWS = 3
    NCOLS = 4

    ostia_path = "/work2/noaa/marine/jmeixner/ReferenceData/sst_OSTIA/1p00/daily/sst_OSTIA.20151*.1p00.nc" 
    nowave_path = "/work2/noaa/marine/ljones/SFS-Wave-Analysis/wave_analysis/ensembles/precip1997now_ensemble.nc"
    wave_path = "/work2/noaa/marine/ljones/SFS-Wave-Analysis/wave_analysis/ensembles/precip1997w_ensemble.nc"

    #read the data in
    ostia_in = xr.open_mfdataset(ostia_path).sel(time = slice("2015-11-01", "2015-11-30"))  #cut it down to the same time length as the relevant model data
    wave_in = xr.open_mfdataset(wave_path).rename({"yh": "lat", "xh": "lon"})
    nowave_in = xr.open_mfdataset(nowave_path).rename({"yh": "lat", "xh": "lon"})

    #subset the model data to get SSTs, convert to Celsius if necessary 
    ostia_ds = ostia_in["analysed_sst"] - 273.15 #deg C
    wave_ds = wave_in["WTMP_surface"] - 273.16 #deg C
    nowave_ds = nowave_in["WTMP_surface"] -273.15 #deg C
   
    #put cftime indexes in datetime format for comparison with OSTIA data (in datetime)
    wave_ds["time"] = wave_ds.indexes["time"].to_datetimeindex()
    nowave_ds["time"] = nowave_ds.indexes["time"].to_datetimeindex()

    #interpolate the data using xesmf
    file_weights = 'regrid_weights.nc'
    if os.path.exists(file_weights):
        regridder = xe.Regridder(ostia_ds, wave_ds, 'nearest_s2d', reuse_weights=True, filename=file_weights)
    else:
        regridder = xe.Regridder(ostia_ds, wave_ds, 'nearest_s2d', reuse_weights=False, filename=file_weights)
    ostia_interp = regridder(ostia_ds)

    #remove model outputs other than the 12z runs
    wave_hr = wave_ds.isel(time = (wave_ds.time.dt.hour == 12))
    nowave_hr = nowave_ds.isel(time = (nowave_ds.time.dt.hour == 12))

    #calculate differences for comparison plots
    wave_no = wave_hr - nowave_hr

    wave_ostia = wave_hr - ostia_interp

    nowave_ostia = nowave_hr - ostia_interp

    #calculate min and max of each difference fo use for constant color bars across the same calculation 
    wnow_min, wnow_max = data_range.data_range(wave_no)
    wnow_levels = cont_levels.cont_levles(wnow_min, wnow_max, 10)  # levels for the contour plot

    ow_min, ow_max = data_range.data_range(wave_ostia)
    ow_levels = cont_levels.cont_levels(ow_min, ow_max, 10)  #levels of the contour plot

    onow_min, onow_max = data_range.data_range(nowave_ostia)
    onow_levels = cont_levels.cont_levels(onow_min, onow_max, 10)

    #use slice() to put data into non calendar weekly subsets
    wnow1 = wave_no.sel(time = slice("2015-11-01", "2015-11-07")).mean(dim = "time")
    wnow2 = wave_no.sel(time = slice("2015-11-08", "2015-11-14")).mean(dim = "time")
    wnow3 = wave_no.sel(time = slice("2015-11-18", "2015-11-24")).mean(dim = "time")
    wnow4 = wave_no.sel(time = slice("2015-11-25", "2015-12-01")).mean(dim = "time")
    wnow_arr = [wnow1, wnow2, wnow3, wnow4]

    ow1 = wave_ostia.sel(time = slice("2015-11-01", "2015-11-07")).mean(dim = "time")
    ow2 = wave_ostia.sel(time = slice("2015-11-08", "2015-11-14")).mean(dim = "time")
    ow3 = wave_ostia.sel(time = slice("2015-11-18", "2015-11-24")).mean(dim = "time")
    ow4 = wave_ostia.sel(time = slice("2015-11-25", "2015-12-01")).mean(dim = "time")
    ow_arr = [ow1, ow2, ow3, ow4]

    onow1 = nowave_ostia.sel(time = slice("2015-11-01", "2015-11-07")).mean(dim = "time")
    onow2 = nowave_ostia.sel(time = slice("2015-11-08", "2015-11-14")).mean(dim = "time")
    onow3 = nowave_ostia.sel(time = slice("2015-11-18", "2015-11-24")).mean(dim = "time")
    onow4 = nowave_ostia.sel(time = slice("2015-11-25", "2015-12-01")).mean(dim = "time")
    onow_arr = [onow1, onow2, onow3, onow4]

    #set up figure for the plots
    fig, axs = plt.subplots(nrows = NROWS, ncols = NCOLS, layout = "constrained", subplot_kw = {"projection": ccrs.PlateCarree()})

    #plot wave vs no wave differences
    plts_wnow = []

    for i in range(0, NCOLS):
        p = axs[0][i].contourf(wnow_arr[i].lon, wnow_arr[i].lat, wnow_arr[i], levels = wnow_levels, transform = ccrs.PlateCarree(), cmap = "seismic", vmin = wnow_min, vmax = wnow_max, extend = "both")
        axs[0][i].set_title("Week {}".format(i + 1))
        axs[0][i].coastlines()
        plts_wnow.append(p)

    fig.colorbar(plts_wnow[0], ax = axs[0, :].ravel().tolist(), location = "bottom", label = "Waves - No Waves, deg C")
    
    #plot wave vs ostia differences
    plts_ow = []

    for j in range(0, NCOLS):
        p = axs[1][j].contourf(ow_arr[j].lon, ow_arr[j].lat, ow_arr[j], levels = ow_levels, transform = ccrs.PlateCarree(), cmap = "seismic", vmin = ow_min, vmax = ow_max, extend = "both")
        axs[1][j].set_title("Week {}".format(j + 1))
        axs[1][j].coastlines()
        plts_ow.append(p)

    fig.colorbar(plts_ow[0], ax = axs[1, :].ravel().tolist(), location = "bottom", label = "Waves - OSTIA, deg C")

    #plot now wave vs ostia differences 
    plts_onow = []

    for k in range(0, NCOLS):
        p = axs[2][k].contourf(onow_arr[k].lon, onow_arr[k].lat, onow_arr[k], levels = onow_levels, transform = ccrs.PlateCarree(), cmap = "seismic", vmin = onow_min, vmax = onow_max, extend = "both")
        axs[2][k].set_title("Week {}".format(k + 1))
        axs[2][k].coastlines()
        plts_onow.append(p)

    fig.colorbar(plts_onow[0], ax = axs[2, :].ravel().tolist(), location = "bottom", label = "No Waves - OSTIA, deg C")

    fig.suptitle("GEFS SSTs w/ and w/o Waves Compared to OSTIA")

    plt.savefig("ostia_weekly.png")

if __name__ == "__main__":
    main()