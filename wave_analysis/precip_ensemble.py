#!/usr/bin/env python3

#SBATCH -J precip_ensemble.py
#SBATCH -o precip_ens_out
#SBATCH -e precip_ens_error
#SBATCH -A marine-cpu
#SBATCH --ntasks=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=0
#SBATCH -t 1:00:00

############################
#Author: Lucas Jones, Hollings Scholar Intern at NOAA EMC
#Date: 7/2/24
############################

#This program calls functions to create a file  with the ensemble mean of model outputted precipitation. It can be run for
#each of the 6 conditions respectively (with and without waves, for years 1997, 2015, 2020)

import sys
sys.path.append("/work2/noaa/marine/ljones/SFS-Wave-Analysis/wave_analysis")

from readio import files_to_ens as fe

def main():
    
    OUT_FILE = "precip1997now_ensemble.nc"

    #The filepaths for each model output data
    updir = "/work2/noaa/marine/ljones/90day_experiments/no_waves/WAVETEST_1997110100_S2S/gefs.19971101/00/" 
    sub = "/products/atmos/grib2/1p00/gefs.t00z.pgrb2.1p00.f*.nc"

    filelist = []

    for i in range(0, 11):
        if i >= 10:
            filelist.append(updir + "mem0" + str(i) + sub)

        else:
            filelist.append(updir + "mem00" + str(i) + sub)

    #call the method to handle ensemble file creation for each grouping
    fe.files_to_ens("APCP_surface", OUT_FILE, filelist)

if __name__ == "__main__":
    main()
