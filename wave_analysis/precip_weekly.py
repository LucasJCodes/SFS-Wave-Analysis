#!/usr/bin/env python3

#SBATCH -J precip_weekly.py
#SBATCH -o precip_weekly_out
#SBATCH -e precip_weekly_error
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

#This program generates plots of weekly precipitation differences between SFS ensemble output data with and without waves.

import sys
sys.path.append("/work2/noaa/marine/ljones/SFS-Wave-Analysis/wave_analysis/")

from stats import weekly_ttest
from metplot import data_range
import cartopy.crs as ccrs
from metplot import cont_levels
import matplotlib as mpl
import matplotlib.pyplot as plt
import xarray as xr

def main():

    YEAR = "1997"

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
    vmin = -2
    vmax = 2

    levels = cont_levels.cont_levels(vmin, vmax, 15)

    #break into 4 weekly chunks for each dataset and average
    week1 = diff.sel(time = slice(YEAR + "-11-01", YEAR + "-11-07")).sum(dim = "time")
    week2 = diff.sel(time = slice(YEAR + "-11-08", YEAR + "-11-14")).sum(dim = "time")
    week3 = diff.sel(time = slice(YEAR + "-11-17", YEAR + "-11-23")).sum(dim = "time")
    week4 = diff.sel(time = slice(YEAR + "-11-24", YEAR + "-11-30")).sum(dim = "time")

    #perform t testing to plot statistical significance
    w1_pvals = weekly_ttest.weekly_ttest("APCP_surface", YEAR, "11", "01", 0.05)
    w2_pvals = weekly_ttest.weekly_ttest("APCP_surface", YEAR, "11", "08", 0.05)
    w3_pvals = weekly_ttest.weekly_ttest("APCP_surface", YEAR, "11", "15", 0.05)
    w4_pvals = weekly_ttest.weekly_ttest("APCP_surface", YEAR, "11", "22", 0.05)

    mpl.rcParams["hatch.linewidth"] = 0.5

    #plot the weekly differences
    fig, axs = plt.subplots(nrows = 2, ncols = 2, subplot_kw = {"projection": ccrs.PlateCarree()})

    p1 = axs[0][0].contourf(week1.longitude, week1.latitude, week1, transform = ccrs.PlateCarree(), cmap = "Spectral", levels = levels, vmin = vmin, vmax = vmax, extend = "both")
    axs[0][0].contourf(w1_pvals.longitude, w1_pvals.latitude, w1_pvals, colors = "none", hatches = ["/"*10], transform = ccrs.PlateCarree())
    axs[0][0].set_title("Nov. 1-7, " + YEAR)
    axs[0][0].coastlines()
    axs[0][0].gridlines(draw_labels = {"left": "y"}, linestyle = "--", linewidth = 0.5)

    p2 = axs[0][1].contourf(week2.longitude, week2.latitude, week2, transform = ccrs.PlateCarree(), cmap = "Spectral", levels = levels, vmin = vmin, vmax = vmax)
    axs[0][1].contourf(w2_pvals.longitude, w2_pvals.latitude, w2_pvals, colors = "none", hatches = ["/"*10], transform = ccrs.PlateCarree())
    axs[0][1].set_title("Nov. 8-14, " + YEAR)
    axs[0][1].coastlines()
    axs[0][1].gridlines(linestyle = "--", linewidth = 0.5)

    p3 = axs[1][0].contourf(week3.longitude, week3.latitude, week3, transform = ccrs.PlateCarree(), cmap = "Spectral", levels = levels, vmin = vmin, vmax = vmax)
    axs[1][0].contourf(w3_pvals.longitude, w3_pvals.latitude, w3_pvals, colors = "none", hatches = ["/"*10], transform = ccrs.PlateCarree())
    axs[1][0].set_title("Nov. 15-21, " + YEAR) 
    axs[1][0].coastlines()
    axs[1][0].gridlines(draw_labels = {"bottom": "x", "left": "y"}, linestyle = "--", linewidth = 0.5)

    p4 = axs[1][1].contourf(week4.longitude, week4.latitude, week4, transform = ccrs.PlateCarree(), cmap = "Spectral", levels = levels, vmin = vmin, vmax = vmax) 
    axs[1][1].contourf(w4_pvals.longitude, w4_pvals.latitude, w4_pvals, colors = "none", hatches = ["/"*10], transform = ccrs.PlateCarree())
    axs[1][1].set_title("Nov. 22-28, " + YEAR)
    axs[1][1].coastlines()
    axs[1][1].gridlines(draw_labels = {"bottom": "x"}, linestyle = "--", linewidth = 0.5)

    fig.colorbar(p1, ax = axs, location = "bottom", extend = "both", label = "inches")

    fig.suptitle("Difference in Precipitation (waves - no waves) " + YEAR)

    plt.savefig("precip" + YEAR + "weekly.png")

if __name__ == "__main__":
    main()
