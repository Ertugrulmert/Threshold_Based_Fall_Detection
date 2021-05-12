import os
import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import utilities

"""
Threshold Based Fall Detection Algorithm

Stages and correspoding parameters of the algorithm:

( detailed explanation of the algorithm is given in the README file )

●	Impact: 
	impact_thresh (float) : impact is initiated after this threshold is passed, 
							impact ends after magnitude dips below the threshold

●	Post Impact: 
	post_impact_ms (int) : waiting time after the impact 

●	Motionless Period: 
	motionless_thresh (float) : motionless period is violated and fall detecion cancelled if 
								magnitude deviates from 1g by the threshold amount
	post_impact_ms (int) : length of the required motionless period in milliseconds after the waiting period

●	Posture Change:
	angle_thres_deg (int) : minimum angle change in degrees required for the body posture of the indiviudal between
							pre and post fall 

sampling_freq : the sampling frequency (Hz) of the accelerometer used for measurement

---> If fall detection is cancelled at any point after the impact section, search for a fall continues from the 


"""
def fall_detection(xyz_series, impact_thresh = 2.3, motionless_thresh = 0.3,
							   angle_thres_deg = 20, post_impact_ms = 1000,
							   motionless_ms = 1000, sampling_freq = 200 ):
    
    #getting vector magntidue series
    magnitude_series = utilities.get_mag_series(xyz_series)
    
    #preparing parameters

    angle_threshold = angle_thres_deg * math.pi / 180 

    #time interavals (in ms)
    post_impact_time = post_impact_ms * sampling_freq /1000
    motionless_time = motionless_ms * sampling_freq /1000

    #list of edetected fall events
    fall_event = []

    old_xyz = []

    #	impact (bool) : flag for impact initiation 
    #	wait (bool) : flag for post-impact waiting period
    #	motionless (bool) : flag for motionless period
    impact = wait = motionless = False


    #	t_1 (int) : time of impact initiation 
    #	t_2 (int) : time of impact end
    t_1= t_2 = 0

    # timer (int) : used to count time for each stage of fall 
    timer = 0

    # storing initial normalied 3-axial acceleration 
    # to calculate posture change after fall
    reference_xyz = xyz_series[0] / magnitude_series[0]

    t = 0
    while t < len(magnitude_series) :

        #searching for an impact
        if not wait and not motionless :
            
            #impact begins
            if not impact and magnitude_series[t] > impact_thresh :
                #print("impact found at "+str(t))
                t_1 = t
                impact= True
                #wait = True
                
            #impact is over
            elif impact and t > t_1  and magnitude_series[t] < impact_thresh :
                #print("impact is over at "+str(t))
                t_2 = t
                timer = 0
                wait = True
                impact = False
                
        #wait until the signal stabilizes
        elif wait:
            if timer < post_impact_time:
                timer += 1
            else:
                #print("waited 1 sec")
                wait = False
                timer = 0
                motionless = True

        #in the motioness period
        elif motionless:
            if timer < motionless_time:
                if magnitude_series[t] > 1 + motionless_thresh or magnitude_series[t] < 1- motionless_thresh :
                    motionless = False
                    timer = 0
                    #return to end of impact to keep searching
                    #print("motionless stage distrupted at "+str(t))
                    t = t_2
                else:
                    timer += 1
            else:
                #print("motionless stage finished")
                # to find the motionless state body orientation,
                # we take the average of the last 50 data points

                final_xyz =  xyz_series[t-100:t].mean(axis=0) 
                final_xyz = final_xyz / np.linalg.norm(final_xyz)

                #retrieving the change in angle since beginning of fall
                angle = abs(np.arccos( np.dot(reference_xyz, final_xyz) ))

                #if the body angle (posture) changed sufficiently
                if angle > angle_threshold:

                    # Fall detected succesfully
                    # each fall event includes: start of impact, end of impact, end of waiting time, end of motionless time
                    fall_event.append( [t_1,t_2,t_2+post_impact_time,t_2+post_impact_time+motionless_time] )

                motionless = False
                timer = 0
        t += 1
                
    # the algorithm reaches here if the time series ends before the mtionless time period ends
    if motionless : 
    	# each fall event includes: start of impact, end of impact, end of waiting time, end of motionless time
        fall_event.append( [t_1,t_2,t_2+post_impact_time+motionless_time] )
                
    return fall_event



"""
Processes all acceerlation data in the SisFall Dataset and provides performance results

Brief info about the SisFall Dataset:
-3-axial acceleration data provided in ".txt" format
-Total Files: 4,510 files
-Total Fall Event Recordings: ( 15 fall types ) x ( 5 trials ) x (23 "SA" labelled subjects + "SE06" subject =24) = 1800
-Total ADL (Activites of Daily Living) Recordings: 2710

"""

def process_dataset(folder_path="SisFall_dataset", impact_thresh= 2.3, motionless_thresh = 0.3, 
					angle_thresh= 20, print_results =True):

	correct_detections = 0
	misses = 0
	faulty_detections = 0
	# ADL : Activites of Daily Living
	undetected_ADL = 0
	total_ADL = 0
	total_Fall = 0

	folder_path =  "SisFall_dataset"


	#listing folders for each subject
	for subjectFolder in os.listdir(folder_path):  

				#all valid subject folder names in the dataset folder system start with "S"
	            if subjectFolder[0] != "S":
	                continue

	            subject_path = os.path.join( folder_path, subjectFolder )

	            #listing data files for each trial in the current subject folder
	            for dataFile in os.listdir( subject_path ):

	            	# "F" -> Fall 
	            	# "D" -> Daily Activities 
	                if ( dataFile[0] != "F" and dataFile[0] != "D"):
	                    continue
	                elif dataFile[0] == "F":
	                    total_Fall +=1
	                else:
	                    total_ADL +=1

	                data_path = os.path.join(subject_path, dataFile)

	                # the numerical parameters are selected accroding to the instructions of the SisFall Dataset
					data_series = utilities.prepare_data(data_path, sampling_frequency=200, resolution=13, g_range=32, plot_data=False):

	                # using the default model parameters ars they are already selected as optimal
	                result = fall_detection(data_series,impact_thresh= impact_thresh, motionless_thresh = motionless_thresh, angle_thresh= angle_thresh )

	                # determining the status of the result
	                if dataFile[0] == "D":
	                    if len(result)>0 :
	                    	# FALSE POSITIVE
	                        faulty_detections += 1
	                    else:
	                    	# TRUE NEGATIVE 
	                        undetected_ADL += 1
	                else:
	                    if len(result)>0 :
	                    	# TRUE POSITIVE
	                        correct_detections += 1
	                    else:
	                    	#FALSE NEGATIVE
	                        misses += 1
	                    
	     
	sensitivity = correct_detections/(correct_detections+misses)
	specificity = undetected_ADL/total_ADL
	accuracy = correct_detections + undetected_ADL / (total_ADL + total_Fall)   
	        
	if print_results:
	    
		print("Activities of Daily Living: "+ str(total_ADL))
		print("Expected Detections: " + str(total_Fall ))
		print("Correct Detections: " + str(correct_detections))
		print("Misses: " + str(misses))
		print("Faulty Detections: " + str(faulty_detections))
		print("Correctly Undetected ADL: " + str(undetected_ADL))

		print("Sensitivity: "+ str(sensitivity))
		print("Specificity: "+ str(specificity))
		print("Accuracy: ")+ str(accuracy))

  	results ={ "TP": correct_detections, "TN": undetected_ADL,
  			   "FP": faulty_detections, "FN" : misses,
  			   "sensitivity": sensitivity, "specificity": specificity
  			   "accuracy": accuracy }
  	
  	return results



if __name__ == '__main__':
    
    process_dataset(folder_path="SisFall_dataset")
