# routeCalculator
....
#INPUTS

coordinatesFile = "ADD_HERE_THE_FILE_WITH_THE_CENTROIDS.xlsx"
#The coordinatesFile must have at least 3 columns with the following information:(code,longitude,latitude)
maxNumberOfCoordinatesPerGroup = n
"""
The maxNumberOfCoordinatesPerGroup must be defined so that all groups have the same number of coordinates. 
For example, if you have 180 coordinates, the maxNumberOfCoordinatesPerGroup 36 (resulting in 5 groups of 36) 
or 45 (resulting in 4 groups of 36). 
I have successfully applied a maxNumberOfCoordinatesPerGroup up to 53 and retrieved a file with distances and durations between more than 1000 coordinates. 
"""
outputFile = "ADD_HERE_THE_OUTPUT_FILE.xlsx"
