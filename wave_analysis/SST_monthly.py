#!/usr/bin/env python3

#SBATCH -J SST_monthly.py
#SBATCH -o SST_monthly_out
#SBATCH -e SST_monthly_error
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

#This program graphs ensemble mean wave - no wave differences in SSTs for 3 month long periods
#(November, December, January) of the three initial condition dates.

import sys
sys.path.append("/work2/noaa/marine/ljones/SFS-Wave-Analysis/wave_analysis/")

from metplot import data_range
import cartopy.crs as ccrs
from metplot import cont_levels
import matplotlib.pyplot as plt
import matplotlib as mpl
from stats import monthly_ttest
import xarray as xr

def main():

    YEAR = "2020"
    YEAR2 = "2021"

    #the filepath for the ensemble mean SST data
    waves = "/work2/noaa/marine/ljones/SFS-Wave-Analysis/wave_analysis/ensembles/SST" + YEAR + "w_ensemble.nc"
    nowaves = "/work2/noaa/marine/ljones/SFS-Wave-Analysis/wave_analysis/ensembles/SST" + YEAR + "now_ensemble.nc"

    #read in data
    waves_in = xr.open_mfdataset(waves)["WTMP_surface"] - 273.15  #convert to deg C

    nowaves_in = xr.open_mfdataset(nowaves)["WTMP_surface"] - 273.15 #convert to deg C
    
    print(waves_in)
    print(nowaves_in)

    #calculate the difference between waves and no waves
    diff = waves_in - nowaves_in

    #subset into weekly periods (the first two and last two weeks of the period) and calculate the mean for each week (and make datarray for graphing but selecing var)
    month1 = diff.sel(time = slice(YEAR + "-11-01", YEAR + "-11-30")).mean(dim = "time")
    month2 = diff.sel(time = slice(YEAR + "-12-01", YEAR + "-12-31")).mean(dim = "time")
    month3 = diff.sel(time = slice(YEAR2 + "-01-01", YEAR2 + "-01-30")).mean(dim = "time")

    #find overall data min and max for consistent contours and single colorbar
    vmin = -2.0
    vmax = 2.0

    levs = cont_levels.cont_levels(vmin, vmax, 15)
    
    #perform t testing to plot statistical significance
    m1_pvals = monthly_ttest.monthly_ttest("SST", YEAR, "11", 0.05)
    m2_pvals = monthly_ttest.monthly_ttest("SST", YEAR, "12", 0.05)
    m3_pvals = monthly_ttest.monthly_ttest("SST", YEAR2, "01", 0.05)
    
    mpl.rcParams["hatch.linewidth"] = 0.5

    #plot
    fig, axs = plt.subplots(nrows = 3, ncols = 1, subplot_kw = {"projection": ccrs.PlateCarree()})

    ax1 = axs[0].contourf(month1.longitude, month1.latitude, month1, levels = levs, vmin = vmin, vmax = vmax, transform = ccrs.PlateCarree(), cmap = "Spectral_r")
    axs[0].contourf(m1_pvals.longitude, m1_pvals.latitude, m1_pvals, colors = "none", transform = ccrs.PlateCarree(), hatches = ["/"*10])
    axs[0].coastlines()
    axs[0].gridlines(draw_labels = {"left": "y"}, linestyle = "--", linewidth = 0.5)
    axs[0].set_title("November " + YEAR, loc = "left")

    ax2 = axs[1].contourf(month2.longitude, month2.latitude, month2, levels = levs, vmin = vmin, vmax = vmax, transform = ccrs.PlateCarree(), cmap = "Spectral_r")
    axs[1].contourf(m2_pvals.longitude, m2_pvals.latitude, m2_pvals, colors = "none", transform = ccrs.PlateCarree(), hatches = ["/"*10])
    axs[1].coastlines()
    axs[1].gridlines(draw_labels = {"left": "y"}, linestyle = "--", linewidth = 0.5)
    axs[1].set_title("December " + YEAR, loc = "left")

    ax3 = axs[2].contourf(month3.longitude, month3.latitude, month3, levels = levs, vmin = vmin, vmax = vmax, transform = ccrs.PlateCarree(), cmap = "Spectral_r", extend = "both")
    axs[2].contourf(m3_pvals.longitude, m3_pvals.latitude, m3_pvals, colors = "none", transform = ccrs.PlateCarree(), hatches = ["/"*10])
    axs[2].coastlines()
    axs[2].gridlines(draw_labels = {"bottom": "x", "left": "y"}, linestyle = "--", linewidth = 0.5)
    axs[2].set_title("January " + YEAR2, loc = "left")

    plt.colorbar(ax3, ax = axs, location = "right", label = "deg C", extend = "both")

    fig.suptitle("Difference in Sea Surface Temperatures (waves - no waves) " + YEAR)

    plt.savefig("SST" + YEAR + "monthly.png")

if __name__ == "__main__":
    main()


