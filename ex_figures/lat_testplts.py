#!/usr/bin/env python3

#SBATCH -J lat_testplts.py
#SBATCH -o lonout
#SBATCH -e lonerror
#SBATCH -q debug
#SBATCH -A marine-cpu
#SBATCH --ntasks=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=0
#SBATCH -t 05:00

############################
#Author: Lucas Jones, Hollings Scholar Intern at NOAA EMC
#Date: 6/20/24
############################

import xarray as xr
import datetime as dt
import matplotlib.pyplot as plt
import cartopy.crs as ccrs

def main():

    ostia_path = "/work2/noaa/marine/jmeixner/ReferenceData/sst_OSTIA/1p00/daily/sst_OSTIA.20151*****.1p00.nc"
    wave_path = "/work2/noaa/marine/ljones/30day_tests/Nov15_S2SW/COMROOT/Nov15_S2SW/gefs.20151101/00/mem000/products/ocean/netcdf/*.nc"

    #read the data in
    ostia_in = xr.open_mfdataset(ostia_path).rename({"lat": "yh", "lon": "xh"}).sel(time = slice("2015-11-01", "2015-12-02"))
    wave_in = xr.open_mfdataset(wave_path)

    #subset the model data with more that SST variables and convert to Celsius
    ostia_ds = ostia_in["analysed_sst"] - 273.15 #deg c
    wave_ds = wave_in["SST"] - 273.15 #deg C

    ostia = ostia_ds.sel(time = slice("2015-11-01", "2015-11-07")).mean(dim = "time")
    wave = wave_ds.sel(time = slice("2015-11-01", "2015-11-07")).mean(dim = "time")

    ostia_lon = ostia.assign_coords(xh = (ostia.xh - 360))

    ostia_interp = ostia_lon.interp_like(wave, method = "linear") #kwargs = {"bounds_error": False, "fill_value":  "extrapolate"})

    diff = wave - ostia_interp

    print(ostia_lon)
    print(wave)
    print(ostia_interp)
    print(ostia_interp.min().values)

    fig, axs = plt.subplots(nrows = 3, ncols = 1, subplot_kw = {"projection": ccrs.PlateCarree()})

    axs[0].contourf(ostia_interp.xh, ostia_interp.yh, ostia_interp, transform = ccrs.PlateCarree())
    axs[0].coastlines()
    axs[0].set_title("OSTIA")

    axs[1].contourf(wave.xh, wave.yh, wave, transform = ccrs.PlateCarree())
    axs[1].coastlines()
    axs[1].set_title("GEFS")

    axs[2].contourf(diff.xh, diff.yh, diff, transform = ccrs.PlateCarree())
    axs[2].coastlines()
    axs[2].set_title("Difference")

    plt.savefig("lon_confusion.png")

if __name__ == "__main__":
    main()
