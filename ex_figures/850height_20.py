#!/usr/bin/env python3

#SBATCH -J 850height_20.py
#SBATCH -o outfile
#SBATCH -e errorfile
#SBATCH -q debug
#SBATCH -A marine-cpu
#SBATCH --ntasks=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=0
#SBATCH -t 05:00

###############################
#Author: Lucas Jones, Hollings Scholar Intern at NOAA EMC
#Date: 6/12/24
###############################

import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import pandas as pd

def main():

    path_nowave = "/work2/noaa/marine/ljones/30day_tests/Nov20_S2S/COMROOT/Nov20_S2S/gefs.20201101/00/mem000/products/atmos/grib2/1p00/gefs.t00z.pgrb2b.1p00.f***.nc"
    path_wave = "/work2/noaa/marine/ljones/30day_tests/Nov20_S2SW/COMROOT/Nov20_S2SW/gefs.20201101/00/mem000/products/atmos/grib2/1p00/gefs.t00z.pgrb2b.1p00.f***.nc"

    ds_nowave = xr.open_mfdataset(path_nowave)
    ds_wave = xr.open_mfdataset(path_wave)

    #subset data to get 850 hPa heights only
    nowave_850 = ds_nowave["HGT_850mb"]
    wave_850 = ds_wave["HGT_850mb"]

    #slice into 7 day periods (14 days after initialization and 14 days leading up to model run end
    now1 = nowave_850.sel(time = slice("2020-11-01", "2020-11-07")).mean(dim = "time")
    now2 = nowave_850.sel(time = slice("2020-11-08", "2020-11-14")).mean(dim = "time")
    now3 = nowave_850.sel(time = slice("2020-11-18", "2020-11-24")).mean(dim = "time")
    now4 = nowave_850.sel(time = slice("2020-11-25", "2020-12-01")).mean(dim = "time")
    
    w1 = wave_850.sel(time = slice("2020-11-01", "2020-11-07")).mean(dim = "time")
    w2 = wave_850.sel(time = slice("2020-11-08", "2020-11-14")).mean(dim = "time")
    w3 = wave_850.sel(time = slice("2020-11-18", "2020-11-24")).mean(dim = "time")
    w4 = wave_850.sel(time = slice("2020-11-25", "2020-11-01")).mean(dim = "time")

    #calculate differnces for plotting
    diff1 = w1 - now1
    diff2 = w2 - now2
    diff3 = w3 - now3
    diff4 = w4 - now4

    #plot the differences
    fig, axs = plt.subplots(nrows = 2, ncols = 2, subplot_kw = {"projection": ccrs.PlateCarree()})

    ax1 = axs[0][0].contourf(diff1.longitude, diff1.latitude, diff1, transform = ccrs.PlateCarree())
    axs[0][0].coastlines()

    ax2 = axs[0][1].contourf(diff2.longitude, diff2.latitude, diff2, transform = ccrs.PlateCarree())
    axs[0][1].coastlines()

    ax3 = axs[1][0].contourf(diff3.longitude, diff3.latitude, diff3, transform = ccrs.PlateCarree())
    axs[1][0].coastlines()

    ax4 = axs[1][1].contourf(diff4.longitude, diff4.latitude, diff4, transform = ccrs.PlateCarree())
    axs[1][1].coastlines()

    plt.savefig("pres850_comp.png")

if __name__ == "__main__":
    main()
