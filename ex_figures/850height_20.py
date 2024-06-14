#!/usr/bin/env python3

#SBATCH -J runpy
#SBATCH -o outfile
#SBATCH -e errorfile
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

def main():

    path_nowave = "/work2/noaa/marine/ljones/30day_tests/Nov20_S2S/COMROOT/Nov20_S2S/gefs.20201101/00/mem000/products/atmos/grib2/1p00/gefs.t00z.pgrb2b.1p00.f***.nc"
    path_wave = "/work2/noaa/marine/ljones/30day_tests/Nov20_S2SW/COMROOT/Nov20_S2SW/gefs.20201101/00/mem000/products/atmos/grib2/1p00/gefs.t00z.pgrb2b.1p00.f***.nc"

    ds_nowave = xr.open_mfdataset(path_nowave)
    ds_wave = xr.open_mfdataset(path_wave)

    #subset data to get 850 hPa heights only
    nowave_850 = ds_nowave["HGT_850mb"]
    wave_850 = ds_wave["HGT_850mb"]

    #slice into 7 day periods (14 days after initialization and 14 days leading up to model run end
    now_week1 = nowave_850.sel(time = slice("2020-11-01", "2020-11-07"))
    now_week2 = nowave_850.sel(time = slice("2020-11-8", "2020-11-14"))
    now_week3 = nowave_850.sel(time = slice("2020-11-18", "2020-11-24"))
    now_week4 = nowave_850.sel(time = slice("2020-11-25", "2020-12-01"))
    
    w_week1 = wave_850.sel(time = slice("2020-11-01", "2020-11-07"))

    #calculate differnces for plotting
    diff1 = w_week1 - now_week1

    #plot the differences
    fig, axs = plt.subplots(nrows = 2, ncols = 2, subplot_kw = {"projection": ccrs.PlateCarree()})

    ax1 = axs[0][0].contourf(diff1.xh, diff1.yh, diff1, transform = ccrs.PlateCarree())

    plt.savefig("pres850_comp.png")

if __name__ == "__main__":
    main()
