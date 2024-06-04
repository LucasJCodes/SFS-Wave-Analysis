#!/usr/bin/env python3

# plot global lat and lon lines from GEFS model output to show tripolar grid

import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from emcpy.plots.map_plots import MapGridded
from emcpy.plots import CreatePlot, CreateFigure 

def main():

    path = "/work2/noaa/marine/ljones/experiments/timing/COMROOT/timing/gefs.20230123/00/mem000/model_data/ocean/history/"
    filename = "gefs.ocean.t00z.6hr_avg.f009.nc"

    data_in = xr.load_dataset(path + filename)
    lat = data_in["geolat"]

    fig = plt.figure() 
    ax = fig.add_subplot(1, 1, 1, projection = ccrs.PlateCarree())

    ax.set_global()
    ax.coastlines()

    ax.contourf(lat["xh"], lat["yh"], lat)

    plt.savefig("lat.png")

if __name__ == "__main__":
    main()
