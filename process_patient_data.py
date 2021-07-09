import utilities, threshold_based_model
from pandas import *
import numpy as np
import matplotlib.pyplot as plt


"""
Processes a patient's accelerometer data given its csv file path
Detects and displays (optional) fall events
"""

def process_patient_data(patient_csv_path, display_graphs = False):
    
    # Reads the patient file into Pandas dataframe
    
    patient_data = read_csv(patient_csv_path, sep=';')

    
    # Converts teh dataframe to time series consisting of 
    # acceleration data from the 3 axes over time

    time_series_patient = utilities.get_patient_time_series(patient_data, display = display_graphs)
    
    print("---- Fall Detection ----")
    
    # we need to specify the frequency as 100 Hz since the function defaults to 200 otherwise
    patient_result = threshold_based_model.fall_detection(time_series_patient, sampling_freq = 100 )
    
    print( "Number of Fall Events Detected: " + str(len(patient_result)) )
    
    #displaying fall event graphs
    #only displays the data points starting from 200 points before impact 
    #and ending at 1000 points after impact
    
    if display_graphs:
        for event in patient_result:
    
            plt.figure(figsize=(10,5))
        
            magnitude = np.array( [utilities.get_vector_mag(xyz) for xyz in time_series_patient[event[0]-200:event[0]+ 1000] ] )
            
            plt.plot(magnitude, label="magnitude")
            plt.plot(time_series_patient[event[0]-200:event[0]+ 1000,0], label="x axis")
            plt.plot(time_series_patient[event[0]-200:event[0]+ 1000,1], label="y axis")
            plt.plot(time_series_patient[event[0]-200:event[0]+ 1000,2], label="z axis")
            plt.axvline(x=200, ymin=-6, ymax=6, c = 'k',linewidth=1, label="Impact" )
            plt.legend(loc=(1.04,0.5))
            plt.title("Fall Event")
        
if __name__ == '__main__':
    
    patient1_path = "patient_data\hasta1.csv"
    patient2_path = "patient_data\hasta2.csv"
    patient4_path = "patient_data\hasta4.csv"
    
    print("\n---- Patient 1 ----")
    process_patient_data(patient_csv_path = patient1_path , display_graphs = False )
    
    print("\n---- Patient 2 ----")
    process_patient_data(patient_csv_path = patient2_path , display_graphs = False )
    
    print("\n---- Patient 4 ----")
    process_patient_data(patient_csv_path = patient4_path , display_graphs = False )