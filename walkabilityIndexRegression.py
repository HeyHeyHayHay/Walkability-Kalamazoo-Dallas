
import csv
import numpy
import matplotlib.pyplot as matplot


Walkability_Index = 'C:\\Users\\hayde\\OneDrive\\Desktop\\Coding\\Walkability_Index\\EPA_SmartLocationDatabase_V3_Jan_2021_Final.csv'



fields = []
rows = []

CSA_Names = []

NatWalkIndIndex = 114
Shape_AreaIndex = 116
CSA_NameIndex = 8
PopIndex = 18
CountyFPIndex = 4
StateFPIndex = 3
dallasID = '48113'
kalamazooID = '2677'

with open(Walkability_Index, 'r') as csvfile:
    csvreader = csv.reader(csvfile)

    fields = next(csvreader)

    for row in csvreader:
        rows.append(row)
        CSA_Names.append(row[8])


    # print("Total number of rows: %d"%(csvreader.line_num))

# Print all the column names
# print('Field names are:' + ', '.join(field for field in fields))

# Print all the names of locations
#print(CSA_Names)

# find the percentage of these which are given State

def reverse(list):
   new_list = list[::-1]
   return new_list

def outputListWithStringInString(string, columnIndex):
    listWithString = []
    string = str(string)

    for row in rows:
            if string in row[columnIndex]:
                listWithString.append(row[columnIndex])

    return listWithString

def findFieldIndex(fieldName):
    for index in range(len(fields)):
        if fieldName in fields[index]:
            return(index)

def concatenatefields(objectID, field1Index, field2Index):

    part1 = rows[int(objectID)-1][int(field1Index)]
    part2 = rows[int(objectID)-1][int(field2Index)]

    return (part1 + part2)

def objectIDsOfStringInString(string, columnIndex):
    objectIDsWithString = []
    string = str(string)

    for row in rows:
            if string in row[columnIndex]:
                objectIDsWithString.append(row[0])

    return objectIDsWithString

def objectIDsOf(string, columnIndex):
    objectIDsWithString = []
    string = str(string)

    for row in rows:
            if string == str(row[int(columnIndex)]):
                objectIDsWithString.append(row[0])

    return objectIDsWithString

def objectIDsOfConcatenate(string, columnIndex1, columnIndex2):
    objectIDsWithString = []
    string = str(string)

    for row in rows:
        if string == str(row[int(columnIndex1)])+str(row[int(columnIndex2)]):
            objectIDsWithString.append(row[0])

    return objectIDsWithString

def fieldListFromObjectIDs(listOfObjectIDs, fieldIndex):
    list = []
    for objectID in listOfObjectIDs:
        list.append(rows[int(objectID)-1][fieldIndex])

    return list

def percentageOfList(smallerList, totalList):
    return len(smallerList)/len(totalList)

def objectIDsNonZeroWalkability(objectIDs):
    for id in objectIDs:
        if rows[int(id)-1][114] == 0:
            objectIDs.remove(id-1)
            print("found zero")
    return objectIDs

def averageWalkability(objectIDs):
    objectIDs = objectIDsNonZeroWalkability(objectIDs)
    numberOfBlockGroups = len(objectIDs)
    sum = 0
    for id in objectIDs:
        sum = sum + float(rows[int(id)-1][114])

    return (sum/numberOfBlockGroups)

def averageWalkabilityPerArea(objectIDs):
    objectIDs = objectIDsNonZeroWalkability(objectIDs)
    numberOfBlockGroups = len(objectIDs)
    totalArea = 0
    totalWTimesArea = 0

    for id in objectIDs:
        totalArea = totalArea + float(rows[int(id)-1][116])
        totalWTimesArea = totalWTimesArea + float(rows[int(id)-1][116])*float(rows[int(id)-1][114])

    avgWperArea = totalWTimesArea/totalArea
    return (avgWperArea)

def averageWalkabilityPerCapita(objectIDs):
    objectIDs = objectIDsNonZeroWalkability(objectIDs)
    numberOfBlockGroups = len(objectIDs)
    totalPop = 0
    totalWTimesPop = 0

    for id in objectIDs:
        totalPop = totalPop + float(rows[int(id)-1][18])
        totalWTimesPop = totalWTimesPop + float(rows[int(id)-1][18])*float(rows[int(id)-1][114])

    if totalPop == 0:
        return (0)

    avgWperPop = totalWTimesPop/totalPop
    return (avgWperPop)

def sumPopulation(objectIDs):
    objectIDs = objectIDsNonZeroWalkability(objectIDs)

    population = float(0)

    for id in objectIDs:
        population = population + float(rows[int(id)-1][PopIndex])

    return population


def percentile(value, field):
    totalRows = len(rows)
    numberBelow = 0
    for row in rows:
        if float(row[int(field)]) <= value:
            numberBelow = numberBelow + 1

    return (numberBelow/totalRows)

def percentileAdjustedForField(value, comparedField, adjustingField):

    #this does not work

    total = 0
    numberBelow = 0

    for row in rows:

        total = total + float(row[int(adjustingField)])

        if float(row[int(comparedField)]) <= value:

            numberBelow = numberBelow + float(row[int(adjustingField)])


    return (numberBelow/total)

def findAllValuesForCSA_Name(tag):
    tag = str(tag)

    IDs = objectIDsOfStringInString(tag, CSA_NameIndex)

    thisAverageWalkability = averageWalkability(IDs)
    thisAverageWalkabilityPerArea = averageWalkabilityPerArea(IDs)
    thisAverageWalkabilityPerCapita = averageWalkabilityPerCapita(IDs)

    thisPerWalk = percentile(thisAverageWalkability, NatWalkIndIndex)
    thisPerWalkArea = percentileAdjustedForField(thisAverageWalkabilityPerArea, NatWalkIndIndex, Shape_AreaIndex)
    thisPerWalkPop = percentileAdjustedForField(thisAverageWalkabilityPerCapita, NatWalkIndIndex, PopIndex)

    findings = [tag, thisAverageWalkability, thisPerWalk, thisAverageWalkabilityPerArea, thisPerWalkArea, thisAverageWalkabilityPerCapita, thisPerWalkPop]

    return(findings)

def findAllValuesForIDs(ids):
    IDs = ids

    thisAverageWalkability = averageWalkability(IDs)
    thisAverageWalkabilityPerArea = averageWalkabilityPerArea(IDs)
    thisAverageWalkabilityPerCapita = averageWalkabilityPerCapita(IDs)

    thisPerWalk = percentile(thisAverageWalkability, NatWalkIndIndex)
    thisPerWalkArea = percentileAdjustedForField(thisAverageWalkabilityPerArea, NatWalkIndIndex, Shape_AreaIndex)
    thisPerWalkPop = percentileAdjustedForField(thisAverageWalkabilityPerCapita, NatWalkIndIndex, PopIndex)

    findings = [thisAverageWalkability, thisPerWalk, thisAverageWalkabilityPerArea, thisPerWalkArea, thisAverageWalkabilityPerCapita, thisPerWalkPop]

    return(findings)

def allCountyDict():
    countyDict = {}

    for row in rows:
        countyGeoID = concatenatefields(row[0], StateFPIndex, CountyFPIndex)
        objectID = row[0]

        listOfObjectIDs = countyDict.setdefault(countyGeoID, [objectID])
        listOfObjectIDs.append(objectID)

    return countyDict

counties = allCountyDict()

def evaluateDict(dictionary, function):

    evaluatedDict = {}

    for areaKey in dictionary:
        objectIDs = dictionary.get(areaKey)
        eval = function(objectIDs)

        evaluatedDict.setdefault(areaKey, eval)

    return evaluatedDict

def sortDict(dict):
    sortedList = sorted(dict.items(), key=lambda x:x[1], reverse=True)
    return sortedList

def findRankOfCounty(countyGeoID, rankedList):

    for pair in rankedList:
        if countyGeoID == pair[0]:
            rank = 1 + rankedList.index(pair)
            return rank

def evaluateCounty(countyGeoID, function):
    counties = allCountyDict()

    dict = evaluateDict(counties, function)

    value = dict.get(countyGeoID)

    return value

def findValuesRanksForCounty(countyGeoID):
    counties = allCountyDict()

    averageWalkabilityOfCounties = evaluateDict(counties, averageWalkability)
    averageWalkabilityPerAreaOfCounties = evaluateDict(counties, averageWalkabilityPerArea)
    averageWalkabilityPerCapitaOfCounties = evaluateDict(counties, averageWalkabilityPerCapita)

    thisAverageWalkability = averageWalkabilityOfCounties.get(countyGeoID)
    thisAverageWalkabilityPerArea = averageWalkabilityPerAreaOfCounties.get(countyGeoID)
    thisAverageWalkabilityPerCapita = averageWalkabilityPerCapitaOfCounties.get(countyGeoID)

    sortWalk = sortDict(averageWalkabilityOfCounties)
    sortWalkArea = sortDict(averageWalkabilityPerAreaOfCounties)
    sortWalkCapita = sortDict(averageWalkabilityPerCapitaOfCounties)

    rankWalk = findRankOfCounty(countyGeoID, sortWalk)
    rankWalkArea = findRankOfCounty(countyGeoID, sortWalkArea)
    rankWalkCapita = findRankOfCounty(countyGeoID, sortWalkCapita)

    return (countyGeoID, thisAverageWalkability, rankWalk, thisAverageWalkabilityPerArea, rankWalkArea, thisAverageWalkabilityPerCapita, rankWalkCapita)

def listTopBottomNRanks(rankedList, n, top):
    top = bool(top)

    listOfCountyIDs = []
    listOfCountyNames = []

    if top == True:
        for i in range(n):
            listOfCountyIDs.append(rankedList[i][0])
    else:
        rankedList = reverse(rankedList)
        for i in range(n):
            listOfCountyIDs.append(rankedList[i][0])

    for countyID in listOfCountyIDs:
        objectIDs = counties.get(countyID)
        objectID = objectIDs[0]
        CSA_Name = rows[int(objectID)][CSA_NameIndex]
        listOfCountyNames.append(CSA_Name)

    return (listOfCountyNames, listOfCountyIDs)

def splitDictWalkability(dictPop, dictWalk, min, max):
    listOfKeysToPop = []
    newDictPop = dictPop.copy()
    newdictWalk = dictWalk.copy()
    for i in dictWalk:
        value = dictWalk.get(i)
        if ((value > max) or (value <= min)):
            listOfKeysToPop.append(i)

    for key in listOfKeysToPop:
        newdictWalk.pop(key)
        newDictPop.pop(key)

    XY = [newDictPop, newdictWalk]
    return XY


countyPopulationsX = evaluateDict(counties, sumPopulation)

averageWalkabilityOfCountiesY = evaluateDict(counties, averageWalkability)

xK = [evaluateCounty(kalamazooID, sumPopulation)]
xD = [evaluateCounty(dallasID, sumPopulation)]
yK = [evaluateCounty(kalamazooID, averageWalkability)]
yD = [evaluateCounty(dallasID, averageWalkability)]

x = list(countyPopulationsX.values())
y = list(averageWalkabilityOfCountiesY.values())

xy0 = splitDictWalkability(countyPopulationsX, averageWalkabilityOfCountiesY, 0, 1)
xy1 = splitDictWalkability(countyPopulationsX, averageWalkabilityOfCountiesY, 1, 7)
xy2 = splitDictWalkability(countyPopulationsX, averageWalkabilityOfCountiesY, 7, 9.333333)
xy3 = splitDictWalkability(countyPopulationsX, averageWalkabilityOfCountiesY, 9.333333, 11.333333)
xy4 = splitDictWalkability(countyPopulationsX, averageWalkabilityOfCountiesY, 11.333333, 13)
xy5 = splitDictWalkability(countyPopulationsX, averageWalkabilityOfCountiesY, 13, 14.833333)
xy6 = splitDictWalkability(countyPopulationsX, averageWalkabilityOfCountiesY, 14.833333, 16.666666)
xy7 = splitDictWalkability(countyPopulationsX, averageWalkabilityOfCountiesY, 16.666666, 20.000000)



mymodel = numpy.poly1d(numpy.polyfit(x, y, 1))

myline = numpy.linspace(-100000, 10000000, 100)

#matplot.scatter(x, y, color = '0.7')
matplot.scatter(list((xy0[0]).values()), list((xy0[1]).values()), color = '#ffffff')
matplot.scatter(list((xy1[0]).values()), list((xy1[1]).values()), color = '#f4fbc5')
matplot.scatter(list((xy2[0]).values()), list((xy2[1]).values()), color = '#d6eeb0')
matplot.scatter(list((xy3[0]).values()), list((xy3[1]).values()), color = '#aadc9c')
matplot.scatter(list((xy4[0]).values()), list((xy4[1]).values()), color = '#7bc588')
matplot.scatter(list((xy5[0]).values()), list((xy5[1]).values()), color = '#56a56e')
matplot.scatter(list((xy6[0]).values()), list((xy6[1]).values()), color = '#368961')
matplot.scatter(list((xy7[0]).values()), list((xy7[1]).values()), color = '#326b53')

matplot.xlabel("Population of County")
matplot.ylabel("Average Walkability of County")
matplot.title("County Population vs Average Walkability")

matplot.plot(myline, mymodel(myline), color = '0.5')

matplot.plot(xK, yK, 'k', marker = 'o', markersize = 8)
matplot.plot(xD, yD, "k", marker = 'o', markersize = 8)

matplot.show()
