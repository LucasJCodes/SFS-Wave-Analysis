#!/usr/bin/env python3

#This program will create weekly plots of GEFS SST output initialized at 19971101 both with and with out waves for comparison

import xarray as xr
import matplotlib.pyplot as plt

def main():
    
    path_wave = "/work2/noaa/marine/ljones/30day_tests/Nov97_S2SW/COMROOT/Nov97_S2SW/gefs.19971101/00/mem000/products/ocean/netcdf/*.nc"
    path_nowave = "/work2/noaa/marine/ljones/30day_tests/Nov97_S2S/COMROOT/Nov97_S2S/gefs.19971101/00/mem000/products/ocean/netcdf/*.nc"

    #read in data from multiple files
    wave_in = xr.open_mfdataset(path_wave)
    nowave_in = xr.open_mfdataset(path_nowave)
    
    print(wave_in)

if __name__ == "__main__":
    main()
