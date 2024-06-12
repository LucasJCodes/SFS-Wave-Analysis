#!/usr/bin/env python3

############################
#Author: Lucas Jones, Hollings Scholar Intern at NOAA EMC
#Date: 6/11/24
############################

import xarray as xr
import datetime as dt
import matplotlib.pyplot as plt
import cartopy.crs as ccrs

def main():

    ostia_path = "/work2/noaa/marine/jmeixner/ReferenceData/sst_OSTIA/0p05/2015/201511**-UKMO-L4HRfnd-GLOB-v01-fv02-OSTIA.nc" 
    wave_path = "/work2/noaa/marine/ljones/30day_tests/Nov15_S2S/COMROOT/Nov15_S2S/gefs.20151101/00/mem000/products/ocean/netcdf/*.nc"
    nowave_path = "/work2/noaa/marine/ljones/30day_tests/Nov15_S2SW/COMROOT/Nov15_S2SW/gefs.20151101/00/mem000/products/ocean/netcdf/*.nc"

    #read the data in
    ostia_in = xr.open_mfdataset(ostia_path)
    wave_in = xr.open_mfdataset(wave_path)
    nowave_in = xr.open_mfdataset(nowave_path)

    #subset the model data with more that SST variables and convert to Celsius
    ostia_ds = ostia_in["analysed_sst"] - 273.15 #deg c
    wave_ds = wave_in["SST"] - 273.15 #deg C
    nowave_ds = nowave_in["SST"] - 273.15 #deg C

    #use groupby() to put data into weekly segments 
    ostia = ostia_in.groupby("time.week").mean()
    ostia2 = ostia_in.convert_calendar(calendar = "standard").groupby("time.week").mean()
    wave = wave_ds.groupby("time.week").mean()
    nowave = nowave_ds.groupby("time.week").mean()

    #side quest: test difference between using conver_calendar() vs without
    print(ostia_ds[45].time)
    print(ostia_ds2[45].time)

    #calculate differences for comparison plots
    waves_no = wave - nowave

    wave_ostia = wave - ostia

    nowave_ostia = nowave - ostia

    #set up figure for the plots
    fig, axs = plt.subplots(nrows = 3, ncols = 5, subplot_kw = {"projection": ccrs.PlateCarree()})

if __name__ == "__main__":
    main()
