#!/usr/bin/env python3

#SBATCH -J 850height_weekly.py
#SBATCH -o 850height_weekly_out
#SBATCH -e 850height_weekly_error
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

#This program plots differences in weekly mean 850 hPa heights, waves - no waves, for 
# one of the 3 initial condition dates (1997, 2015, 2020).

import sys
sys.path.append("/work2/noaa/marine/ljones/SFS-Wave-Analysis/wave_analysis/")

from stats import weekly_ttest
from metplot import data_range
import cartopy.crs as ccrs
import matplotlib as mpl
from metplot import cont_levels
import matplotlib.pyplot as plt
import xarray as xr

def main():
    
    YEAR = "2020"

    #file path for the ensemble means
    wave_path = "/work2/noaa/marine/ljones/SFS-Wave-Analysis/wave_analysis/ensembles/850Height" + YEAR + "w_ensemble.nc" 
    nowave_path = "/work2/noaa/marine/ljones/SFS-Wave-Analysis/wave_analysis/ensembles/850Height" + YEAR + "now_ensemble.nc"

    #open the data
    nowave_in = xr.open_mfdataset(nowave_path)
    wave_in = xr.open_mfdataset(wave_path)

    #subset data to get 850 hPa heights only at 12z each day
    nowave_850 = nowave_in["HGT_850mb"] #.sel(time = (nowave_in.time.dt.hour == 12))
    wave_850 = wave_in["HGT_850mb"] #.sel(time = (wave_in.time.dt.hour == 12))

    print(nowave_850)
    print(wave_850)

    #calculate the difference 
    diff = wave_850 - nowave_850

    #separate into weekly periods for graphing
    week1 = diff.sel(time = slice(YEAR + "-11-01", YEAR + "-11-07")).mean(dim = "time")
    week2 = diff.sel(time = slice(YEAR + "-11-08", YEAR + "-11-14")).mean(dim = "time")
    week3 = diff.sel(time = slice(YEAR + "-11-15", YEAR + "-11-21")).mean(dim = "time")
    week4 = diff.sel(time = slice(YEAR + "-11-22", YEAR + "-11-28")).mean(dim = "time")

    #set the range for the data so the contour levels and colorbar are the same
    vmin = -120 #data_range.data_range(diff)
    vmax = 120

    levels = cont_levels.cont_levels(vmin, vmax, 15)
    
    #perform t testing to plot statistical significance
    w1_pvals = weekly_ttest.weekly_ttest("850Height", YEAR, "11", "01", 0.05)
    w2_pvals = weekly_ttest.weekly_ttest("850Height", YEAR, "11", "08", 0.05)
    w3_pvals = weekly_ttest.weekly_ttest("850Height", YEAR, "11", "15", 0.05)
    w4_pvals = weekly_ttest.weekly_ttest("850Height", YEAR, "11", "22", 0.05)

    mpl.rcParams["hatch.linewidth"] = 0.5

    #plot the differences
    fig, axs = plt.subplots(nrows = 2, ncols = 2, subplot_kw = {"projection": ccrs.PlateCarree()})
    fig.suptitle("Difference in 850hPa Geopotential Height (waves - no waves) " + YEAR, fontsize = 12)

    ax1 = axs[0][0].contourf(week1.longitude, week1.latitude, week1, levels = levels, vmin = vmin, vmax = vmax, transform = ccrs.PlateCarree(), cmap = "seismic")
    axs[0][0].contourf(w1_pvals.longitude, w1_pvals.latitude, w1_pvals, colors = "none", hatches = ["/"*10], transform = ccrs.PlateCarree())
    axs[0][0].coastlines()
    axs[0][0].gridlines(draw_labels = {"left": "y"}, linestyle = "--", linewidth = 0.5)
    axs[0][0].set_title("Nov. 1-7, " + YEAR, loc = "left")

    ax2 = axs[0][1].contourf(week2.longitude, week2.latitude, week2, levels = levels, vmin = vmin, vmax = vmax, transform = ccrs.PlateCarree(), cmap = "seismic")
    axs[0][1].contourf(w2_pvals.longitude, w2_pvals.latitude, w2_pvals, colors = "none", hatches = ["/"*10], transform = ccrs.PlateCarree())
    axs[0][1].coastlines()
    axs[0][1].gridlines(linestyle = "--", linewidth = 0.5)
    axs[0][1].set_title("Nov. 8-14, " + YEAR, loc = "left")

    ax3 = axs[1][0].contourf(week3.longitude, week3.latitude, week3, levels = levels, vmin = vmin, vmax = vmax, transform = ccrs.PlateCarree(), cmap = "seismic")
    axs[1][0].contourf(w3_pvals.longitude, w3_pvals.latitude, w3_pvals, colors = "none", hatches = ["/"*10], transform = ccrs.PlateCarree())
    axs[1][0].coastlines()
    axs[1][0].gridlines(draw_labels = {"bottom": "x", "left": "y"}, linestyle = "--", linewidth = 0.5)
    axs[1][0].set_title("Nov. 15-21, " + YEAR, loc = "left")

    ax4 = axs[1][1].contourf(week4.longitude, week4.latitude, week4, levels = levels, vmin = vmin, vmax = vmax, transform = ccrs.PlateCarree(), cmap = "seismic", extend = "both")
    axs[1][1].contourf(w4_pvals.longitude, w4_pvals.latitude, w4_pvals, colors = "none", hatches = ["/"*10], transform = ccrs.PlateCarree())
    axs[1][1].coastlines()
    axs[1][1].gridlines(draw_labels = {"bottom": "x"}, linestyle = "--", linewidth = 0.5)
    axs[1][1].set_title("Nov. 22-28, " + YEAR, loc = "left")

    plt.colorbar(ax4, ax = axs, extend = "both", orientation = "horizontal", label = "meters")

    plt.savefig("850height" + YEAR + "weekly.png")

if __name__ == "__main__":
    main()
