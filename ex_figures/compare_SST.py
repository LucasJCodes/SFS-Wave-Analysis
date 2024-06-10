#!/usr/bin/env python3

import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs

def read_data(file_path, filename):
    """
    This function takes a file path and file name, reading in the 3 dimensional netCDF data associated with that file.  It then subsets the data correctly for a 2 dimensional dataset and returns an xarray dataset.
    """

    # read in the data
    data_in = xr.load_dataset(file_path + filename)

    # subset 
    data2d = data_in.isel(time = 0) 

    return data2d

def main():
    
    path_waves = "/work2/noaa/marine/ljones/30day_tests/Nov97_S2SW/COMROOT/Nov97_S2SW/gefs.19971101/00/mem000/products/ocean/grib2/1p00/"
    file_waves = "gefs.ocean.t00z.1p00.f714.grib2.nc"

    path_nowave = "/work2/noaa/marine/ljones/30day_tests/Nov97_S2S/COMROOT/Nov97_S2S/gefs.19971101/00/mem000/products/ocean/grib2/1p00/"
    file_nowave = "gefs.ocean.t00z.1p00.f714.grib2.nc"

    #read in and subset the data with read_data
    data_wave = read_data(path_waves, file_waves)
    data_nowave = read_data(path_nowave, file_nowave)
    
    #plot the two data sets
    fig, ax = plt.subplots(nrows = 2, ncols = 2, subplot_kw = {"projection": ccrs.PlateCarree()})

    ax[0][0].contourf(data_wave.longitude, data_wave.latitude, data_wave["WTMP_surface"])

    plt.savefig("97SST_comparison")

if __name__ == "__main__":
    main()
