#!/usr/bin/env python3

###################################
#Author: Lucas Jones, Hollings Scholar Intern at NOAA EMC
#Date: 5/11/24
##################################

#Simple program to test plotting from the OSTIA data set.  

import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs

def main():

    path = "/work2/noaa/marine/jmeixner/ReferenceData/sst_OSTIA/0p05/2020/202011**-UKMO-L4HRfnd-GLOB-v01-fv02-OSTIA.nc"
    
    ds = xr.open_mfdataset(path)

    sst = ds["analysed_sst"] - 273.15  #in deg C

    weekly_sst = sst.groupby("time.week").mean()
    week1 = weekly_sst[0]
    week2 = weekly_sst[1]
    week3 = weekly_sst[2]
    week4 = weekly_sst[3]
    week5 = weekly_sst[4]
    week6 = weekly_sst[5]
    
    fig, ax  = plt.subplots(nrows = 3, ncols = 2, subplot_kw = {"projection": ccrs.PlateCarree()})
    
    ax1 = ax[0][0].contourf(week1.lon, week1.lat, week1, transform = ccrs.PlateCarree())
    ax[0][0].coastlines()
    ax[0][0].set_title("Week 1")
    cbar1 = plt.colorbar(ax1, extend = "both")
    
    ax2 = ax[0][1].contourf(week2.lon, week2.lat, week2, transform = ccrs.PlateCarree())
    ax[0][1].coastlines()
    ax[0][1].set_title("Week 2")
    cbar2 = plt.colorbar(ax2, extend = "both")
    
    ax3 = ax[1][0].contourf(week3.lon, week3.lat, week3, transform = ccrs.PlateCarree())
    ax[1][0].coastlines()
    ax[1][0].set_title("Week 3")
    cbar3 = plt.colorbar(ax3, extend = "both")

    ax4 = ax[1][1].contourf(week4.lon, week4.lat, week4, transform = ccrs.PlateCarree())
    ax[1][1].coastlines()
    ax[1][1].set_title("Week 4")
    cbar4 = plt.colorbar(ax4, extend = "both")

    ax5 = ax[2][0].contourf(week5.lon, week5.lat, week5, transform = ccrs.PlateCarree())
    ax[2][0].coastlines()
    ax[2][0].set_title("Week 5")
    cbar5 = plt.colorbar(ax5, extend = "both")

    ax6 = ax[2][1].contourf(week6.lon, week6.lat, week6, transform = ccrs.PlateCarree())
    ax[2][1].coastlines()
    ax[2][1].set_title("Week 6")
    cbar6 = plt.colorbar(ax6, extend = "both")

    plt.savefig("OSTIA_weekly.png")

if __name__ == "__main__":
    main()
