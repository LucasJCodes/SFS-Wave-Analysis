#!/usr/bin/env python3

#SBATCH -J mldepth_weekly.py
#SBATCH -o mldepth_weekly_out
#SBATCH -e mldepth_weekly_error
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

#this program plots the difference in ocean mixed layer depth between SFS model output with and without waves.

import sys
sys.path.append("/work2/noaa/marine/ljones/SFS-Wave-Analysis/wave_analysis")

from metplot import cont_levels as cl
from metplot import data_range as dr
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import xarray as xr

def main():

    #paths for the ensemble values
    path_waves = "/work2/noaa/marine/ljones/SFS-Wave-Analysis/wave_analysis/MLD1997w_ensemble.nc"
    path_nowaves = "/work2/noaa/marine/ljones/SFS-Wave-Analysis/wave_analysis/MLD1997now_ensemble.nc"

    #read in the data
    waves_in = xr.open_mfdataset(path_waves)
    #waves = waves_in.sel(time = (waves_in.time.dt.hour == 12))

    nowaves_in = xr.open_mfdataset(path_nowaves)

    print(waves_in)
    print(waves_in)

    #calculate the difference
    diff = waves_in - nowaves_in

    #break into weekly segments
    week1 = diff.sel(time = slice("1997-11-01", "1997-11-07"))
    week2 = diff.sel(time = slice("1997-11-08", "1997-11-14"))
    week3 = diff.sel(time = slice("1997-11-15", "1997-11-21"))
    week4 = diff.sel(time = slice("1997-11-22", "1997-11-28"))

    #find overall data min and max for consistent contours and single colorbar
    vmin, vmax = dr.data_range(diff)

    levels = cl.cont_levels(vmin, vmax, 10)

    #plot the differences
    fig, axs = plt.subplots(nrows = 2, ncols = 2, subplot_kw = {"projection": ccrs.PlateCarree()})

    axs[0][0].contourf(week1.longitude, week1.latitude, week1, levels = levels, vmin = vmin, vmax = vmax, transform = ccrs.PlateCarree(), cmap = "seismic")
    axs[0][0].coastlines()
    axs[0][0].set_title("Nov. 1-14, 1997", loc = "left")
    
    axs[0][1].contourf(week2.longitude, week2.latitude, week2, levels = levels, vmin = vmin, vmax = vmax, transform = ccrs.PlateCarree(), cmap = "seismic")
    axs[0][1].coastlines()
    axs[0][1].set_title("Nov. 7-14, 1997", loc = "left")

    axs[1][0].contourf(week3.longitude, week3.latitude, week3, levels = levels, vmin = vmin, vmax = vmax, transform = ccrs.PlateCarree(), cmap = "seismic")
    axs[1][0].coastlines()
    axs[1][0].set_title("Nov. 15-21, 1997", loc = "left")

    axs[1][1].contourf(week4.longitude, week4.latitude, week4, levels = levels, vmin = vmin, vmax = vmax, transform = ccrs.PlateCarree(), cmap = "seismic")
    axs[1][1].coastlines()
    axs[1][1].set_title("Nov. 22-28, 1997", loc = "left")

if __name__ == "__main__":
    main()
