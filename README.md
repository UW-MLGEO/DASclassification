# DASclassification

## Members
Erfan Horeh
Alex Rose
Anajani Mirchandani

## Project Goals
In this project we plan to classify different signals in DAS data.

## Data:
OOI 2021
Whidbey 2024

## Challenges associated with DAS data
The OOI DAS dataset is around 26 TB of data as a whole which makes using it on github challenging. Challenges have also been shown from large download sizes and download times.

## Metadata File
The Metadata file for this project helps give bounds in time and space to ships identified for ML. Ships are displayed like in the example image and we find the bounds in which they plot in time and space. The borders of the features displayed are noted for both the distance and time then marked down in the metadata. A calculation is then undergone in the .csv which calculated where it lies in the channels based on the knowing the given channel length. (channel = ((distance / 2meters) * 1000 m/km)

Example Image:  

![xt of bandpass (6 0-80 0Hz)+fk(1450-9000) filtered data plot 30](https://github.com/user-attachments/assets/05f9d48e-e94e-4960-96a0-0365b305878d)

Columns:
Ship_# - Unique # given to each different ship  
folder_name - name of folder  
Gauge_length - Determines spatial resolution of data  
Interrogator - Instrument used  
depth - depth of cable (m)  
Ship_type - type of ship  
Ship_speed - speef of ship  
Cable - Which OOI cable is being utilized (North or South)  
Lon	- Longitude (degrees)  
Lat	- Latitude (degress)  
~Start_distance - (closest distance along cable from Pacific City, OR [km] where ship is seen)  
~End_distance - (furthest distance along cable from Pacific City, OR [km] where ship is seen)  
~Start_channel - (closest channel along cabe from Pacific City, OR [km] where ship is seen, converted from distance)  
~End_channel - (furthest channel along cabe from Pacific City, OR [km] where ship is seen, converted from distance)  
~Start_Time - (First time ship is seen)  
~End_Time -	(last time ship is seen)  
Notes - Notes  



