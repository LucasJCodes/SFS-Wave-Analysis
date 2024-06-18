#!/usr/bin/env python3

#SBATCH -J 15weekly_OSTIA.py
#SBATCH -o 15weekly_OSTIA_out
#SBATCH -e 15weekly_OSTIA_error
#SBATCH -q debug
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

    #constants holding the number of rows and columns in the final figure (used outside figure creation)
    NROWS = 3
    NCOLS = 4

    ostia_path = "/work2/noaa/marine/jmeixner/ReferenceData/sst_OSTIA/1p00/daily/sst_OSTIA.20151*****.1p00.nc" 
    nowave_path = "/work2/noaa/marine/ljones/30day_tests/Nov15_S2S/COMROOT/Nov15_S2S/gefs.20151101/00/mem000/products/ocean/netcdf/*.nc"
    wave_path = "/work2/noaa/marine/ljones/30day_tests/Nov15_S2SW/COMROOT/Nov15_S2SW/gefs.20151101/00/mem000/products/ocean/netcdf/*.nc"

    #read the data in
    ostia_in = xr.open_mfdataset(ostia_path).rename({"lat": "yh", "lon": "xh"}).sel(time = slice("2015-11-01", "2015-12-02"))
    wave_in = xr.open_mfdataset(wave_path)
    nowave_in = xr.open_mfdataset(nowave_path)

    #subset the model data with more that SST variables and convert to Celsius
    ostia_ds = ostia_in["analysed_sst"] - 273.15 #deg c
    wave_ds = wave_in["SST"] - 273.15 #deg C
    nowave_ds = nowave_in["SST"] - 273.15 #deg C 
    
    #change the OSTIA data coordinates from 1 to 360 to values from -300 to 60
    ostia_lon = ostia_ds.assign_coords(xh = (ostia_ds.xh - 300))

    #align the datasets so that differnces can be performed
    #ostia_ds, wave_ds, nowave_ds = xr.align(ostia_ds, wave_ds, nowave_ds, join = "right")

    #iterpolate the OSTIA dataset to match the style of the model products
    ostia = ostia_lon.interp_like(wave_ds, method = "linear")

    print(ostia_lon.xh)
    print(wave_ds.xh)
    print(ostia)

    #calculate differences for comparison plots
    wave_no = wave_ds - nowave_ds

    wave_ostia = wave_ds - ostia

    nowave_ostia = nowave_ds - ostia

    #use slice() to put data into non calendar weekly subsets
    wnow1 = wave_no.sel(time = slice("2015-11-01", "2015-11-07")).mean(dim = "time")
    wnow2 = wave_no.sel(time = slice("2015-11-08", "2015-11-14")).mean(dim = "time")
    wnow3 = wave_no.sel(time = slice("2015-11-18", "2015-11-24")).mean(dim = "time")
    wnow4 = wave_no.sel(time = slice("2015-11-25", "2015-12-01")).mean(dim = "time")
    wnow_arr = [wnow1, wnow2, wnow3, wnow4]

    ow1 = wave_ostia.sel(time = slice("2015-11-01", "2015-11-07")).mean(dim = "time")
    ow2 = wave_ostia.sel(time = slice("2015-11-08", "2015-11-14")).mean(dim = "time")
    ow3 = wave_ostia.sel(time = slice("2015-11-18", "2015-11-24")).mean(dim = "time")
    ow4 = wave_ostia.sel(time = slice("2015-11-25", "2015-12-01")).mean(dim = "time")
    ow_arr = [ow1, ow2, ow3, ow4]

    onow1 = nowave_ostia.sel(time = slice("2015-11-01", "2015-11-07")).mean(dim = "time")
    onow2 = nowave_ostia.sel(time = slice("2015-11-08", "2015-11-14")).mean(dim = "time")
    onow3 = nowave_ostia.sel(time = slice("2015-11-18", "2015-11-24")).mean(dim = "time")
    onow4 = nowave_ostia.sel(time = slice("2015-11-25", "2015-12-01")).mean(dim = "time")
    onow_arr = [onow1, onow2, onow3, onow4]

    #set up figure for the plots
    fig, axs = plt.subplots(nrows = NROWS, ncols = NCOLS, subplot_kw = {"projection": ccrs.PlateCarree()})

    #plot wave vs no wave differences
    plts_wnow = []

    for i in range(0, NCOLS):
        p = axs[0][i].contourf(wnow_arr[i].xh, wnow_arr[i].yh, wnow_arr[i], transform = ccrs.PlateCarree())
        plts_wnow.append(p)
    
    #plot wave vs ostia differences
    plts_ow = []

    for j in range(0, NCOLS):
        p = axs[1][j].contourf(ow_arr[j].xh, ow_arr[j].yh, ow_arr[j], transform = ccrs.PlateCarree())
        plts_ow.append(p)

    #plot now wave vs ostia differences 
    plts_onow = []

    for k in range(0, NCOLS):
        p = axs[2][k].contourf(onow_arr[k].xh, onow_arr[k].yh, onow_arr[k], transform = ccrs.PlateCarree())
        plts_onow.append(p)

    plt.savefig("bigcomp_15.png")

if __name__ == "__main__":
    main()
