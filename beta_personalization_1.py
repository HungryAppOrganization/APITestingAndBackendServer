import csv
import pandas as pd
import numpy as np
import random
from time import strftime, localtime

# This removes capitalization and spaces in names of the tags in the list. It is intended to normalize and remove impurities.
def cleanList(myList):
    myList = [x.lower().replace(" ","") for x in myList if x!="" and isinstance(x,str)]
    return list(set(myList))

#This will be input the raw dictionary from above, and will use the allCats to construct a vector if it contains each or not.
#Extra Cats are continuous variable inputs. 
def convertRowToVec(allCats,row,extraCats):
    newVec = np.zeros(len(allCats)+len(extraCats))
    myValsCleaned = cleanList(row.values())
    for i in xrange(0,len(allCats)):
        if allCats[i] in myValsCleaned:
            newVec[i] = 1
    for i in xrange(0,len(extraCats)):
        newVec[i+len(allCats)] = row[extraCats[i]]
        pass
    return newVec

#This just constructs a user vector to hold both the categorical and continuous inputs. 
def getUserVector(allCats,extraCats):
    newVec = np.zeros(len(allCats)+len(extraCats))
    return newVec

#This Computes the user Vector and averages out across all their swipes (to ensure that preferences stay between [0,1])
def computeUserVectorWithAverage(userSwipes,itemVectors):
##    print(userSwipes)
##    print(itemVectors)
    numSwipes = sum([x!=0 for x in userSwipes])
    res = np.matmul(userSwipes,itemVectors)/numSwipes
##    print("Averaging User Results:",res)
    return res

#This takes in the user vector of preferences and item vectors and returns the scores for how different items rank.
def rankItems(user_vec,item_vectors):
##    print(item_vectors[0])
##    print(np.matmul(user_vec,item_vectors[0]))
    res = np.matmul(user_vec,item_vectors.T)
    print("Rank Results:",res)
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
##    print("New Ranks: ", new_ranks)
    new_ranks = sorted(new_ranks,key = lambda x: x[1])
##    print("Ranked ranks: ", new_ranks)
    ranNum = random.uniform(0, 1)
##    print("RandNum", ranNum, " Exploration:", exploration_rate)
    if (ranNum >= exploration_rate):
        return new_ranks[-1][0]
    else:
        return new_ranks[random.randint(0,len(new_ranks)-1)][0]

if __name__ == "__main__":
    #First go through the csv and make our set of vectors.
    allItems = []
    # Read it in
    reader = csv.DictReader(open("DB_Test - Sheet1.csv"))
    myRow = None
    allItemCategories = []
    #Now add all the items to the same category - we don't discriminate if it is written in Item1 or Item2. 
    for row in reader:
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
    priceMin = min([float(x['Price'].replace('$','')) for x in allItems])
    priceMax = max([float(x['Price'].replace('$','')) for x in allItems])
    priceRange = priceMax - priceMin
    zipMin = min([float(x['Zipcode']) for x in allItems])
    zipMax = max([float(x['Zipcode']) for x in allItems])    
    zipRange = zipMax - zipMin
    for i in xrange(0,len(allItems)):
        allItems[i]['Price'] = (float(allItems[i]['Price'].replace('$','')) - priceMin)/priceRange
        allItems[i]['Zipcode'] = (float(allItems[i]['Zipcode']) - zipMin)/zipRange
        myRow = allItems[i]
    
    #Clean them up. 
    allItemCategories = cleanList(allItemCategories)
    evalMethod = ['Zipcode','Price']
    allVecs = []
    allDescriptions = []
    for myRow in allItems:
        myRowVec = convertRowToVec(allItemCategories,myRow,evalMethod)
        #print(myRowVec)
        allDescriptions.append(myRow['Description'])
        allVecs.append(myRowVec)
    
    #Now this is a 2D numpy array of all the vectors for each item.
    evalMethod.append('Description')
    item_vectors = np.array(allVecs)
    df = pd.DataFrame(item_vectors)
    df.insert(loc = len(item_vectors[0]), column = 'Description', value = allDescriptions)
    df.to_csv('All_Vectors.csv', index = False, header = allItemCategories+evalMethod)
    
    #Load User
    #print(item_vectors)
    user_vector = np.array(getUserVector(allItemCategories,evalMethod))
    #print(user_vector)
    
    #Now we can iterate. and do that shit.
    time_of_all_swipes = []
    user_swipes = np.zeros(len(allItems))
    i = np.random.randint(1,len(allItems)-1)
    while True:
        if (sum([x for x in user_swipes if abs(x)>0])==(len(allItems)-1)):
            print("You swiped everything!")
            break
        else:
            ## print("User Swipes: " , user_swipes)
            ## print("User Vector: " , user_vector)
            ## print("Item Vector: " , item_vectors[i-1])
            ## print("Considering: " , allItems[i])
            ## print("\n")
            print("Considering: ", allItems[i]['Description'])

            print "Choose -1, 1, 2 for Dislike, Like or Buying an item ", i, "or press q to quit"
            n = raw_input()
            #Extracted day in numeric form(0-6 from Sunday to Saturday), hours and minutes 
            time_at_swipe = strftime("%w,%H,%M", localtime()).split(',')
            print(time_at_swipe)
            if n == '-1' or n == '1' or n == '2':
                user_swipes[i] = int(n)
                time_at_swipe = [int(i) for i in time_at_swipe]
                time_of_all_swipes.append(time_at_swipe)
                user_vec = computeUserVectorWithAverage(user_swipes,item_vectors)
                #Now to find similarities, I just find the dot product between that and all the items
                allItemsRanked = rankItems(user_vec,item_vectors)
                #Now we have everything ranked. I want to put it into a dictionary of name: rank. 
                #We will then take the highest
                nextId = genNext(allItemsRanked,allItems,user_swipes,exploration_rate=0.4)
                print("Recommend next id: ", nextId)
                pass
                i = nextId
            elif n == 'q':
                break
            print(time_at_swipe)
            continue

        break
