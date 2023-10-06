
import csv

Walkability_Index = 'C:\\Users\\hayde\\OneDrive\\Desktop\\Coding\\Walkability_Index\\EPA_SmartLocationDatabase_V3_Jan_2021_Final.csv'



fields = []
rows = []

CSA_Names = []

NatWalkIndIndex = 114
Shape_AreaIndex = 116
CSA_NameIndex = 8
PopIndex = 18
CountyFPIndex = 4

with open(Walkability_Index, 'r') as csvfile:
    csvreader = csv.reader(csvfile)

    fields = next(csvreader)

    for row in csvreader:
        rows.append(row)
        CSA_Names.append(row[8])


    print("Total number of rows: %d"%(csvreader.line_num))

# Print all the column names
# print('Field names are:' + ', '.join(field for field in fields))

# Print all the names of locations
#print(CSA_Names)

# find the percentage of these which are given State

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

    avgWperPop = totalWTimesPop/totalPop
    return (avgWperPop)

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

countyFPs = fieldListFromObjectIDs(range(len(rows)), 4)



kalamazooCountyIDs = objectIDsOf('77', CountyFPIndex)
dallasCountyIDs = objectIDsOf('113', CountyFPIndex)

print(fieldListFromObjectIDs(kalamazooCountyIDs, 3))
print(fieldListFromObjectIDs(dallasCountyIDs, 3))

print('usa', findAllValuesForIDs(range(len(rows))))
#print('Kalamazoo', findAllValuesForIDs(kalamazooCountyIDs))
#print('Dallas', findAllValuesForIDs(dallasCountyIDs))
#print(findAllValuesForCSA_Name('MI'))
#print(findAllValuesForCSA_Name('TX'))
#print(findAllValuesForCSA_Name('Kalamazoo'))
#print(findAllValuesForCSA_Name('Dallas'))
