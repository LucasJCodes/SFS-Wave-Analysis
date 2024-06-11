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
    waveSST = wave_in["SST"]
    nowaveSST = nowave_in["SST"]

    #use groupby() to break into weekly chunks.  Note: warning about deprication of time.week expected here, possible other fix: https://github.com/pydata/xarray/discussions/6375
    weekly_wave = waveSST.convert_calendar(calendar = "standard").groupby("time.week").mean()
    weekly_nowave = nowaveSST.convert_calendar(calendar = "standard").groupby("time.week").mean()

    #calculate differences between with and without waves by week
    diff_weekly = weekly_wave - weekly_nowave
    week1 = diff_weekly[0]
    week2 = diff_weekly[1]
    week3 = diff_weekly[2]
    week4 = diff_weekly[3]

    fig, ax = plt.subplots(nrows = 2, ncols = 2, subplot_kw = {"projection": ccrs.PlateCarree()})

    ax[0][0].contourf(week1.longtitude, week1.latitude, week1, transform = ccrs.PlateCarree())

    plt.savefig("Weekly_SST.png")
    

if __name__ == "__main__":
    main()
