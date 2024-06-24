#!/usr/bin/env python3

#SBATCH -J precip_diffs.py
#SBATCH -o out_precip
#SBATCH -e error_precip
#SBATCH -q debug
#SBATCH -A marine-cpu
#SBATCH --ntasks=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=0
#SBATCH -t 05:00

############################
#Author: Lucas Jones, Hollings Scholar Intern at NOAA EMC
#Date: 6/24/24
############################

#This program reads in model outputted precipitation data for three different IC datess (1997-11-01, 2015-11-01, 2020-11-01) and 

import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import numpy as np
import xarray as xr

#a simple helper function to return the dataset minimum and maximum for use determining the plot colorbar min and max
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

    path_nowaves = "/work2/noaa/marine/ljones/30day_tests/Nov20_S2S/COMROOT/Nov20_S2S/gefs.20201101/00/mem000/products/atmos/grib2/1p00/gefs.t00z.pgrb2.1p00.f*.nc"
    path_waves = "/work2/noaa/marine/ljones/30day_tests/Nov20_S2SW/COMROOT/Nov20_S2SW/gefs.20201101/00/mem000/products/atmos/grib2/1p00/gefs.t00z.pgrb2.1p00.f*.nc"

    #open and subset the wave data first
    waves_in = xr.open_mfdataset(path_waves)
    waves = waves_in["APCP_surface"] * 1000 / 100**3 * 39.3701 #kg/m^2 to inches using water density 1 g/m^3
    waves_in.close()

    #open and subset the no wave data
    nowaves_in = xr.open_mfdataset(path_nowaves)
    nowaves = nowaves_in["APCP_surface"] * 1000 / 100**3 * 39.3701 #kg/m^2 to inches using water density 1 g/m^c
    nowaves_in.close()

    #calculate the difference
    diff = waves - nowaves

    #find the largest and smallest values for determing the colorbar range
    vmin, vmax = cbar_range(diff)

    #break into 4 weekly chunks for each dataset and average
    week1 = diff.sel(time = slice("2020-11-01", "2020-11-07")).sum(dim = "time")
    week2 = diff.sel(time = slice("2020-11-08", "2020-11-14")).sum(dim = "time")
    week3 = diff.sel(time = slice("2020-11-17", "2020-11-23")).sum(dim = "time")
    week4 = diff.sel(time = slice("2020-11-24", "2020-11-30")).sum(dim = "time")

    #plot the weekly differences
    fig, axs = plt.subplots(nrows = 2, ncols = 2, subplot_kw = {"projection": ccrs.PlateCarree()})

    p1 = axs[0][0].contourf(week1.longitude, week1.latitude, week1, transform = ccrs.PlateCarree(), cbar = "seismic", vmin = vmin, vmax = vmax)
    axs[0][0].set_title("Week 1")
    axs[0][0].coastlines()

    p2 = axs[0][1].contourf(week2.longitude, week2.latitude, week2, transform = ccrs.PlateCarree(), cbar = "seismic", vmin = vmin, vmax = vmax)
    axs[0][1].set_title("Week 2")
    axs[0][1].coastlines()

    p3 = axs[1][0].contourf(week3.longitude, week3.latitude, week3, transform = ccrs.PlateCarree(), cbar = "seismic", vmin = vmin, vmax = vmax)
    axs[1][0].set_title("Week 3")
    axs[1][0].coastlines()

    p4 = axs[1][1].contourf(week4.longitude, week4.latitude, week4, transform = ccrs.PlateCarree(), cbar = "seismic", vmin = vmin, vmax = vmax) 
    axs[1][1].set_title("Week 4")
    axs[1][1].coastlines()

    fig.colorbar(p1, ax = axs[1, :].ravel().tolist(), location = "bottom")

    plt.savefig("comp_precip.png")

if __name__ == "__main__":
    main()
