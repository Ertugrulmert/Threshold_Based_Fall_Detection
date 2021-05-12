import os
import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import utilities, threshold_based_model

"""
This function searches for the best threshold values that provide the highest sensitivity, specificity and accuracy 
on the entire dataset.
Cross validation was not used for this parameter search, an alternative with cross validation may be implemented next.
"""
def parameter_search(folder_path = "SisFall_dataset", print_logs = False)

    #parameter grid
    impact_grid = [1.75, 2, 2.25, 2.5, 2.75, 3]
    motionless_grid = [0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55]
    angle_grid = [5, 10, 20, 40, 60]

    #parameter sets are evaluated based on sensitivity, specificity and the combination of the two
    max_sensitivity = 0
    max_specificity = 0
    max_accuracy = 0

    sens_results = []
    spec_results = []
    acc_results = []

    sens_params = []
    spec_params = []
    acc_params = []

    correct_detections = 0
    misses = 0
    faulty_detections = 0
    total_ADL = 0
    total_Fall = 0


    for impact_thresh, motionless_thresh, angle_thresh in [( a, b, c) for a in impact_grid for b in motionless_grid for c in angle_grid]:  

        if print_logs:
          print( "Parameters: Impact Threshold: " + str(impact_thresh) 
            + " | Motionless Threshold: " + str(motionless_thresh)
            + " | Angle Threshold: " + str(angle_thresh) )  

        results = threshold_based_model.process_dataset(folder_path="SisFall_dataset", impact_thresh= impact_thresh, 
                                                        motionless_thresh = motionless_thresh, angle_thresh= angle_thresh, print_results = print_logs):
                        
        sensitivity = results["sensitivity"]
        specificity = results["specificity"]
        accuracy = results["accuracy"]

        if sensitivity > max_sensitivity:
            sens_params = ( impact_thresh, motionless_thresh, angle_thresh )
            max_sensitivity = sensitivity
            sens_results = results

        if specificity > max_specificity:
            spec_params = ( impact_thresh, motionless_thresh, angle_thresh )
            max_specificity = specificity
            spec_results = results

        if accuracy > max_accuracy:
            acc_params = ( impact_thresh, motionless_thresh, angle_thresh )
            max_accuracy = accuracy
            acc_results = results
            
            
    print("Parameters for Max Sensitivity: Impact Threshold: " + str(sens_params[0]) 
            + " | Motionless Threshold: " + str(sens_params[1])
            + " | Angle Threshold: " + str(sens_params[2]) )  

    print("Performance for Max Sensitivity: Sensitivity: " + str(sens_results["sensitivity"]) 
            + " | Specificity: " + str(sens_results["specificity"]) 
            + " | Accuracy: " + str(sens_results["accuracy"]) )  

    print("***********************************************")

    print("Parameters for Max Specificity: Impact Threshold: " + str(spec_params[0]) 
            + " | Motionless Threshold: " + str(spec_params[1])
            + " | Angle Threshold: " + str(spec_params[2]) )  

    print("Performance for Max Specificity: Sensitivity: " + str(spec_results["sensitivity"]) 
            + " | Specificity: " + str(spec_results["specificity"]) 
            + " | Accuracy: " + str(spec_results["accuracy"]) )  

    print("***********************************************")

    print("Parameters for Max Accuracy: Impact Threshold: " + str(acc_params[0]) 
            + " | Motionless Threshold: " + str(acc_params[1])
            + " | Angle Threshold: " + str(acc_params[2]) )  

    print("Performance for Max Accuracy: Sensitivity: " + str(acc_results["sensitivity"]) 
            + " | Specificity: " + str(acc_results["specificity"]) 
            + " | Accuracy: " + str(acc_results["accuracy"]) )  