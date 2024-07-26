#!/usr/bin/env python3

#SBATCH -J mldepth_monthly.py
#SBATCH -o mldepth_monthly_out
#SBATCH -e mldepth_monthly_error
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

from stats import monthly_ttest
from metplot import cont_levels as cl
from metplot import data_range as dr
import cartopy.crs as ccrs
import matplotlib as mpl
import matplotlib.pyplot as plt
import xarray as xr

def main():

    YEAR = "1997"
    YEAR2 = "1998"

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
    week1 = diff.sel(time = slice(YEAR + "-11-01", YEAR + "-11-30")).mean(dim = "time")
    week2 = diff.sel(time = slice(YEAR + "-12-01", YEAR + "-12-31")).mean(dim = "time")
    week3 = diff.sel(time = slice(YEAR2 + "-01-01", YEAR2 + "-01-31")).mean(dim = "time")

    print(week3.max())

    #find overall data min and max for consistent contours and single colorbar
    vmin = -90
    vmax = 90

    levels = cl.cont_levels(vmin, vmax, 15)

    #perform t testing to plot statistical significance
    m1_pvals = monthly_ttest.monthly_ttest("MLD", YEAR, "11", 0.05)
    m2_pvals = monthly_ttest.monthly_ttest("MLD", YEAR, "12", 0.05)
    m3_pvals = monthly_ttest.monthly_ttest("MLD", YEAR2, "01", 0.05)

    mpl.rcParams["hatch.linewidth"] = 0.5

    #plot the differences
    fig, axs = plt.subplots(nrows = 3, ncols = 1, subplot_kw = {"projection": ccrs.PlateCarree()})

    p1 = axs[0].contourf(week1.longitude, week1.latitude, week1, levels = levels, vmin = vmin, vmax = vmax, transform = ccrs.PlateCarree(), cmap = "Spectral_r", extend = "both")
    axs[0].contourf(m1_pvals.longitude, m1_pvals.latitude, m1_pvals, colors = "none", transform = ccrs.PlateCarree(), hatches = ["/"*10])
    axs[0].coastlines()
    axs[0].gridlines(draw_labels = {"left": "y"}, linestyle = "--", linewidth = 0.5)
    axs[0].set_title("November " + YEAR, loc = "left")
    
    axs[1].contourf(week2.longitude, week2.latitude, week2, levels = levels, vmin = vmin, vmax = vmax, transform = ccrs.PlateCarree(), cmap = "Spectral_r")
    axs[1].contourf(m2_pvals.longitude, m2_pvals.latitude, m2_pvals, colors = "none", transform = ccrs.PlateCarree(), hatches = ["/"*10])
    axs[1].coastlines()
    axs[1].gridlines(draw_labels = {"left": "y"}, linestyle = "--", linewidth = 0.5)
    axs[1].set_title("December " + YEAR, loc = "left")

    axs[2].contourf(week3.longitude, week3.latitude, week3, levels = levels, vmin = vmin, vmax = vmax, transform = ccrs.PlateCarree(), cmap = "Spectral_r")
    axs[2].contourf(m3_pvals.longitude, m3_pvals.latitude, m3_pvals, colors = "none", transform = ccrs.PlateCarree(), hatches = ["/"*10])
    axs[2].coastlines()
    axs[2].gridlines(draw_labels = {"left": "y", "bottom": "x"}, linestyle = "--", linewidth = 0.5)
    axs[2].set_title("January " + YEAR2, loc = "left")

    plt.colorbar(p1, ax = axs, location = "right", extend = "both")

    fig.suptitle("Difference in Ocean Mixed Layer Depth (waves - no waves) " + YEAR)

    plt.savefig("mldepth" + YEAR + "monthly.png")

if __name__ == "__main__":
    main()
