import csv
import pandas as pd
import numpy as np
import random

def csv_reader(file_obj):
    #Read a csv file
    reader = csv.reader(file_obj)
    for row in reader:
        print(" ".join(row))

#First go through the csv and make our set of vectors.

allItems = []

reader = csv.DictReader(open("smallDBTest.csv"))

myRow = None
allItemCategories = []
for row in reader:
    #print(row)
    allItems.append(row)
    myRow = row

    #Add all the items to the allItemCategories
    allItemCategories.append(row['Item1'])
    allItemCategories.append(row['Item2'])
    allItemCategories.append(row['Item3'])
    allItemCategories.append(row['Item4'])
    allItemCategories.append(row['Item5'])
    allItemCategories.append(row['Item6'])
    allItemCategories.append(row['Genre'])
    allItemCategories.append(row['Class'])
    allItemCategories.append(row['Type_of_meal'])

#Now go through and fix the price/zipCode (normalize it)
print("AllItems: " , allItems)
priceMean = sum([float(x['Price'].replace('$','')) for x in allItems])/len(allItems)
priceUp =max([abs(float(x['Price'].replace('$',''))-priceMean) for x in allItems])
print(priceUp)
zipMean = sum([float(x['Zipcode'].replace('$','')) for x in allItems])/len(allItems)
zipUp =max([abs(float(x['Zipcode'].replace('$',''))-zipMean) for x in allItems])

for i in xrange(0,len(allItems)):
    allItems[i]['Price'] = (float(allItems[i]['Price'].replace('$','')) - priceMean)/priceUp
    allItems[i]['Zipcode'] = (float(allItems[i]['Zipcode']) - zipMean)/zipUp
    myRow = allItems[i]


def cleanList(myList):
    myList = [x.lower().replace(" ","") for x in myList if x!="" and isinstance(x,str)]
    return list(set(myList))


print(myRow)
#Perfect example.
#print(allItemCategories)
#print(cleanList(allItemCategories))

allItemCategories = cleanList(allItemCategories)
evalMethod = ['Zipcode','Price']
#Now normalize the zip/price.
#This will be input the raw dictionary from above, and will use the allCats to construct a vector if it contains each or not.
#Extra Cats are continuous variable inputs. 
def convertRawToVec(allCats,row,extraCats):
    newVec = np.zeros(len(allCats)+len(extraCats))
    myValsCleaned = cleanList(row.values())
    #print(myValsCleaned)
    for i in xrange(0,len(allCats)):
        if allCats[i] in myValsCleaned:
            newVec[i] = 1.0#allCats[i]
    for i in xrange(0,len(extraCats)):
        #Note that for these we need to normalize
        newVec[i+len(allCats)] = row[extraCats[i]]
        pass

    #print(newVec)
    return newVec

def getUserVector(allCats,extraCats):
    newVec = np.zeros(len(allCats)+len(extraCats))
    return newVec


allVecs = []
for myRow in allItems:
    myRowVec = convertRawToVec(allItemCategories,myRow,evalMethod)
    print(myRowVec)
    allVecs.append(myRowVec)

#Now this is a 2D numpy array of all the vectors for each item.
#Now the user vector
item_vectors = np.array(allVecs)
print(item_vectors)
user_vector = np.array(getUserVector(allItemCategories,evalMethod))
print(user_vector)

#Now we can iterate. and do that shit.

user_swipes = np.zeros(len(allItems))

def computeUserVectorWithAverage(userSwipes,itemVectors):
    print(userSwipes)
    print(itemVectors)
    numSwipes = sum([abs(x) for x in userSwipes])
    res = np.matmul(userSwipes,itemVectors)/numSwipes
    print("Results:",res)
    return res

def rankItems(user_vector,item_vectors):
    print(item_vectors[0])
    print(np.matmul(user_vector,item_vectors[0]))
    res = np.matmul(user_vector,item_vectors.T)
    print("RankResults:",res)
    return res

#How this method will work is the following:
#   First turn the all_ranks into a list of tuples. Id _ score
#   Next remove all the user_swipes from this list (based on the ids)
#   Then pull a random number. If the random number is greater than the exploration rate, take the highest rating similar item. If it is less, give it a random one.

def genNext(all_ranks,allItems,user_swipes,exploration_rate=0.1):
    new_ranks = []
    for i in xrange(0, len(all_ranks)):
        if user_swipes[i] == 0:
            new_ranks.append((i,all_ranks[i]))
    print("New Ranks: " , new_ranks)
    new_ranks = sorted(new_ranks,key = lambda x: x[1])
    print("Ranked ranks: " , new_ranks)
    ranNum = random.uniform(0, 1)
    print("RandNum", ranNum, " Exploration:", exploration_rate)
    if (ranNum >= exploration_rate):
        return new_ranks[-1][0]
    else:
        return new_ranks[random.randint(0,len(new_ranks)-1)][0]

i = random.randint(1,len(allItems)-1)
while True:
    if (sum([x for x in user_swipes if abs(x)>0])==(len(allItems)-1)):
        print("You swiped everything!")
        break
    else:
        print("User Swipes: " , user_swipes)
        print("User Vector: " , user_vector)
        print("Item Vector: " , item_vectors[i-1])
        print("Considering: " , allItems[i])
        print("\n")
        print("Considering: " , allItems[i]['Description'])

        print "Choose -1, 2, 1 for Dislike, Love or Like respectively for item", i, "or press q to quit"
        #n = "1"
        n = raw_input()
        #n = "1"
        if n == '-1' or n == '2' or n == '1' or n == '':
            if n == '2':
                n = '1'
            user_swipes[i] = float(n)
            user_vec = computeUserVectorWithAverage(user_swipes,item_vectors)
            #Now to find similarities, I just find the dot product between that and all the items
            allItemsRanked = rankItems(user_vec,item_vectors)
            #Now we have everything ranked. I want to put it into a dictionary of name: rank. 
            #We will then take the highest that is not
            nextId = genNext(allItemsRanked,allItems,user_swipes,exploration_rate=0.4)
            print("Recommend next id: " , nextId)
            pass
            i = nextId

        elif n == 'q':
            break
        continue

    break

    #break



















