#!/usr/bin/env python3

#SBATCH -J total_precip.py
#SBATCH -o out_totalp
#SBATCH -e error_totalp
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

#This program plots the total precipitation from 30 day SFS model runs with IC 2020-11-01 with and without waves for comparison

import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import xarray as xr

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

    #ensure datasets are for same time period and sum data along the time period
    precip_waves = waves.sel(time = slice("2020-11-01", "2020-11-30")).sum(dim = "time")
    precip_nowaves = nowaves.sel(time = slice("2020-11-01", "2020-11-30")).sum(dim = "time") 

    #get data max and mins to determine the colorbar range
    w_max = precip_waves.max().values
    w_min = precip_waves.max().values

    now_max = precip_waves.max().values
    now_min = precip_waves.min().values

    if w_max > now_max:
        vmax = w_max
    else:
        vmax = now_max

    if w_min < now_min:
        vmin = w_min
    else:
        vmin = now_min

    #plot sums
    fig, axs = plt.subplots(nrows = 2, ncols = 1, subplot_kw = {"projection": ccrs.PlateCarree()})

    ax1 = axs[0].contourf(precip_waves.longitude, precip_waves.latitude, precip_waves, transformation = ccrs.PlateCarree(), vmax = vmax, vmin = vmin)
    axs[0].coastlines()

    ax2 = axs[1].contourf(precip_nowaves.longitude, precip_nowaves.latitude, precip_nowaves, transformation = ccrs.PlateCarree(), vmax = vmax, vmin = vmin)
    axs[1].coastlines()

    fig.colorbar(ax2, location = "bottom", extend = "both") 

    plt.savefig("total_precip.png")

    print("test")

if __name__ == "__main__":
    main()
