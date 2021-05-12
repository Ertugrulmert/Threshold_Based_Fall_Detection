"""
Author: Mert Ertuğrul 
Date: 12.05.2021

utilities.py : Contains helper functions used to prepare, display, analyze accelerometer data
"""

import os
import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

"""
Reads and converts the 3-axis accelerometer data into a usable format
Returns time series array
"""
def prepare_data(file_path, sampling_frequency=200, resolution=13, g_range=32, plot_data=False):

	time_series = []

	#reading and processing file
	with open(file_path) as file:
    for line in file:
    	#makes sure that the line is not empty
        if len(line) > 8:

			#Acceleration [g]: [(2*Range)/(2^Resolution)] * Acceleration Data
            time_series.append([ ( (2*g_range)/(2^resolution) ) * int(num)/1000 for num in line.split(",")[:3] ] )

    time_series = np.array(time_series)   

    if plot_data:
    	plt.figure(figsize=(20,10))
		plt.plot(time_series[:,0], label="x axis")
		plt.plot(time_series[:,1], label="y axis")
		plt.plot(time_series[:,2], label="z axis")
		plt.legend(loc=(1.04,0.5))
		plt.title("3-Axial Acceleration Data")

	return time_series

"""
Returns vector magnitude of given array
"""
def get_vector_mag(arr):
    return math.sqrt( sum(i**2 for i in arr) )

"""
Returns vector magnitude time series of given 3-axial acceleration time series
"""
def get_mag_series(time_series, plot_data=False):
	mag_series = np.array( [get_vector_mag(xyz) for xyz in time_series] )
	
	if plot_data:
    	plt.figure(figsize=(20,10))
		plt.plot(mag_series)
		plt.title("Acceleration Vector Magintude Data")