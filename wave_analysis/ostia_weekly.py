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

    YEAR = "2020"
    YEAR2 = "2021"
    OSTIA = "202*"

    #constants holding the number of rows and columns in the final figure (used outside figure creation)
    NROWS = 4
    NCOLS = 3

    ostia_path = "/work2/noaa/marine/jmeixner/ReferenceData/sst_OSTIA/1p00/daily/sst_OSTIA." + OSTIA + ".1p00.nc" 
    nowave_path = "/work2/noaa/marine/ljones/SFS-Wave-Analysis/wave_analysis/ensembles/SST" + YEAR + "now_ensemble.nc"
    wave_path = "/work2/noaa/marine/ljones/SFS-Wave-Analysis/wave_analysis/ensembles/SST" +  YEAR + "w_ensemble.nc"

    #read the data in
    ostia_in = xr.open_mfdataset(ostia_path).sel(time = slice(YEAR + "-11-01", YEAR2 + "-01-30"))  #cut it down to the same time length as the relevant model data
    wave_in = xr.open_mfdataset(wave_path).rename({"latitude": "lat", "longitude": "lon"})
    nowave_in = xr.open_mfdataset(nowave_path).rename({"latitude": "lat", "longitude": "lon"})

    #subset the model data to get SSTs, convert to Celsius, and calculate daily mean for model output for comparison with ostia 
    ostia_ds = (ostia_in["analysed_sst"] - 273.15) #deg C
    wave_ds = (wave_in["WTMP_surface"] - 273.16).resample(time = "1D").mean()  #deg C
    nowave_ds = (nowave_in["WTMP_surface"] -273.15).resample(time = "1D").mean() #deg C

    print(wave_ds)
    print(nowave_ds)
    print(ostia_ds)
   
    #interpolate the data using xesmf
    file_weights = 'regrid_weights.nc'
    if os.path.exists(file_weights):
        regridder = xe.Regridder(ostia_ds, wave_ds, 'nearest_s2d', reuse_weights=True, filename=file_weights)
    else:
        regridder = xe.Regridder(ostia_ds, wave_ds, 'nearest_s2d', reuse_weights=False, filename=file_weights)
    ostia_interp = regridder(ostia_ds)

    ostia_hr = ostia_interp.resample(time = "1D").first()

    #calculate differences for comparison plots
    wave_no = wave_ds - nowave_ds

    wave_ostia = wave_ds - ostia_hr

    nowave_ostia = nowave_ds - ostia_hr

    #set min and max and created levels for  constant color bars across the same calculation 
    wnow_min = -1
    wnow_max = 1  #hardcoding better for visualization

    #wnow_levels = cont_levels.cont_levels(wnow_min, wnow_max, 15)  # levels for the contour plot
    
    #use the same hardcoded levels for both ostia difference sets
    vmin = -2.5
    vmax = 2.5

    #ow_levels = cont_levels.cont_levels(vmin, vmax, 15)  #levels of the contour plot

    #onow_levels = cont_levels.cont_levels(vmin, vmax, 15)

    #use slice() to put data into non calendar weekly subsets
    wnow1 = wave_no.sel(time = slice(YEAR + "-11-01", YEAR + "-11-07")).mean(dim = "time")
    wnow2 = wave_no.sel(time = slice(YEAR + "-11-08", YEAR + "-11-14")).mean(dim = "time")
    wnow3 = wave_no.sel(time = slice(YEAR + "-11-18", YEAR + "-11-24")).mean(dim = "time")
    wnow4 = wave_no.sel(time = slice(YEAR + "-11-25", YEAR + "-12-01")).mean(dim = "time")
    wnow_arr = [wnow1, wnow2, wnow3, wnow4]

    ow1 = wave_ostia.sel(time = slice(YEAR + "-11-01", YEAR + "-11-07")).mean(dim = "time")
    ow2 = wave_ostia.sel(time = slice(YEAR + "-11-08", YEAR + "-11-14")).mean(dim = "time")
    ow3 = wave_ostia.sel(time = slice(YEAR + "-11-18", YEAR + "-11-24")).mean(dim = "time")
    ow4 = wave_ostia.sel(time = slice(YEAR + "-11-25", YEAR + "-12-01")).mean(dim = "time")
    ow_arr = [ow1, ow2, ow3, ow4]

    onow1 = nowave_ostia.sel(time = slice(YEAR + "-11-01", YEAR + "-11-07")).mean(dim = "time")
    onow2 = nowave_ostia.sel(time = slice(YEAR + "-11-08", YEAR + "-11-14")).mean(dim = "time")
    onow3 = nowave_ostia.sel(time = slice(YEAR + "-11-18", YEAR + "-11-24")).mean(dim = "time")
    onow4 = nowave_ostia.sel(time = slice(YEAR + "-11-25", YEAR + "-12-01")).mean(dim = "time")
    onow_arr = [onow1, onow2, onow3, onow4]

    #set up figure for the plots
    fig, axs = plt.subplots(nrows = NROWS, ncols = NCOLS, layout = "constrained", subplot_kw = {"projection": ccrs.PlateCarree()})

    #plot wave vs no wave differences
    plts_wnow = []

    for i in range(0, NROWS):
        p = axs[i][0].pcolormesh(wnow_arr[i].lon, wnow_arr[i].lat, wnow_arr[i], transform = ccrs.PlateCarree(), cmap = "Spectral_r", vmin = wnow_min, vmax = wnow_max)
        axs[i][0].set_title("Week {}".format(i + 1))
        axs[i][0].coastlines()
        axs[i][0].gridlines(draw_labels = {"left": "y"}, linestyle = "--", linewidth = 0.5)
        plts_wnow.append(p)

    axs[NROWS - 1][0].gridlines(draw_labels = {"bottom": "x"}, linestyle = "--", linewidth = 0.5)
    fig.colorbar(plts_wnow[0], ax = axs[:, 0].ravel().tolist(), location = "right", label = "deg C", extend = "both")
    
    #plot wave vs ostia differences
    plts_ow = []

    for j in range(0, NROWS):
        p = axs[j][1].pcolormesh(ow_arr[j].lon, ow_arr[j].lat, ow_arr[j], transform = ccrs.PlateCarree(), cmap = "Spectral_r", vmin = vmin, vmax = vmax)
        axs[j][1].set_title("Week {}".format(j + 1))
        axs[j][1].coastlines()
        axs[j][1].gridlines(linestyle = "--", linewidth = 0.5)
        plts_ow.append(p)

    axs[NROWS - 1][1].gridlines(draw_labels = {"bottom": "x"}, linestyle = "--", linewidth = 0.5)

    #plot now wave vs ostia differences 
    plts_onow = []

    for k in range(0, NROWS):
        p = axs[k][2].pcolormesh(onow_arr[k].lon, onow_arr[k].lat, onow_arr[k], transform = ccrs.PlateCarree(), cmap = "Spectral_r", vmin = vmin, vmax = vmax)
        axs[k][2].set_title("Week {}".format(k + 1))
        axs[k][2].coastlines()
        axs[k][2].gridlines(draw_labels = {"right": "y"}, linestyle = "--", linewidth = 0.5)
        plts_onow.append(p)

    axs[NROWS - 1][2].gridlines(draw_labels = {"bottom": "x"}, linestyle = "--", linewidth = 0.5)

    #shared colorbar for both ostia difference sets
    fig.colorbar(plts_onow[0], ax = axs[NROWS - 1, 1:3].ravel().tolist(), location = "bottom", label = "deg C", extend = "both")

    fig.suptitle("Waves - No Waves, Waves - OSTIA, No Waves - OSTIA " + YEAR)

    plt.savefig("ostia" + YEAR + "weekly.png")

if __name__ == "__main__":
    main()
