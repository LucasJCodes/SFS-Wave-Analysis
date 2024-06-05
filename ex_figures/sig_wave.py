#!/usr/bin/env python3

#This program retrieves data from a the 19971101 IC, 30 day run of the gefs and graph significant wave height 

import xarray as xr
import cartopy.crs as ccrs
import matplotlib.pyplot as plt

def main():

    path = "/work2/noaa/marine/ljones/test01/t05/COMROOT/t05/gefs.19971101/00/mem000/products/wave/gridded/"
    file = "gefswave.t00z.global.1p00.f006.grib2.nc"
    
    data_in = xr.load_dataset(path + file)

    #subset to get significant wave height  
    data2d = data_in.isel(time = 0)
    sig_wave = data2d["HTSGW_surface"]

    fig, ax = plt.subplots(nrows = 1, ncols = 1)

    ax.contourf(sig_wave[0:168])
    #ax.coastlines()
    
    plt.savefig("fig_sigwave.png")

if __name__ == "__main__":
    main()
