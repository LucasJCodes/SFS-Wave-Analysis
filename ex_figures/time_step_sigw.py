#!/usr/bin/env python3

# This program creates 7 plots of significant wave height from a gefs run initialized at 19181101, running for 48 hours.  One plot will be put on the same figure for each day

import xarray as xr
import glob
import matplotlib.pyplot as plt
import cartopy.crs as ccrs

def main():

    # read in all sig wave files from the model run 
    path = "/work2/noaa/marine/ljones/test01/t05/COMROOT/t05/gefs.19971101/00/mem000/products/ocean/grib2/1p00"
    files = glob.glob(path + "/*.nc")

    # prepare figure, axes for plotting
    fig, ax = plt.subplots(7, 2, subplot_kw = {"projection": ccrs.PlateCarree()})

    # perform seven iterations, loading in data forward in time and then plotting
    for file in files:
        
        # read data in 
        data_in = xr.load_dataset(file)
        print(data_in)
        

if __name__ == "__main__":
    main()
