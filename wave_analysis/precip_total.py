#!/usr/bin/env python3

#SBATCH -J precip_total.py
#SBATCH -o precip_total_out
#SBATCH -e precip_total_error
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

#this takes ensemble mean precipitation data with and without waves and plots the difference in total precipitation

import sys
sys.path.append("/work2/noaa/marine/ljones/SFS-Wave-Analysis/wave_analysis/")

import cartopy.crs as ccrs
from metplot import cont_levels
import matplotlib.pyplot as plt
import xarray as xr

def main():
    
    #file paths for wave and non wave precip ensemble means
    waves_path = "/work2/noaa/marine/ljones/SFS-Wave-Analysis/wave_analysis/readio/precip1997w_ensemble.nc"
    nowaves_path = "/work2/noaa/marine/ljones/SFS-Wave-Analysis/wave_analysis/readio/precip1997now_ensemble.nc"

    #open and subset the wave data first
    waves_in = xr.open_mfdataset(waves_path)
    waves = waves_in["APCP_surface"] * 1000 / 100**3 * 39.3701 #kg/m^2 to inches using water density 1 g/m^3
    waves_in.close()

    #open and subset the no wave data
    nowaves_in = xr.open_mfdataset(nowaves_path)
    nowaves = nowaves_in["APCP_surface"] * 1000 / 100**3 * 39.3701 #kg/m^2 to inches using water density 1 g/m^c
    nowaves_in.close()

    #find the sum total precipitation for each data set
    total_waves = waves.sum(dim = "time")
    total_nowaves = nowaves.sum(dim = "time")

    #calculate the difference 
    diff = total_waves - total_nowaves

    print(total_waves[50, 50].values)
    print(total_nowaves[50, 50].values)
    print(diff[50, 50].values)

    #get max values so both total plots have same contour bins and colorbar range
    vmin = 0  #assume the smallest amount of precip is 0

    wmax = total_waves.max().values
    nowmax = total_nowaves.max().values

    if wmax > nowmax:
        vmax = wmax

    else:
        vmax = nowmax

    precip_levels = cont_levels.cont_levels(0, vmax, 10)

    #plot the toal precipitation for each and the difference
    fig, axs = plt.subplots(nrows = 3, ncols = 1, subplot_kw = {"projection": ccrs.PlateCarree()})

    p1 = axs[0].contourf(total_waves.longitude, total_waves.latitude, total_waves, levels = precip_levels, vmin = vmin, vmax = vmax, transform = ccrs.PlateCarree())
    axs[0].coastlines()
    axs[0].set_title("With Waves")

    p2 = axs[1].contourf(total_waves.longitude, total_waves.latitude, total_waves, levels = precip_levels, vmin = vmin, vmax = vmax, transform = ccrs.PlateCarree())
    axs[1].coastlines()
    axs[1].set_title("Without Waves")

    fig.colorbar(p1, ax = axs[0:2].ravel().tolist(), location = "bottom", extend = "right")

    p3 = axs[2].contourf(total_waves.longitude, total_waves.latitude, total_waves, transform = ccrs.PlateCarree(), cmap = "seismic")
    axs[2].coastlines()
    axs[2].set_title("Waves - No Waves")

    fig.colorbar(p3, location = "bottom", extend = "both")

    fig.suptitle("Total Precipitation Comparison")

    plt.savefig("precip_total.png")

if __name__ == "__main__":
    main()
