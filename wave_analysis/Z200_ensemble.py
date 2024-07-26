#!/usr/bin/env python3

#SBATCH -J Z200_ensemble.py
#SBATCH -o Z200_ens_out
#SBATCH -e Z200_ens_error
#SBATCH -A marine-cpu
#SBATCH --ntasks=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=0
#SBATCH -t 1:00:00

############################
#Author: Lucas Jones, Hollings Scholar Intern at NOAA EMC
#Date: 7/25/24
############################

#This program calls functions to create a file with the ensemble mean of model outputted 200 hPa zonal wind for
#each of the 6 respective conditions(with and without waves, for years 1997, 2015, 2020)

import sys
sys.path.append("/work2/noaa/marine/ljones/SFS-Wave-Analysis/wave_analysis")

from readio import files_to_ens as fe

def main():
    
    YEAR = "2020"
    OUT_FILE = "Z200" + YEAR + "now_ensemble.nc"

    #The filepaths for each model output data
    updir = "/work2/noaa/marine/ljones/90day_experiments/no_waves/WAVETEST_" + YEAR + "110100_S2S/gefs." + YEAR + "1101/00/" 
    sub = "/products/atmos/grib2/1p00/gefs.t00z.pgrb2b.1p00.f*.nc"

    filelist = []

    for i in range(0, 11):
        if i >= 10:
            filelist.append(updir + "mem0" + str(i) + sub)

        else:
            filelist.append(updir + "mem00" + str(i) + sub)

    #call the method to handle ensemble file creation for each grouping
    fe.files_to_ens("UGRD_200mb", OUT_FILE, filelist)


if __name__ == "__main__":
    main()

