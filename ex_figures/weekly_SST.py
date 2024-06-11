#!/usr/bin/env python3

######################################
#Author: Lucas Jones, Hollings Scholar Intern at NOAA EMC
#Date: 6/11/24
######################################

#This program will create weekly plots of GEFS SST output initialized at 19971101 both with and with out waves for comparison

import xarray as xr
import matplotlib.pyplot as plt
import datetime as dt
import cartopy.crs as ccrs

def main():
    
    path_wave = "/work2/noaa/marine/ljones/30day_tests/Nov97_S2SW/COMROOT/Nov97_S2SW/gefs.19971101/00/mem000/products/ocean/netcdf/*.nc"
    path_nowave = "/work2/noaa/marine/ljones/30day_tests/Nov97_S2S/COMROOT/Nov97_S2S/gefs.19971101/00/mem000/products/ocean/netcdf/*.nc"

    #read in data from multiple files
    wave_in = xr.open_mfdataset(path_wave, use_cftime = True)
    nowave_in = xr.open_mfdataset(path_nowave)
    
    #subset
    waveSST = wave_in["SST"] - 273.15
    nowaveSST = nowave_in["SST"] - 273.15

    #use groupby() to break into weekly chunks.  Note: warning about deprication of time.week expected here, possible other fix: https://github.com/pydata/xarray/discussions/6375
    weekly_wave = waveSST.convert_calendar(calendar = "standard").groupby("time.week").mean()
    weekly_nowave = nowaveSST.convert_calendar(calendar = "standard").groupby("time.week").mean()

    #calculate differences between with and without waves by week
    diff_weekly = weekly_wave - weekly_nowave
    week1 = diff_weekly[0]
    week2 = diff_weekly[1]
    week3 = diff_weekly[2]
    week4 = diff_weekly[3]
    week5 = diff_weekly[4]

    fig, ax = plt.subplots(nrows = 2, ncols = 3, subplot_kw = {"projection": ccrs.PlateCarree()})

    ax1 = ax[0][0].contourf(week1.xh, week1.yh, week1, transform = ccrs.PlateCarree(), cmap = "seismic")
    ax[0][0].coastlines()
    ax[0][0].set_title("Week 1")
    fig.colorbar(ax1, location = "bottom", extend = "both", label = "deg C")

    ax2 = ax[0][1].contourf(week2.xh, week2.yh, week2, transform = ccrs.PlateCarree(), cmap = "seismic")
    ax[0][1].coastlines()
    ax[0][1].set_title("Week 2")
    fig.colorbar(ax2, location = "bottom", extend = 'both', label = "deg C")

    ax3 = ax[0][2].contourf(week3.xh, week3.yh, week3, transform = ccrs.PlateCarree(), cmap = "seismic")
    ax[0][2].coastlines()
    ax[0][2].set_title("Week 3")
    fig.colorbar(ax3, location = "bottom", extend = "both", label = "deg C")

    ax4 = ax[1][0].contourf(week4.xh, week4.yh, week4, transform = ccrs.PlateCarree(), cmap = "seismic")
    ax[1][0].coastlines()
    ax[1][0].set_title("Week 4")
    fig.colorbar(ax4, location = 'bottom', extend = "both", label = "deg C")

    ax5 = ax[1][1].contourf(week5.xh, week5.yh, week5, transform = ccrs.PlateCarree(), cmap = "seismic")
    ax[1][1].coastlines()
    ax[1][1].set_title("Week 5")
    fig.colorbar(ax5, location = "bottom", extend = "both", label = "deg C")

    plt.savefig("Weekly_SST.png")
    

if __name__ == "__main__":
    main()
