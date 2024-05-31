#!/usr/bin/env python3

#This is a test Python script
#Let's graph some gridded SSTs from a 01/23/2023 GEFS model run

import xarray as xr
import matplotlib.pyplot as plt
from emcpy.plots.map_plots import MapContour
from emcpy.plots import CreatePlot, CreateFigure

def main():

    path = "/work2/noaa/marine/ljones/experiments/timing/COMROOT/timing/gefs.20230123/00/mem000/model_data/ocean/history/"
    filename = "gefs.ocean.t00z.6hr_avg.f009.nc"

    data = xr.open_dataset(path + filename)

    #subset data to only have SST data
    SST = data["SST"]
    
    SST2d = SST["time" == 0]
    
    #Create a contour plot of the SST data and plot it on a figure
    SST_map = MapContour(SST2d.coords["yh"], SST2d.coords["xh"], SST2d)
    plot = CreatePlot()
    plot.plot_layers = [SST_map]
    plot.projection = "plcarr"
    plot.domain = "global"
    plot.add_xlabel("Longitude")
    plot.add_ylabel("Latitude")
    plot.add_colorbar()

    fig = CreateFigure()
    fig.plot_list = [plot]
    #fig._map_contour(SST_map)
    fig.create_figure()
    fig.save_figure("figure1.png")

if __name__ == "__main__":
    main()
