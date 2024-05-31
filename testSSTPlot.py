#!/usr/bin/env python3

#This is a test Python script
#Let's graph some gridded SSTs from a 01/23/2023 GEFS model run

import xarray as xr
from emcpy.plots.map_plots import MapContour
from emcpy.plots.create_plots import CreateFigure

def main():

    path = "/work2/noaa/marine/ljones/experiments/timing/COMROOT/timing/gefs.20230123/00/mem000/model_data/ocean/history/"
    filename = "ncview gefs.ocean.t00z.6hr_avg.f009.nc"

    data = xr.open_dataset(path + filename)

    #subset data to only have SST data
    SST = data.sel("SST")
    
    #Create a contour plot of the SST data
    SST_map = MapContour(SST.sel("lat"), SST.sel("lon"), SST.sel("SST"))
    fig = CreateFigure()
    fig.map_contour(SST_map).save_figure(path + "figure1")
    fig.close_figure()
