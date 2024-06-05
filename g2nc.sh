#!/bin/bash

#Script to convert grib2 files to netcdf
files='ls *.grb2f0*'

for file in $files
do
        wgrib2 ${file} -netcdf ${file}.nc
done
