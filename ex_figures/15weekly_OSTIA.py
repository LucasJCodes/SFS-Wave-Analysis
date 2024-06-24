#!/usr/bin/env python3

#SBATCH -J 15weekly_OSTIA.py
#SBATCH -o 15weekly_OSTIA_out
#SBATCH -e 15weekly_OSTIA_error
#SBATCH -q debug
#SBATCH -A marine-cpu
#SBATCH --ntasks=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=0
#SBATCH -t 05:00

############################
#Author: Lucas Jones, Hollings Scholar Intern at NOAA EMC
#Date: 6/21/24
############################

import cartopy.crs as ccrs
import datetime as dt
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import xarray as xr
import xesmf as xe

#simple helpter function to determine the contour range for a sysmetrical colorbar 
def cbar_range(dataset):
    
    vmin = np.nan
    vmax = np.nan

    data_min = dataset.min().values
    data_max = dataset.max().values

    if data_max > abs(data_min):
        vmax = data_max
        vmin = -data_max

    else:
        vmax = abs(data_min)
        vmin = - abs(data_min)

    return vmin, vmax

def main():

    #constants holding the number of rows and columns in the final figure (used outside figure creation)
    NROWS = 3
    NCOLS = 4

    ostia_path = "/work2/noaa/marine/jmeixner/ReferenceData/sst_OSTIA/1p00/daily/sst_OSTIA.20151*****.1p00.nc" 
    nowave_path = "/work2/noaa/marine/ljones/30day_tests/Nov15_S2S/COMROOT/Nov15_S2S/gefs.20151101/00/mem000/products/ocean/netcdf/*.nc"
    wave_path = "/work2/noaa/marine/ljones/30day_tests/Nov15_S2SW/COMROOT/Nov15_S2SW/gefs.20151101/00/mem000/products/ocean/netcdf/*.nc"

    #read the data in
    ostia_in = xr.open_mfdataset(ostia_path).sel(time = slice("2015-11-01", "2015-11-30"))
    wave_in = xr.open_mfdataset(wave_path).rename({"yh": "lat", "xh": "lon"})
    nowave_in = xr.open_mfdataset(nowave_path).rename({"yh": "lat", "xh": "lon"})

    #subset the model data to get SSTs, convert to Celsius if necessary 
    ostia_ds = ostia_in["analysed_sst"] - 273.15 #deg C
    wave_ds = wave_in["SST"] #already in deg C
    nowave_ds = nowave_in["SST"] #a;ready in deg C
   
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
    wnow_min, wnow_max = cbar_range(wave_no)
    wnow_step = (wnow_max - wnow_min) / 10
    wnow_levels = np.arange(wnow_min, wnow_max + wnow_step, wnow_step) # levels for the contour plot

    ow_min, ow_max = cbar_range(wave_ostia)
    ow_step = (ow_max - ow_min) / 10
    ow_levels = np.arange(ow_min, ow_max + ow_step - 0.1, ow_step) #slight binary math error, subtract 0.1 to make sure only the top bin is included, not an additional one

    onow_min, onow_max = cbar_range(nowave_ostia)
    onow_step = (onow_max - onow_min) / 10
    onow_levels = np.arange(onow_min, onow_max + onow_step, onow_step)

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

    plt.savefig("bigcomp_15.png")

if __name__ == "__main__":
    main()
