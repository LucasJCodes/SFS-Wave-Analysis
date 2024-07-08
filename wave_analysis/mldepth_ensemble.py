#!/usr/bin/env python3

#SBATCH -J mldepth_weekly.py
#SBATCH -o mldepth_weekly_out
#SBATCH -e mldepth_weekly_error
#SBATCH -q debug
#SBATCH -A marine-cpu
#SBATCH --ntasks=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=0
#SBATCH -t 05:00

############################
#Author: Lucas Jones, Hollings Scholar Intern at NOAA EMC
#date: 8/8/24
############################

#This program calculates an ensemble mean for mixed layer depth of the ocean

import sys
sys.path.append("/work2/noaa/marine/ljones/SFS-Wave-Analysis/wave_analysis")

from readio import files_to_ens as fe

def main():

    #The filepaths for each model output data
    #waves 1997
    w1997mem0 = "/work2/noaa/marine/ljones/90day_experiments/waves/WAVETEST_1997110100_S2SW/gefs.19971101/00/mem000/products/ocean/grib2/1p00"
    w1997mem1 = "/work2/noaa/marine/ljones/90day_experiments/waves/WAVETEST_1997110100_S2SW/gefs.19971101/00/mem001/products/ocean/grib2/1p00"
    w1997mem2 = "/work2/noaa/marine/ljones/90day_experiments/waves/WAVETEST_1997110100_S2SW/gefs.19971101/00/mem002/products/ocean/grib2/1p00"
    w1997mem3 = "/work2/noaa/marine/ljones/90day_experiments/waves/WAVETEST_1997110100_S2SW/gefs.19971101/00/mem003/products/ocean/grib2/1p00"
    w1997mem4 = "/work2/noaa/marine/ljones/90day_experiments/waves/WAVETEST_1997110100_S2SW/gefs.19971101/00/mem004/products/ocean/grib2/1p00"
    w1997mem5 = "/work2/noaa/marine/ljones/90day_experiments/waves/WAVETEST_1997110100_S2SW/gefs.19971101/00/mem005/products/ocean/grib2/1p00"
    w1997mem6 = "/work2/noaa/marine/ljones/90day_experiments/waves/WAVETEST_1997110100_S2SW/gefs.19971101/00/mem006/products/ocean/grib2/1p00"
    w1997mem7 = "/work2/noaa/marine/ljones/90day_experiments/waves/WAVETEST_1997110100_S2SW/gefs.19971101/00/mem007/products/ocean/grib2/1p00"
    w1997mem8 = "/work2/noaa/marine/ljones/90day_experiments/waves/WAVETEST_1997110100_S2SW/gefs.19971101/00/mem008/products/ocean/grib2/1p00"
    w1997mem9 = "/work2/noaa/marine/ljones/90day_experiments/waves/WAVETEST_1997110100_S2SW/gefs.19971101/00/mem009/products/ocean/grib2/1p00"
    w1997mem10 = "/work2/noaa/marine/ljones/90day_experiments/waves/WAVETEST_1997110100_S2SW/gefs.19971101/00/mem010/products/ocean/grib2/1p00"

    #waves 2015
    w2015mem0 =
    w2015mem1 =
    w2015mem2 =
    w2015mem3 =
    w2015mem4 =
    w2015mem5 =
    w2015mem6 =
    w2015mem7 =
    w2015mem8 =
    w2015mem9 =
    w2015mem10 =

    #waves 2020
    w2020mem0 =
    w2020mem1 =
    w2020mem2 =
    w2020mem3 =
    w2020mem4 =
    w2020mem5 =
    w2020mem6 =
    w2020mem7 =
    w2020mem8 =
    w2020mem9 =
    w2020mem10 =

    #no waves 1997
    now1997mem0 =
    now1997mem1 =
    #no waves 2015

    #no waves 2020

    #call the method to handle ensemble file creation for each grouping
    fe.files_to_ens("WDEPTH_mixedlayerdepth", "MLD1997w_ensemble.nc", w1997mem0, w1997mem1, w1997mem2, w1997mem3, w1997mem4, w1997mem5, w1997mem6, w1997mem7, w1997mem8, w1997mem9, w1997mem10)

    fe.files_to_ens("WDEPTH_mixedlayerdepth", "MLD1997now_ensemble.nc", now1997mem0, now1997mem1)


if __name__ == "__main__":
    main()
