#!/usr/bin/env python3

#SBATCH -J mldepth_members.py
#SBATCH -o mldepth_mem_out
#SBATCH -e mldepth_mem_error
#SBATCH -A marine-cpu
#SBATCH --ntasks=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=0
#SBATCH -t 4:00:00

############################
#Author: Lucas Jones, Hollings Scholar Intern at NOAA EMC
#Date: 7/17/24
############################

#This program calls functions to create a file with the weekly mean for each model member of model
#outputted ocean mixed layer depth for different initial conditions.
#Data file paths for each intial condition are manually loaded.

import sys
sys.path.append("/work2/noaa/marine/ljones/SFS-Wave-Analysis/wave_analysis")

from readio import members_ds

def main():

    STARTYEAR = "2021"
    STARTMONTH = "01"
    STARTDAY = "01"
    ENDYEAR = "2021"
    ENDMONTH = "01"
    ENDDAY = "30"
    OUT_FILE = "monthly/MLD" + STARTYEAR + STARTMONTH + ".nc"

    #The filepaths for each model output data
    updir = "/work2/noaa/marine/ljones/90day_experiments/no_waves/WAVETEST_" + "2020" + "110100_S2S/gefs." + "2020" + "1101/00/"
    sub = "/products/ocean/grib2/1p00/gefs.ocean.t00z.1p00.f*.grib2.nc"

    filelist = []

    for i in range(0, 11):
        if i >= 10:
            filelist.append(updir + "mem0" + str(i) + sub)

        else:
            filelist.append(updir + "mem00" + str(i) + sub)

    #call the method to handle ensemble file creation for each grouping
    members_ds.members_ds(filelist, OUT_FILE, "WDEPTH_mixedlayerdepth", STARTYEAR + "-" + STARTMONTH + "-" + STARTDAY, ENDYEAR + "-" + ENDMONTH + "-" + ENDDAY)

if __name__ == "__main__":
    main()

