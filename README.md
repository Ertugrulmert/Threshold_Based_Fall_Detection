# Threshold Based Fall Detection Algorithm

This repository contains the implementation of a threshold based fall detection alogirhtm and its parameter search code. 

### Files:
- threshold_based_model.py : contains the implementation of the algorithm and a main function to run it on the default dataset
- parameter_search.py : contains the parameter search code for the algorithm
- utilities.py : contains helper functions

## What are threshold based fall detection models?


The data type used for fall detection within the scope of this project is the acceleration along x, y and z axes obtained with a 3-axis accelerometer. Models explored within the scope of this project worked with the magnitude of the acceleration vector and its direction change over a specified time.
	Threshold-based fall detection models are based on representing the stages of a fall with certain threshold values. A fall is conditioned on the acceleration vector magnitude exceeding the threshold values ​​in the correct order and within specified time intervals as well as acceleration changing direction over time. The conditions are selected to optimally differentiate a fall from activities of daily living such as running, jumping, sitting, standing up etc.
	
Studies published on this detector type show that the stages of falling largely remain the same or similar accross different studies, but the methods used to represent these stages, the numbers used for threshold values ​​and the combinations of threshold values ​​differ [[1]](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0037062). 

## Stages of the final algorithm used in this project:

 1. **Impact Stage**
 
	 This phase represents the moment when the person hits a surface during the falling process. Impact manifests itself as a sudden rise and fall in the magnitude of the acceleration vector. In different studies, there are models that use only one threshold value for magnitude rise or two separate threshold values for rise and fall. Whether to use separate threshold values for the beginning and end of the impact is a parameter that needs to be determined. I used one imapct threshold to initiate and end the impact stage. 
	 
 2. **Post-Impact Stage**
 
	Immediately after the impact, a waiting period is included so that the signal has time to stabilize before the later processing stages.  In this way, when there is an extended or multiple-impact fall, the ongoing acceleration fluctuations will settle down before the next stage, which will monitor whether the individual remains motionless.  The waiting time is a model parameter.
	
3.  **Motionless Stage**

The individual is expected to stay relativelly still on the surface they fell onto for a short while before recovering. Motionless is modeled as the acceleration vector magnitude not deviating from 1 g more than a set threshold value for a minimum time period. 

4. **Change in body orientation after fall**

This stage is based on the assumption that a fall would change the orientation of the individual's body. The orientation of the body shortly before the first stage of fall detection is compared to the post-fall orientation and the angle difference between the initial and final acceleration vectors is used as a threshold. Angle difference threshold value is a model parameter.

## Dataset Used

For the parameter selection and performance evaluation of the model, [SisFall Dataset](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5298771/)  was used. The dataset consists of a mixture of synthetic fall and ADL (Activities of Daily Living) recordings. 

## Model Performance
The performance of the model on the entire dataset was found to be as follows:

-Sensitivity: % 92.7
-Specificity: % 95.5
-Accuracy: % 94.4

Threshold values were determined by carrying out grid search using values in the neighborhood of values used in research papers published on this subject [[1]](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0037062).
It must be noted that the entire dataset was used for both the grid search and performance evalation. Thus, information leak is likely present and the performance values may be higher than realistic estimates. In any case, they are comparable to the results given in the review article I took as reference [[1]](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0037062). Using a separate validation set would be the ideal approach.
