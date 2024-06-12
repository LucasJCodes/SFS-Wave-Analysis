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
    ostia_in = xr.open_mfdataset(ostia_path) #.rename_dims({"lat": "xh", "lon": "yh"})
    wave_in = xr.open_mfdataset(wave_path)
    nowave_in = xr.open_mfdataset(nowave_path)

    #subset the model data with more that SST variables and convert to Celsius
    ostia_ds = ostia_in["analysed_sst"] - 273.15 #deg c
    wave_ds = wave_in["SST"] - 273.15 #deg C
    nowave_ds = nowave_in["SST"] - 273.15 #deg C

    #use groupby() to put data into weekly segments 
    ostia = ostia_in.convert_calendar(calendar = "standard").groupby("time.week").mean()
    wave = wave_ds.convert_calendar(calendar = "standard").groupby("time.week").mean()
    nowave = nowave_ds.convert_calendar(calendar = "standard").groupby("time.week").mean()

    #calculate differences for comparison plots
    waves_no = wave - nowave

    wave_ostia = wave - ostia

    nowave_ostia = nowave - ostia

    #set up figure for the plots
    fig, axs = plt.subplots(nrows = 3, ncols = 4, subplot_kw = {"projection": ccrs.PlateCarree()})

    #plot wave vs no wave diffs

    print(ostia_in)
    print(wave_in)
    print(nowave_in)
    p1 = axs[0][0].contourf(waves_no[1].xh, waves_no[1].yh, waves_no[1], transform = ccrs.PlateCarree())
    p2 = axs[0][1].contourf(waves_no[2].xh, waves_no[2].yh, waves_no[3], transform = ccrs.PlateCarree())
    p3 = axs[0][2].contourf(waves_no[3].xh, waves_no[3].yh, waves_no[3], transform = ccrs.PlateCarree())
    p4 = axs[0][3].contourf(waves_no[4].xh, waves_no[4].yh, waves_no[4], transform = ccrs.PlateCarree())

    #p5 = axs[1][0].contourf(wave_ostia[1].lat, wave_ostia[1].lon, wave_ostia[1], transform = ccrs.PlateCarree())
    #p6 = axs[1][1].contourf(wave_ostia[2].lat, wave_ostia[2].lon, wave_ostia[2], transform = ccrs.PlateCarree())
    #p7 = axs[1][2].contourf(wave_ostia[3].lat, wave_ostia[3].lon, wave_ostia[3], transform = ccrs.PlateCarree())
    #p8 = axs[1][3].contourf(wave_ostia[4].lat, wave_ostia[4].lon, wave_ostia[4], transform = ccrs.PlateCarree())

    plt.savefig("bigcomp_15.png")

if __name__ == "__main__":
    main()
