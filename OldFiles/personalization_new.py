import csv
import pandas as pd
import numpy as np
import random

#This file will input a csv file, store all the values. Randomly select each one and ask the user what they think of it, then store the user preferences and keep going.

####Support functions

def csv_reader(file_obj):
    #Read a csv file
    retVal = []
    reader = csv.reader(file_obj)
    for row in reader:
        print row
        retVal.append(row)
    return retVal

#These are all the things the user has swiped on. 
taste_profile = {'Type_of_meal':0,'Genre':0,'Class':0,'Item1':0,'Item2':0,'Item3':0,'Item4':0,'Item5':0,'Item6':0}
user_vec = []
db_file = "smallDBTest.csv"

if __name__ == "__main__":

    #First getting all the possible foodItems from the file
    allFoodItems = []
    with open(db_file,'r') as f:
        allFoodItems = csv_reader(f)

    print(allFoodItems)

    count = (len(open(db_file).readlines(  ))) - 1 # To find size of the CSV file

    #Make everything into numbers based. 
    

    totNum = 0 #Number of options thus far. 
    while totNum < count:

        #I is a random number
        i = random.randint(1,count)
        totNum += 1
        while True:

            print "Choose -1, 0, 1 for Dislike, Love or Like respectively for item", allFoodItems[i][1], "or press q to quit"
            n = raw_input()
            if n == '-1' or n == '0' or n == '1' or n == '':
                #user_vec[i]=n
                user_vec.append(i)
                break
            elif n == 'q':
                print("Unrecognized input")
        #Now personalize and shit.
        #Now add this onto it.
        #Old vector + 
        user_vec[i] = user_vec[i] + 











##    print user_vec
    
    # Adding the data user selected to a dictionary
    reader = csv.DictReader(open(db_file))
    result = {}
    c = 0

    for row in reader:
        if c < len(user_vec):
            if user_vec[c] == '1' or user_vec[c] == '0' or user_vec[c] == '-1':
                for column, value in row.iteritems():
                    result.setdefault(column.strip(), []).append(value.strip())
            else:
                user_vec.remove(user_vec[c])
                c = c-1
        elif c >= len(user_vec):
            break
        c = c+1
    print(result)
##    print result
##    print user_vec
    
    df = pd.DataFrame(result)
    stacked = df[['Type_of_meal','Genre','Class','Item1','Item2','Item3','Item4','Item5','Item6']].stack()
    print(stacked)


    df[['Type_of_meal','Genre','Class','Item1','Item2','Item3','Item4','Item5','Item6']] = pd.Series(stacked.factorize()[0], index=stacked.index).unstack()
##    print (df)
    result =df.to_dict('list')
    print("Line 79")
    print(result)

    
    # Change the vector from string to int type
    for i in range(0,len(user_vec)):
        user_vec[i] = int(user_vec[i])
    
    # Add the data to a List
    L=[]
    for key, value in result.iteritems():
        if key == "Zipcode":
            value = [int(i) for i in value]
            L.append(value)
        elif key == "Price":
            value = [i.strip('$') for i in value]
            value = [float(i) for i in value]
            L.append(value)
        elif key == "Offer_Delivery":
            value = [int(i) for i in value]
            L.append(value)
        elif key == "Type_of_meal":
            L.append(value)
        elif key == "Genre":
            L.append(value)
        elif key == "Class":
            L.append(value)
        elif key == "Item1":
            L.append(value)
        elif key == "Item2":
            L.append(value)
        elif key == "Item3":
            L.append(value)
        elif key == "Item4":
            L.append(value)
        elif key == "Item5":
            L.append(value)
        elif key == "Item6":
            L.append(value)
##    print L

    L = np.array(L)
    user_vec = np.array(user_vec)
    res = np.matmul(L,user_vec)
    print "Resultant vector is",res
    res_vec = res/len(user_vec)
    print "Resultant vector divided by total number of items selected is", res_vec

    # Adding all the data to a dictionary
    reader = csv.DictReader(open(db_file))
    result_all = {}
    for row in reader:
        for column, value in row.iteritems():
            result_all.setdefault(column.strip(), []).append(value.strip())
##    print result_all

    df = pd.DataFrame(result_all)
    stacked = df[['Type_of_meal','Genre','Class','Item1','Item2','Item3','Item4','Item5','Item6']].stack()
    df[['Type_of_meal','Genre','Class','Item1','Item2','Item3','Item4','Item5','Item6']] = pd.Series(stacked.factorize()[0], index=stacked.index).unstack()
##    print (df)
    result_all =df.to_dict('list')
    
    # Add all the data to a List and Names of food items to another List
    L_all=[]
    L_name=[]
    for key, value in result_all.iteritems():
        if key == "Zipcode":
            value = [int(i) for i in value]
            L_all.append(value)
        elif key == "Price":
            value = [i.strip('$') for i in value]
            value = [float(i) for i in value]
            L_all.append(value)
        elif key == "Offer_Delivery":
            value = [int(i) for i in value]
            L_all.append(value)
        elif key == "Type_of_meal":
            L_all.append(value)
        elif key == "Genre":
            L_all.append(value)
        elif key == "Class":
            L_all.append(value)
        elif key == "Item1":
            L_all.append(value)
        elif key == "Item2":
            L_all.append(value)
        elif key == "Item3":
            L_all.append(value)
        elif key == "Item4":
            L_all.append(value)
        elif key == "Item5":
            L_all.append(value)
        elif key == "Item6":
            L_all.append(value)
        elif key == "Description":
            L_name.append(value)
##    print L_all

##    L_all = [[float(L_all) for L_all in sublist] for sublist in L_all]
    L_name = L_name[0]
    L_all = np.array(L_all)
##    print L_all

    # Find the Euclidean Distance between the res_vec and all other food items
    Dist=[]
    for i in range(0,len(L_all[1])):
        vector1 = res_vec
        vector2 = L_all[0:12,i]
        diff = vector2 - vector1
        squareDistance = np.dot(diff.T, diff)
        Dist.append(squareDistance)

##    print Dist

    dict1={}
    for i in range(0,len(L_name)):
        dict1[L_name[i]] = Dist[i]

    dict1 = sorted(dict1.items(), key=lambda x: x[1])
    print dict1