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
    
    #fig, ax = plt.subplots(nrows = 3, ncols = 2, subplot_kw = {"projection": ccrs.PlateCarree()})

if __name__ == "__main__":
    main()
