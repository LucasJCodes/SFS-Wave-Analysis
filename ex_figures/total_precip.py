#!/usr/bin/env python3

#SBATCH -J precip_diffs.py
#SBATCH -o out_precip
#SBATCH -e error_precip
#SBATCH -q debug
#SBATCH -A marine-cpu
#SBATCH --ntasks=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=0
#SBATCH -t 05:00

############################
#Author: Lucas Jones, Hollings Scholar Intern at NOAA EMC
#Date: 6/24/24
############################

#This program plots the total precipitation from 30 day SFS model runs with IC 2020-11-01 with and without waves for comparison

def main():
    
    path_nowaves = "/work2/noaa/marine/ljones/30day_tests/Nov20_S2S/COMROOT/Nov20_S2S/gefs.20201101/00/mem000/products/atmos/grib2/1p00/gefs.t00z.pgrb2.1p00.f*.nc"
    path_waves = "/work2/noaa/marine/ljones/30day_tests/Nov20_S2SW/COMROOT/Nov20_S2SW/gefs.20201101/00/mem000/products/atmos/grib2/1p00/gefs.t00z.pgrb2.1p00.f*.nc"

    #open and subset the wave data first
    waves_in = xr.open_mfdataset(path_waves)
    waves = waves_in["APCP_surface"] * 1000 / 100**3 * 39.3701 #kg/m^2 to inches using water density 1 g/m^3
    waves_in.close()

    #open and subset the no wave data
    nowaves_in = xr.open_mfdataset(path_nowaves)
    nowaves = nowaves_in["APCP_surface"] * 1000 / 100**3 * 39.3701 #kg/m^2 to inches using water density 1 g/m^c
    nowaves_in.close()

    #ensure datasets are for same time period

    #sum data long time

    #plot sums

if __name__ == "__main__":
    main()
