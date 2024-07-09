#!/usr/bin/env python3

#SBATCH -J SST_ensemble.py
#SBATCH -o SST_ens_out
#SBATCH -e SST_ens_error
#SBATCH -q debug
#SBATCH -A marine-cpu
#SBATCH --ntasks=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=0
#SBATCH -t 30:00

############################
#Author: Lucas Jones, Hollings Scholar Intern at NOAA EMC
#Date: 6/24/24
############################

#This program calls functions to create a file  with the ensemble mean of model outputted SSTs for 
#different initial conditions respectively (with and without waves, for years 1997, 2015, 2020).
#Data file paths for each intial condition are manually loaded.

import sys
sys.path.append("/work2/noaa/marine/ljones/SFS-Wave-Analysis/wave_analysis")

from readio import files_to_ens as fe

def main():
    
    OUT_FILE = "SST2020now_ensemble.nc"

    #The filepaths for each model output data
    updir = "/work2/noaa/marine/ljones/90day_experiments/no_waves/WAVETEST_2020110100_S2S/gefs.20201101/00/"
    sub = "/products/ocean/grib2/1p00/gefs.ocean.t00z.1p00.f*.grib2.nc"

    filelist = []

    for i in range(0, 11):
        if i >= 10:
            filelist.append(updir + "mem0" + str(i) + sub)

        else:
            filelist.append(updir + "mem00" + str(i) + sub)

    print(filelist)

    #call the method to handle ensemble file creation for each grouping
    fe.files_to_ens("WTMP_surface", OUT_FILE, filelist)

if __name__ == "__main__":
    main()
