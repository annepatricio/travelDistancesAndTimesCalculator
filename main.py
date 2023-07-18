import pandas as pd
import requests
import numpy as np
import xlsxwriter
from collections import OrderedDict
import math

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


#CODE

file = pd.read_excel(coordinatesFile)
data = pd.DataFrame(file)
data2 = data.to_numpy()
d3 = np.array(data2)
lines = len(d3)
numberOfGroups = math.ceil((lines-1)/maxNumberOfCoordinatesPerGroup)

def notSucessfull():
    for ori in range(maxNumberOfCoordinatesPerGroup):
        for dest in range(maxNumberOfCoordinatesPerGroup):
            distances.append("erro")
            durations.append("erro")

row = 0
coordinates = []
coordinate_string = ''

for i in range(numberOfGroups):
    group = []
    for i in range(maxNumberOfCoordinatesPerGroup):
        group.append([d3[row, 0], d3[row, 1], d3[row, 2]])
        row = row + 1
    coordinates.append(group)

c = ';'
inicio = 'http://router.project-osrm.org/table/v1/driving/'
sources = '?sources='
destinations = '&destinations='
fim = '&annotations=duration,distance'
codes = []
distances = []
durations = []

for o in range(numberOfGroups):
    grupoOrigem = coordinates[o]
    originCodes = []
    originCoordinates = ""
    sourceIndex =""
    i = 0
    for origin in grupoOrigem:
        originID = origin[0]
        originLat = origin[1]
        originLon = origin[2]
        originCoo = ','.join(map(str, [originLon, originLat]))
        originCodes.append(originID)
        originCoordinates = ';'.join(map(str, [originCoordinates, originCoo]))
        sourceIndex = ';'.join(map(str, [sourceIndex, i]))
        i = i+1
    originCoordinates = originCoordinates[1:]
    sourceIndex = sourceIndex[1:]

    for d in range(numberOfGroups):
        destinationCodes = []
        i = maxNumberOfCoordinatesPerGroup
        destinationCoordinates = ""
        destinationIndex = ""
        grupoDestino = coordinates[d]

        for destination in grupoDestino:
            destID = destination[0]
            destLat = destination[1]
            destLon = destination[2]
            destCoo = ','.join(map(str, [destLon, destLat]))
            destinationCodes.append(destID)
            destinationCoordinates = ';'.join(map(str, [destinationCoordinates, destCoo]))
            destinationIndex = ';'.join(map(str, [destinationIndex, i]))
            i = i + 1
        destinationIndex = destinationIndex[1:]
        link = inicio + originCoordinates+destinationCoordinates+sources+sourceIndex+destinations+destinationIndex+fim
        for c in originCodes:
            for d in destinationCodes:
                code = "origin" + str(c) + "destination" + str(d)
                codes.append(code)

        #get distances and durations
        try:
            response = requests.get(link, timeout=600)
            response.raise_for_status()  # Check if the request was successful
            json_data = response.json()
            if response.status_code == 200 and json_data['code'] == 'Ok':
                for ori in range(maxNumberOfCoordinatesPerGroup):
                    for dest in range(maxNumberOfCoordinatesPerGroup):
                        distances.append(json_data['distances'][ori][dest])
                        durations.append(json_data['durations'][ori][dest])
                        print(json_data['distances'][ori][dest],json_data['durations'][ori][dest])
            else:
                notSucessfull()
        except requests.exceptions.ConnectionError as err:
            notSucessfull()
        except requests.exceptions.HTTPError as err:
            notSucessfull()
        except requests.exceptions.RequestException as err:
            notSucessfull()
        except (KeyError, IndexError) as err:
            notSucessfull()

workbook = xlsxwriter.Workbook(outputFile)
worksheet = workbook.add_worksheet()
row = 0
column = 0
worksheet.write(row, column, "code:")
worksheet.write(row, column + 1, "distance")
worksheet.write(row, column + 2, "duration")
row += 1
i = 0
for item in range(len(codes)):
    worksheet.write(row, column, codes[item])
    worksheet.write(row, column + 1, distances[item])
    worksheet.write(row, column + 2, durations[item])
    row += 1
workbook.close()
