#!/usr/bin/env python3

# plot global lat and lon lines from GEFS model output to show tripolar grid

import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs 

def main():

    path = "/work2/noaa/marine/ljones/experiments/timing/COMROOT/timing/gefs.20230123/00/mem000/model_data/ocean/history/"
    filename = "gefs.ocean.t00z.6hr_avg.f009.nc"


    #read in data and separate out model lat and lon data
    data_in = xr.load_dataset(path + filename)
    lat = data_in["geolat"]
    lon = data_in["geolon"]

    fig, ax = plt.subplots(nrows = 2, ncols = 1, subplot_kw = {"projection": ccrs.PlateCarree()})

    ax = ax.flatten()

    #contour plot the data
    ax[0].contourf(lat["xh"], lat["yh"], lat, transform = ccrs.PlateCarree())
    ax[1].contourf(lon["xh"], lat["yh"], lon, transform = ccrs.PlateCarree())

    ax[0].coastlines()
    ax[1].coastlines()

    plt.savefig("latlon.png")

if __name__ == "__main__":
    main()
