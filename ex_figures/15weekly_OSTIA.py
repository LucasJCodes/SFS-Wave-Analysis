#!/usr/bin/env python3

#SBATCH -J 15weekly_OSTIA.py
#SBATCH -o 15weekly_OSTIA_out
#SBATCH -e 15weekly_OSTIA_error
#SBATCH -A marine-cpu
#SBATCH --ntasks=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=0
#SBATCH -t 05:00


############################
#Author: Lucas Jones, Hollings Scholar Intern at NOAA EMC
#Date: 6/11/24
############################

import xarray as xr
import datetime as dt
import matplotlib.pyplot as plt
import cartopy.crs as ccrs

def main():

    ostia_path = "/work2/noaa/marine/jmeixner/ReferenceData/sst_OSTIA/1p00/daily/sst_OSTIA.20151*****.1p00.nc" 
    wave_path = "/work2/noaa/marine/ljones/30day_tests/Nov15_S2S/COMROOT/Nov15_S2S/gefs.20151101/00/mem000/products/ocean/netcdf/*.nc"
    nowave_path = "/work2/noaa/marine/ljones/30day_tests/Nov15_S2SW/COMROOT/Nov15_S2SW/gefs.20151101/00/mem000/products/ocean/netcdf/*.nc"

    #read the data in
    ostia_in = xr.open_mfdataset(ostia_path).rename({"lat": "yh", "lon": "xh"})
    wave_in = xr.open_mfdataset(wave_path)
    nowave_in = xr.open_mfdataset(nowave_path)

    #subset the model data with more that SST variables and convert to Celsius
    ostia_ds = ostia_in["analysed_sst"] - 273.15 #deg c
    wave_ds = wave_in["SST"] - 273.15 #deg C
    nowave_ds = nowave_in["SST"] - 273.15 #deg C

    #align the datasets so that differnces can be performed
    ostia_ds, wave_ds, nowave_ds = xr.align(ostia_ds, wave_ds, nowave_ds, join = "left")

    #calculate differences for comparison plots
    wave_no = wave_ds - nowave_ds

    wave_ostia = wave_ds - ostia_ds

    nowave_ostia = nowave_ds - ostia_ds
    
    print(wave_no)
    print(wave_ostia)
    print(nowave_ostia)

    #use slice() to put data into non calendar weekly subsets
    wnow1 = wave_no.sel(time = slice("2015-11-01", "2015-11-07")).mean()
    ow1 = wave_ostia.sel(time = slice("2015-11-01", "2015-11-07")).mean()
    onow1 = nowave_ostia.sel(time = slice("2015-11-01", "2015-11-07")).mean()

    #set up figure for the plots
    fig, axs = plt.subplots(nrows = 3, ncols = 4, subplot_kw = {"projection": ccrs.PlateCarree()})

    #plot wave vs no wave differences 
    #p1 = axs[0][0].contourf(waves_no[1].xh, waves_no[1].yh, waves_no[1], transform = ccrs.PlateCarree())
    #p2 = axs[0][1].contourf(waves_no[2].xh, waves_no[2].yh, waves_no[3], transform = ccrs.PlateCarree())
    #p3 = axs[0][2].contourf(waves_no[3].xh, waves_no[3].yh, waves_no[3], transform = ccrs.PlateCarree())
    #p4 = axs[0][3].contourf(waves_no[4].xh, waves_no[4].yh, waves_no[4], transform = ccrs.PlateCarree())

    #p5 = axs[1][0].contourf(wave_ostia[1].lat, wave_ostia[1].lon, wave_ostia[1], transform = ccrs.PlateCarree())
    #p6 = axs[1][1].contourf(wave_ostia[2].lat, wave_ostia[2].lon, wave_ostia[2], transform = ccrs.PlateCarree())
    #p7 = axs[1][2].contourf(wave_ostia[3].lat, wave_ostia[3].lon, wave_ostia[3], transform = ccrs.PlateCarree())
    #p8 = axs[1][3].contourf(wave_ostia[4].lat, wave_ostia[4].lon, wave_ostia[4], transform = ccrs.PlateCarree())

    plt.savefig("bigcomp_15.png")

if __name__ == "__main__":
    main()
