# DASclassification

## Members and Contact Info (email, GitHub username)
Erfan Horeh <br>
Alex Rose - arose17@uw.edu, arose1234 <br>
Anjani Mirchandani 

## Project Goals
In this project we plan to classify different signals in DAS data using machine learning.

How we will complete this project:
1. Make DAS data AI-ready for use with different ML methods
2. Propose methods for ship noise DAS data to be used my ML

### How our notebooks are organized:  
Due to the large nature of DAS data it was very difficult to separate the notebooks into different files for the steps undergone since we are dealing with extremely big data. We have 1 notebook which includes our steps in order to be able to analyze the data since we are unable to save our data directly to GitHub.

## Installation:

### Needed Imports
If you have all packages installed then tbe .ipynb file should run das_package has functions inside made for this project

```
import os
import numpy as np
from tqdm import tqdm
import glob
from skimage.measure import block_reduce
import matplotlib.pyplot as plt
import scipy.signal as sp
```

## Data:
Ocean Observatories Initiative RAPID community test from 2021

The OOI 2021 data comes specifically as .h5 files which contain numerous numbered variables such as time and distance along cable and Whidbey 2024 data has not been recieved yet.  
Strain rate data is calculated later on in the notebook.

### Citation:
Wilcock, W., & Ocean Observatories Initiative. (2023). Rapid: A Community Test of Distributed Acoustic Sensing on the Ocean Observatories <br> 
Initiative Regional Cabled Array [Data set]. Ocean Observatories Initiative. https://doi.org/10.58046/5J60-FJ89

Example Image:  

![xt of bandpass (6 0-80 0Hz)+fk(1450-9000) filtered data plot 30](https://github.com/user-attachments/assets/05f9d48e-e94e-4960-96a0-0365b305878d)

### Exploratory Data Analysis(EDA) notes:
For the DAS data the mean, max, min, and variance are not helpful for the overall data. However, using different variables from the data: the spectrum, our plotted spectrogram, and the signal to noise ratio are much more beneficial as they help up observe more of the key trends occuring in the data due to the high dimensionality presented in the DAS data.

## Metadata File:
The Metadata file for this project helps give bounds in time and space to ships identified for ML. Ships are displayed like in the example image and we find the bounds in which they plot in time and space. The borders of the features displayed are noted for both the distance and time then marked down in the metadata. A calculation is then undergone in the .csv which calculated where it lies in the channels based on the knowing the given channel length. (channel = ((distance / 2meters) * 1000 m/km)

### How the metadata file is organized:
Each column has a specific attribute it is displaying. The rows in the metadata correspond to each instance of identifiable ships crossing over either a section of the North or South OOI cable monitored in our data. The columns below explain what each attribute is and how it contributes to our study.

Columns:
Ship_# - Unique # given to each different ship, allows for knowing if the same ship is in more than 1 row   
folder_name - name of folder on onedrive, due to large data constraints some folders are on onedrive for viewing which shows plot similar to example above   
Gauge_length - Determines spatial resolution of data  
Interrogator - Instrument used, either optasense or silixa  
depth - depth of cable (m), how far underwater the cable is lying on the seafloor  
Ship_type - type of ship  
Ship_speed - speef of ship  
Cable - Which OOI cable is being utilized (North or South), the OOI RCA has multiple cables and these are two sitting along the oregon margin  
Lon	- Longitude (degrees)  
Lat	- Latitude (degress)  
~Start_distance - (closest distance along cable from Pacific City, OR [km] where ship is seen), Left side of the plot  
~End_distance - (furthest distance along cable from Pacific City, OR [km] where ship is seen) , Right side of the plot 
~Start_channel - (closest channel along cabe from Pacific City, OR [km] where ship is seen, converted from distance), attribute used for key variables in the data  
~End_channel - (furthest channel along cabe from Pacific City, OR [km] where ship is seen, converted from distance), attribute used for key variables in the data   
~Start_Date_Time_Plot - time indicated in top right of plot for start time whihc is = 0.
~Start_Time_from_plot - (First time ship is seen from start of plot), Bottom side of the plot  
~End_Time_from_plot -	(last time ship is seen from start of plot), Top side of the plot  
~Start_datetime_ship - actual start time in MM/D/YYYY HH:MM:SS
~end_datetime_ship - actual end time in MM/D/YYYY HH:MM:SS
Notes - Notes  

## Challenges associated with DAS data
The OOI DAS dataset is around 26 TB of data as a whole which makes using it on github challenging. Challenges have also been shown from large download sizes and download times. The dimensionality of the dataset is also very large so specific code blocks take lots of time to run.

## Contributions:
Erfan Horeh - Project Lead  

Alex Rose - Project Assistant  
- Assisted with compilation and formatting of metadata of where ships are located in the data to be utilized by ML and compiled sections of README.md file.
- Compiled Research Relevance file and utilized AutoML to find suitable models.

Anjani Mirchandani- Project Assistant

