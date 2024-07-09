#!/usr/bin/env python3

#SBATCH -J mldepth_ensemble.py
#SBATCH -o mldepth_ens_out
#SBATCH -e mldepth_ens_error
#SBATCH -q debug
#SBATCH -A marine-cpu
#SBATCH --ntasks=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=0
#SBATCH -t 15:00

############################
#Author: Lucas Jones, Hollings Scholar Intern at NOAA EMC
#date: 8/8/24
############################

#This program calculates an ensemble mean for mixed layer depth of the ocean

import sys
sys.path.append("/work2/noaa/marine/ljones/SFS-Wave-Analysis/wave_analysis")

from readio import files_to_ens as fe

def main():

    OUT_FILE = "MLD1997now_ensemble.nc"

    #The filepaths for each model output data
    updir = "/work2/noaa/marine/ljones/90day_experiments/no_waves/WAVETEST_1997110100_S2S/gefs.19971101/00/"
    sub = "/products/ocean/grib2/1p00/gefs.ocean.t00z.1p00.f*.grib2.nc"

    filelist = []

    for i in range(0, 11):
        if i >= 10:
            filelist.append(updir + "mem0" + str(i) + sub)

        else:
            filelist.append(updir + "mem00" + str(i) + sub)

    fe.files_to_ens("WDEPTH_mixedlayerdepth", OUT_FILE, filelist)


if __name__ == "__main__":
    main()
