#!/bin/bash

#SBATCH -J g2nc.sh
#SBATCH -o tutorial.o%J
#SBATCH -A marine-cpu
#SBATCH --ntasks=1
#SBATCH --ntasks-per-node=1 
#SBATCH --cpus-per-task=1
#SBATCH --mem=0
#SBATCH -t 1:00:00


#Script to convert grib2 files to netcdf
files='/work/noaa/marine/nbarton/RUNS/COMROOT/WAVETEST_1997110100_S2SW/gefs.19971101/00/mem000/products/ocean/grib2/1p00/gefs.ocean.t00z.1p00.f*.grib2'
ndir='/work/noaa/marine/nbarton/RUNS/COMROOT/WAVETEST_1997110100_S2SW/gefs.19971101/00/mem000/products/ocean/grib2/1p00/'
out_dir='/work2/noaa/marine/ljones/90day_experiments/waves/WAVETEST_1997110100_S2SW/gefs.19971101/00/mem000/products/ocean/grib2/1p00'

cd ${ndir}
files=`ls gefs.ocean.t00z.1p00.f*.grib2`

mkdir -p ${out_dir}
cd $out_dir

for file in $files
do
        wgrib2 ${ndir}/${file} -netcdf ${file}.nc
	echo ${ndir} -netcdf ${file}.nc
done
