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
#SBATCH -t 10:00

############################
#Author: Lucas Jones, Hollings Scholar Intern at NOAA EMC
#Date: 7/8/24
############################

#this program plots the difference in ocean mixed layer depth between SFS model output with and without waves.

import sys
sys.path.append("/work2/noaa/marine/ljones/SFS-Wave-Analysis/wave_analysis")

from stats import weekly_ttest
from metplot import cont_levels as cl
from metplot import data_range as dr
import cartopy.crs as ccrs
import matplotlib as mpl
import matplotlib.pyplot as plt
import xarray as xr

def main():

    YEAR = "1997"

    #paths for the ensemble values
    path_waves = "/work2/noaa/marine/ljones/SFS-Wave-Analysis/wave_analysis/ensembles/MLD" + YEAR + "w_ensemble.nc"
    path_nowaves = "/work2/noaa/marine/ljones/SFS-Wave-Analysis/wave_analysis/ensembles/MLD" + YEAR + "now_ensemble.nc"

    #read in the data
    waves_in = xr.open_mfdataset(path_waves)["WDEPTH_mixedlayerdepth"]

    nowaves_in = xr.open_mfdataset(path_nowaves)["WDEPTH_mixedlayerdepth"]

    print(waves_in)
    print(nowaves_in)

    #calculate the difference
    diff = waves_in - nowaves_in

    #break into weekly segments
    week1 = diff.sel(time = slice(YEAR + "-11-01", YEAR + "-11-07")).mean(dim = "time")
    week2 = diff.sel(time = slice(YEAR + "-11-08", YEAR + "-11-14")).mean(dim = "time")
    week3 = diff.sel(time = slice(YEAR + "-11-15", YEAR + "-11-21")).mean(dim = "time")
    week4 = diff.sel(time = slice(YEAR + "-11-22", YEAR + "-11-28")).mean(dim = "time")

    #find overall data min and max for consistent contours and single colorbar
    vmin = -30
    vmax = 30

    levels = cl.cont_levels(vmin, vmax, 15)

    #perform t testing to plot statistical significance
    w1_pvals = weekly_ttest.weekly_ttest("MLD", YEAR, "11", "01", 0.05)
    w2_pvals = weekly_ttest.weekly_ttest("MLD", YEAR, "11", "08", 0.05)
    w3_pvals = weekly_ttest.weekly_ttest("MLD", YEAR, "11", "15", 0.05)
    w4_pvals = weekly_ttest.weekly_ttest("MLD", YEAR, "11", "22", 0.05)

    mpl.rcParams["hatch.linewidth"] = 0.5

    #plot the differences
    fig, axs = plt.subplots(nrows = 2, ncols = 2, subplot_kw = {"projection": ccrs.PlateCarree()})

    p1 = axs[0][0].contourf(week1.longitude, week1.latitude, week1, levels = levels, vmin = vmin, vmax = vmax, transform = ccrs.PlateCarree(), cmap = "Spectral", extend = "both")
    axs[0][0].contourf(w1_pvals.longitude, w1_pvals.latitude, w1_pvals, colors = "none", hatches = ["/"*10], transform = ccrs.PlateCarree())
    axs[0][0].coastlines()
    axs[0][0].gridlines(draw_labels = {"left": "y"}, linestyle = "--", linewidth = 0.5)
    axs[0][0].set_title("Nov 1-7, " + YEAR, loc = "left")
    
    axs[0][1].contourf(week2.longitude, week2.latitude, week2, levels = levels, vmin = vmin, vmax = vmax, transform = ccrs.PlateCarree(), cmap = "Spectral")
    axs[0][1].contourf(w2_pvals.longitude, w2_pvals.latitude, w2_pvals, colors = "none", hatches = ["/"*10], transform = ccrs.PlateCarree())
    axs[0][1].coastlines()
    axs[0][1].gridlines(linestyle = "--", linewidth = 0.5)
    axs[0][1].set_title("Nov. 8-14, " + YEAR, loc = "left")

    axs[1][0].contourf(week3.longitude, week3.latitude, week3, levels = levels, vmin = vmin, vmax = vmax, transform = ccrs.PlateCarree(), cmap = "Spectral")
    axs[1][0].contourf(w3_pvals.longitude, w3_pvals.latitude, w3_pvals, colors = "none", hatches = ["/"*10], transform = ccrs.PlateCarree())
    axs[1][0].coastlines()
    axs[1][0].gridlines(draw_labels = {"left": "y", "bottom": "x"}, linestyle = "--", linewidth = 0.5)
    axs[1][0].set_title("Nov. 15-21, " + YEAR, loc = "left")

    axs[1][1].contourf(week4.longitude, week4.latitude, week4, levels = levels, vmin = vmin, vmax = vmax, transform = ccrs.PlateCarree(), cmap = "Spectral")
    axs[1][1].contourf(w4_pvals.longitude, w4_pvals.latitude, w4_pvals, colors = "none", hatches = ["/"*10], transform = ccrs.PlateCarree())
    axs[1][1].coastlines()
    axs[1][1].gridlines(draw_labels = {"bottom": "x"}, linestyle = "--", linewidth = 0.5)
    axs[1][1].set_title("Nov. 22-28, " + YEAR, loc = "left")

    plt.colorbar(p1, ax = axs, location = "bottom", extend = "both")

    fig.suptitle("Difference in Ocean Mixed Layer Depth (waves - no waves) " + YEAR)

    plt.savefig("mldepth" + YEAR + "weekly.png")

if __name__ == "__main__":
    main()
