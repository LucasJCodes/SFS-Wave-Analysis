#!/usr/bin/env python3

#SBATCH -J precip_monthly.py
#SBATCH -o precip_monthly_out
#SBATCH -e precip_monthly_error
#SBATCH -q debug
#SBATCH -A marine-cpu
#SBATCH --ntasks=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=0
#SBATCH -t 05:00

############################
#Author: Lucas Jones, Hollings Scholar Intern at NOAA EMC
#Date: 7/19/24
############################

#This program generates plots of weekly precipitation differences between SFS ensemble output data with and without waves.

import sys
sys.path.append("/work2/noaa/marine/ljones/SFS-Wave-Analysis/wave_analysis/")

from metplot import data_range
import cartopy.crs as ccrs
from metplot import cont_levels
import matplotlib.pyplot as plt
import xarray as xr

def main():

    YEAR = "1997"
    YEAR2 = "1998"

    path_nowaves = "/work2/noaa/marine/ljones/SFS-Wave-Analysis/wave_analysis/ensembles/precip" + YEAR + "now_ensemble.nc"
    path_waves = "/work2/noaa/marine/ljones/SFS-Wave-Analysis/wave_analysis/ensembles/precip" + YEAR + "w_ensemble.nc"

    #open and subset the wave data first
    waves_in = xr.open_mfdataset(path_waves)
    waves = waves_in["APCP_surface"] * 1000 / 100**3 * 39.3701 #kg/m^2 to inches using water density 1 g/cm^3
    waves_in.close()

    #open and subset the no wave data
    nowaves_in = xr.open_mfdataset(path_nowaves)
    nowaves = nowaves_in["APCP_surface"] * 1000 / 100**3 * 39.3701 #kg/m^2 to inches using water density 1 g/cm^3
    nowaves_in.close()

    print(waves_in)
    print(nowaves_in)

    #calculate the difference
    diff = waves - nowaves

    #find the largest and smallest values for determing the colorbar range and contour levels
    vmin = -5
    vmax = 5

    levels = cont_levels.cont_levels(vmin, vmax, 15)

    #break into 4 weekly chunks for each dataset and average
    month1 = diff.sel(time = slice(YEAR + "-11-01", YEAR + "-11-30")).sum(dim = "time")
    month2 = diff.sel(time = slice(YEAR + "-12-01", YEAR + "-12-31")).sum(dim = "time")
    month3 = diff.sel(time = slice(YEAR2 + "-01-01", YEAR2 + "-01-31")).sum(dim = "time")

    #plot the weekly differences
    fig, axs = plt.subplots(nrows = 3, ncols = 1, subplot_kw = {"projection": ccrs.PlateCarree()})

    p1 = axs[0].contourf(month1.longitude, month1.latitude, month1, transform = ccrs.PlateCarree(), cmap = "Spectral", levels = levels, vmin = vmin, vmax = vmax, extend = "both")
    axs[0].set_title("November " + YEAR)
    axs[0].coastlines()

    p2 = axs[1].contourf(month2.longitude, month2.latitude, month2, transform = ccrs.PlateCarree(), cmap = "Spectral", levels = levels, vmin = vmin, vmax = vmax)
    axs[1].set_title("December " + YEAR)
    axs[1].coastlines()

    p3 = axs[2].contourf(month3.longitude, month3.latitude, month3, transform = ccrs.PlateCarree(), cmap = "Spectral", levels = levels, vmin = vmin, vmax = vmax)
    axs[2].set_title("January " + YEAR2) 
    axs[2].coastlines()

    fig.colorbar(p1, ax = axs, location = "right", extend = "both", label = "inches")

    plt.savefig("precip" + YEAR + "monthly.png")

if __name__ == "__main__":
    main()
