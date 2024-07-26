#!/usr/bin/env python3

#SBATCH -J 850height_members.py
#SBATCH -o 850height_mem_out
#SBATCH -e 850height_mem_error
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

    STARTYEAR = "2015"
    STARTMONTH = "12"
    STARTDAY = "01"
    ENDYEAR = "2015"
    ENDMONTH = "12"
    ENDDAY = "31"
    OUT_FILE = "/monthly/850Height" + STARTYEAR + STARTMONTH + ".nc"

    #The filepaths for each model output data
    updir = "/work2/noaa/marine/ljones/90day_experiments/no_waves/WAVETEST_" + STARTYEAR + "110100_S2S/gefs." + STARTYEAR + "1101/00/"
    sub = "/products/atmos/grib2/1p00/gefs.t00z.pgrb2b.1p00.f*.nc"

    filelist = []

    for i in range(0, 11):
        if i >= 10:
            filelist.append(updir + "mem0" + str(i) + sub)

        else:
            filelist.append(updir + "mem00" + str(i) + sub)

    #call the method to handle ensemble file creation for each grouping
    members_ds.members_ds(filelist, OUT_FILE, "HGT_850mb", STARTYEAR + "-" + STARTMONTH + "-" + STARTDAY, ENDYEAR + "-" + ENDMONTH + "-" + ENDDAY)

if __name__ == "__main__":
    main()

