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

from metplot import data_range
import cartopy.crs as ccrs
from metplot import cont_levels
import matplotlib.pyplot as plt
import xarray as xr

def main():

    YEAR = "1997"

    #file paths for wave and non wave precip ensemble means
    waves_path = "/work2/noaa/marine/ljones/SFS-Wave-Analysis/wave_analysis/ensembles/precip" + YEAR + "w_ensemble.nc"
    nowaves_path = "/work2/noaa/marine/ljones/SFS-Wave-Analysis/wave_analysis/ensembles/precip" + YEAR + "now_ensemble.nc"

    #open and subset the wave data first
    waves_in = xr.open_mfdataset(waves_path)
    waves = waves_in["APCP_surface"] * 1000 / 100**3 * 39.3701 #kg/m^2 to inches using water density 1 g/m^3
    waves_in.close()

    #open and subset the no wave data
    nowaves_in = xr.open_mfdataset(nowaves_path)
    nowaves = nowaves_in["APCP_surface"] * 1000 / 100**3 * 39.3701 #kg/m^2 to inches using water density 1 g/m^c
    nowaves_in.close()

    print(waves_in)
    print(nowaves_in)

    #find the sum total precipitation for each data set
    total_waves = waves.sum(dim = "time")
    total_nowaves = nowaves.sum(dim = "time")

    #calculate the difference 
    diff = total_waves - total_nowaves

    #get max values so both total plots have same contour bins and colorbar range
    vmin = 0  #assume the smallest amount of precip is 0

    vmax = 70

    precip_levels = cont_levels.cont_levels(0, vmax, 15)

    #get a symetric colorbar range for the diff plot
    dmin = -6
    dmax = 6

    diff_levels = cont_levels.cont_levels(dmin, dmax, 15)

    #plot the toal precipitation for each and the difference
    fig, axs = plt.subplots(nrows = 3, ncols = 1, subplot_kw = {"projection": ccrs.PlateCarree()})

    p1 = axs[0].contourf(total_waves.longitude, total_waves.latitude, total_waves, levels = precip_levels, vmin = vmin, vmax = vmax, cmap = "YlGnBu", transform = ccrs.PlateCarree(), extend = "max")
    axs[0].coastlines()
    axs[0].set_title("Total With Waves", loc = "left")

    p2 = axs[1].contourf(total_nowaves.longitude, total_nowaves.latitude, total_nowaves, levels = precip_levels, vmin = vmin, vmax = vmax, cmap = "YlGnBu", transform = ccrs.PlateCarree(), extend = "max")
    axs[1].coastlines()
    axs[1].set_title("Total Without Waves", loc = "left")

    fig.colorbar(p1, ax = axs[0:2].ravel().tolist(), extend = "max", label = "inches of rain")

    p3 = axs[2].contourf(diff.longitude, diff.latitude, diff, levels = diff_levels, vmin = dmin, vmax = dmax, cmap = "Spectral", transform = ccrs.PlateCarree(), extend = "both")
    axs[2].coastlines()
    axs[2].set_title("Difference Waves - No Waves", loc = "left")

    fig.colorbar(p3, ax = axs[2], location = "right", extend = "both", label = "Difference in inches")

    fig.suptitle("Total Precipitation (Nov - Jan) Comparison " + YEAR)

    plt.savefig("precip" + YEAR + "total.png")

if __name__ == "__main__":
    main()
