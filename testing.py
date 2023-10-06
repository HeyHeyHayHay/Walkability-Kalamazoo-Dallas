list = []
list.append( 'New York-Newark, NY-NJ-CT-PA')
list.append( 'Oklahoma City-Shawnee, OK')
list.append( 'Buffalo-Cheektowaga-Olean, NY')
print(list)

def outputListWithStringInString(string,list):
    listWithString = []

    for item in list:
            if string in item:
                print("is in NY")
                listWithString.append(item)

    return listWithString

print(outputListWithStringInString('NY',list))

list1 = [1,2,4]
list2 = [5,7,9]

listT = [list1, list2]

print(listT[0][1])
