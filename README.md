# Travel distances and times calculator

## Description

This project is a simple calculator that allows you to calculate the distance and duration of a trip between a set of geographic coordinates using the OSMR API.

#INPUTS

| Input  | Detail |
| ------------- | ------------- |
| coordinatesFile  |  Coordinate File in .xlsx with at least 3 columns with the following information:(code,longitude,latitude)|
| maxNumberOfCoordinatesPerGroup | The maxNumberOfCoordinatesPerGroup must be defined so that all groups have the same number of coordinates. For example, if you have 180 coordinates, the maxNumberOfCoordinatesPerGroup 36 (resulting in 5 groups of 36) or 45 (resulting in 4 groups of 36). I have successfully applied a maxNumberOfCoordinatesPerGroup up to 53 and retrieved a file with distances and durations between more than 1000 coordinates.|
| outputFile  |  File in .xlsx |
