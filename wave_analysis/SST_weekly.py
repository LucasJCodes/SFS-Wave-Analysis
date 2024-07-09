#!/usr/bin/env python3

#SBATCH -J SST_weekly.py
#SBATCH -o SST_weekly_out
#SBATCH -e SST_weekly_error
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

#This program graphs ensemble mean wave - no wave differences in SSTs for 4 selected weeks 

import sys
sys.path.append("/work2/noaa/marine/ljones/SFS-Wave-Analysis/wave_analysis/")

from metplot import data_range
import cartopy.crs as ccrs
from metplot import cont_levels
import matplotlib.pyplot as plt
import xarray as xr

def main():

    YEAR = "1997"

    #the filepath for the ensemble mean SST data
    waves = "/work2/noaa/marine/ljones/SFS-Wave-Analysis/wave_analysis/ensembles/SST" + YEAR + "w_ensemble.nc" 
    nowaves = "/work2/noaa/marine/ljones/SFS-Wave-Analysis/wave_analysis/ensembles/SST" + YEAR + "now_ensemble.nc" 

    #read in data
    waves_in = xr.open_mfdataset(waves)["WTMP_surface"] - 273.15  #convert to deg C
    #waves = waves_in.sel(time = (waves_in.time.dt.hour == 12))  #only the 12z times

    nowaves_in = xr.open_mfdataset(nowaves)["WTMP_surface"] - 273.15 #convert to deg C
    #nowaves = nowaves_in.sel(time = (nowaves_in.time.dt.hour == 12)) #only the 12z times

    #calculate the difference between waves and no waves
    diff = waves_in - nowaves_in

    #subset into weekly periods (the first two and last two weeks of the period) and calculate the mean for each week (and make datarray for graphing but selecing var)
    week1 = diff.sel(time = slice(YEAR + "-11-01", YEAR + "-11-07")).mean(dim = "time")
    week2 = diff.sel(time = slice(YEAR + "-11-08", YEAR + "-11-14")).mean(dim = "time")
    week3 = diff.sel(time = slice(YEAR + "-11-15", YEAR + "-11-21")).mean(dim = "time")
    week4 = diff.sel(time = slice(YEAR + "-11-22", YEAR + "-11-28")).mean(dim = "time")

    print(week1)
    print(week2)
    print(week3)
    print(week4)

    #find overall data min and max for consistent contours and single colorbar
    vmin, vmax = data_range.data_range(diff)
    
    print("vmin: " + str(vmin) + " vmax: " + str(vmax))

    levs = cont_levels.cont_levels(vmin, vmax, 10)

    #plot
    fig, axs = plt.subplots(nrows = 2, ncols = 2, subplot_kw = {"projection": ccrs.PlateCarree()})
    
    ax1 = axs[0][0].contourf(week1.longitude, week1.latitude, week1, levels = levs, vmin = vmin, vmax = vmax, transform = ccrs.PlateCarree(), cmap = "seismic")
    axs[0][0].coastlines()
    axs[0][0].set_title("Nov. 1-7, " + YEAR, loc = "left")

    ax2 = axs[0][1].contourf(week2.longitude, week2.latitude, week2, levels = levs, vmin = vmin, vmax = vmax, transform = ccrs.PlateCarree(), cmap = "seismic")
    axs[0][1].coastlines()
    axs[0][1].set_title("Nov. 8-14, " + YEAR, loc = "left")

    ax3 = axs[1][0].contourf(week3.longitude, week3.latitude, week3, levels = levs, vmin = vmin, vmax = vmax, transform = ccrs.PlateCarree(), cmap = "seismic")
    axs[1][0].coastlines()
    axs[1][0].set_title("Nov. 15-21, " + YEAR, loc = "left")

    ax4 = axs[1][1].contourf(week4.longitude, week4.latitude, week4, levels = levs, vmin = vmin, vmax = vmax, transform = ccrs.PlateCarree(), cmap = "seismic", extend = "both")
    axs[1][1].coastlines()
    axs[1][1].set_title("Nov. 22-18, " + YEAR, loc = "left")
    
    plt.colorbar(ax4, ax = axs, location = "bottom", label = "deg C", extend = "both", pad = 0.05)

    fig.suptitle("Difference in Sea Surface Temperatures")

    plt.savefig("SST" + YEAR + "weekly.png")

if __name__ == "__main__":
    main()
