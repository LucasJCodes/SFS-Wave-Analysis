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
    ostia_in = xr.open_mfdataset(ostia_path).rename({"lat": "yh", "lon": "xh"}).sel(time = slice("2015-11-01", "2015-12-02"))
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

    #use slice() to put data into non calendar weekly subsets
    wnow1 = wave_no.sel(time = slice("2015-11-01", "2015-11-07")).mean(dim = "time")
    wnow2 = wave_no.sel(time = slice("2015-11-08", "2015-11-14")).mean(dim = "time")
    wnow3 = wave_no.sel(time = slice("2015-11-18", "2015-11-24")).mean(dim = "time")
    wnow4 = wave_no.sel(time = slice("2015-11-25", "2015-12-01")).mean(dim = "time")

    ow1 = wave_ostia.sel(time = slice("2015-11-01", "2015-11-07")).mean(dim = "time")
    ow2 = wave_ostia.sel(time = slice("2015-11-08", "2015-11-14")).mean(dim = "time")
    ow3 = wave_ostia.sel(time = slice("2015-11-18", "2015-11-24")).mean(dim = "time")
    ow4 = wave_ostia.sel(time = slice("2015-11-25", "2015-12-01")).mean(dim = "time")

    onow1 = nowave_ostia.sel(time = slice("2015-11-01", "2015-11-07")).mean(dim = "time")
    onow2 = nowave_ostia.sel(time = slice("2015-11-08", "2015-11-14")).mean(dim = "time")
    onow3 = nowave_ostia.sel(time = slice("2015-11-18", "2015-11-24")).mean(dim = "time")
    onow4 = nowave_ostia.sel(time = slice("2015-11-25", "2015-12-01")).mean(dim = "time")

    print(wnow3[30][10].values)

    #set up figure for the plots
    fig, axs = plt.subplots(nrows = 3, ncols = 4, subplot_kw = {"projection": ccrs.PlateCarree()})

    #plot wave vs no wave differences 
    p1 = axs[0][0].contourf(wnow1.xh, wnow1.yh, wnow1, transform = ccrs.PlateCarree())
    p2 = axs[0][1].contourf(wnow2.xh, wnow2.yh, wnow2, transform = ccrs.PlateCarree())
    p3 = axs[0][2].contourf(wnow3.xh, wnow3.yh, wnow3, transform = ccrs.PlateCarree())
    p4 = axs[0][3].contourf(wnow4.xh, wnow4.yh, wnow4, transform = ccrs.PlateCarree())

    p5 = axs[1][0].contourf(ow1.xh, ow1.yh, ow1, transform = ccrs.PlateCarree())
    p6 = axs[1][1].contourf(ow2.xh, ow2.yh, ow2, transform = ccrs.PlateCarree())
    p7 = axs[1][2].contourf(ow3.xh, ow3.yh, ow3, transform = ccrs.PlateCarree())
    p8 = axs[1][3].contourf(ow4.xh, ow4.yh, ow4, transform = ccrs.PlateCarree())

    p9 = axs[2][0].contourf(onow1.xh, onow1.yh, onow1, transform = ccrs.PlateCarree())

    plt.savefig("bigcomp_15.png")

if __name__ == "__main__":
    main()
