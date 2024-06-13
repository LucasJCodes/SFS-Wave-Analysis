#!/usr/bin/env python3

#SBATCH -J runpy
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

def main():

    path = "/work2/noaa/marine/ljones/30day_tests/Nov20_S2S/COMROOT/Nov20_S2S/gefs.20201101/00/mem000/products/atmos/grib2/1p00/gefs.t00z.pgrb2b.1p00.f***.nc"

    ds = xr.open_mfdataset(path)

    #subset data to get 850 hPa heights only
    data_850 = ds["HGT_850"]
    print(data_850)

    #slice into 7 day periods (14 days after initialization and 14 days leading up to model run end


if __name__ == "__main__":
    main()
