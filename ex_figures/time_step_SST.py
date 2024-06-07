#!/usr/bin/env python3

# This program creates 8 plots of SST  from a gefs run initialized at 19181101, running for 48 hours.  One plot will be put on the same figure for each day

import xarray as xr
import glob
import matplotlib.pyplot as plt
import cartopy.crs as ccrs

def main():
    
    # constants holding the arbitrary number of rows and columns in the figure
    ROWS = 4
    COLS = 2
    # read in all ocean files from the model run 
    path = "/work2/noaa/marine/ljones/test01/t05/COMROOT/t05/gefs.19971101/00/mem000/products/ocean/grib2/1p00/"
    files = glob.glob(path + "/*.nc")

    # prepare figure, axes for plotting
    fig, ax = plt.subplots(ROWS, COLS, subplot_kw = {"projection": ccrs.Robinson()})

    # perform seven iterations, loading in data forward in time and then plotting
    for file in files:
        
        # read data in and subset
        data_in = xr.load_dataset(file)
        data2d = data_in.isel(time = 0)
        SST = data2d["WTMP_surface"]
        #print(SST)
        
        # plot each file on its own ax

        # creates i, j variables to determine the row and column to plot in
        curr_i = files.index(file)

        if curr_i > ROWS - 1:
            i = curr_i - ROWS
            j = 1

        else:
            i = curr_i
            j = 0

        test = ax[i][j].contourf(SST, transform = ccrs.Robinson())
        ax[i][j].coastlines()

    plt.savefig("SST_time_step.png")
        

if __name__ == "__main__":
    main()
