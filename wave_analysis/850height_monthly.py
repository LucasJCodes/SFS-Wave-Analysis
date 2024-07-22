#!/usr/bin/env python3

#SBATCH -J 850height_monthly.py
#SBATCH -o 850height_monthly_out
#SBATCH -e 850height_monthly_error
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

from metplot import data_range
import cartopy.crs as ccrs
from metplot import cont_levels
import matplotlib as mpl
import matplotlib.pyplot as plt
from stats import monthly_ttest
import xarray as xr

def main():
    
    YEAR = "2020"
    YEAR2 = "2021"

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
    month1 = diff.sel(time = slice(YEAR + "-11-01", YEAR + "-11-30")).mean(dim = "time")
    month2 = diff.sel(time = slice(YEAR + "-12-01", YEAR + "-12-31")).mean(dim = "time")
    month3 = diff.sel(time = slice(YEAR2 + "-01-01", YEAR2 + "-01-31")).mean(dim = "time")

    #set the range for the data so the contour levels and colorbar are the same
    vmin = -120 #data_range.data_range(diff)
    vmax = 120

    levels = cont_levels.cont_levels(vmin, vmax, 15)

    #perform t testing to plot statistical significance
    m1_pvals = monthly_ttest.monthly_ttest("850Height", YEAR, "11", 0.05)
    m2_pvals = monthly_ttest.monthly_ttest("850Height", YEAR, "12", 0.05)
    m3_pvals = monthly_ttest.monthly_ttest("850Height", YEAR2, "01", 0.05)

    mpl.rcParams["hatch.linewidth"] = 0.5    

    #plot the differences
    fig, axs = plt.subplots(nrows = 3, ncols = 1, subplot_kw = {"projection": ccrs.PlateCarree()})
    fig.suptitle("Difference in 850hPa Geopotential Height (waves - no waves)", fontsize = 12)

    ax1 = axs[0].contourf(month1.longitude, month1.latitude, month1, levels = levels, vmin = vmin, vmax = vmax, transform = ccrs.PlateCarree(), cmap = "seismic")
    axs[0].contourf(m1_pvals.longitude, m1_pvals.latitude, m1_pvals, colors = "none", transform = ccrs.PlateCarree(), hatches = ["/"*10])
    axs[0].coastlines()
    axs[0].gridlines(draw_labels = {"left": "y"}, linestyle = "--", linewidth = 0.5)
    axs[0].set_title("November " + YEAR, loc = "left")

    ax2 = axs[1].contourf(month2.longitude, month2.latitude, month2, levels = levels, vmin = vmin, vmax = vmax, transform = ccrs.PlateCarree(), cmap = "seismic")
    axs[1].contourf(m2_pvals.longitude, m2_pvals.latitude, m2_pvals, colors = "none", transform = ccrs.PlateCarree(), hatches = ["/"*10])
    axs[1].coastlines()
    axs[1].gridlines(draw_labels = {"left": "y"}, linestyle = "--", linewidth = 0.5)
    axs[1].set_title("December " + YEAR, loc = "left")

    ax3 = axs[2].contourf(month3.longitude, month3.latitude, month3, levels = levels, vmin = vmin, vmax = vmax, transform = ccrs.PlateCarree(), cmap = "seismic")
    axs[2].contourf(m3_pvals.longitude, m3_pvals.latitude, m3_pvals, colors = "none", transform = ccrs.PlateCarree(), hatches = ["/"*10])
    axs[2].coastlines()
    axs[2].gridlines(draw_labels = {"bottom": "x", "left": "y"}, linestyle = "--", linewidth = 0.5)
    axs[2].set_title("January " + YEAR2, loc = "left")

    fig.colorbar(ax3, ax = axs, extend = "both", location = "right", label = "meters")

    plt.savefig("850height" + YEAR + "monthly.png")

if __name__ == "__main__":
    main()
