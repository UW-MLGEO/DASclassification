# DASclassification

## Members
Erfan Horeh
Alex Rose
Anajani Mirchandani

## Project Goals
In this project we plan to classify different signals in DAS data using machine learning.

How we will complete this project:
1. Make DAS data AI-ready for use with different ML methods
2. Propose methods for ship noise DAS data to be used my ML


## Data:
OOI 2021
Whidbey 2024

## Challenges associated with DAS data
The OOI DAS dataset is around 26 TB of data as a whole which makes using it on github challenging. Challenges have also been shown from large download sizes and download times.

## Metadata File:
The Metadata file for this project helps give bounds in time and space to ships identified for ML. Ships are displayed like in the example image and we find the bounds in which they plot in time and space. The borders of the features displayed are noted for both the distance and time then marked down in the metadata. A calculation is then undergone in the .csv which calculated where it lies in the channels based on the knowing the given channel length. (channel = ((distance / 2meters) * 1000 m/km)

Example Image:  

![xt of bandpass (6 0-80 0Hz)+fk(1450-9000) filtered data plot 30](https://github.com/user-attachments/assets/05f9d48e-e94e-4960-96a0-0365b305878d)

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
~Start_Time - (First time ship is seen), Bottom side of the plot  
~End_Time -	(last time ship is seen), Top side of the plot  
Notes - Notes  

## Contributions:
Erfan Horeh - Project Lead  

Alex Rose - Project Assistant  
- Assisted with compilation and formatting of metadata of where ships are located in the data to be utilized by ML and compiled sections of README.md file

Anajani Mirchandani- Project Assistant
 
