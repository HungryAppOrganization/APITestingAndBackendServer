import csv
import pandas as pd
import numpy as np

def csv_reader(file_obj):
    #Read a csv file
    reader = csv.reader(file_obj)
    for row in reader:
        print(" ".join(row))

if __name__ == "__main__":
    user_vec = [] # Vector for user's choices 
    csv_path = "smallDBTest.csv" # Read the CSV file
    with open(csv_path, "rb") as f_obj:
        csv_reader(f_obj)

    count = (len(open("smallDBTest.csv").readlines(  ))) - 1 # To find size of the CSV file
    f_obj.close()

    # User enters his choices 
    for i in range(1, count+1):
        print "Choose -1, 0, 1 for Dislike, Love or Like respectively for item", i, "or press q to quit"
        #n = "1"
        #n = raw_input()
        n = "1"
        if n == '-1' or n == '0' or n == '1' or n == '':
            user_vec.append(n)
        elif n == 'q':
            break
##    print user_vec
    
    # Adding the data user selected to a dictionary
    reader = csv.DictReader(open("smallDBTest.csv"))
    result = {}
    c = 0
    for row in reader:
        if c < len(user_vec):
            if user_vec[c] == '1' or user_vec[c] == '0' or user_vec[c] == '-1':
                print("Row:",row)
                for column, value in row.iteritems():
                    result.setdefault(column.strip(), []).append(value.strip())
                    print(result[column.strip()])
            else:
                user_vec.remove(user_vec[c])
                c = c-1
        elif c >= len(user_vec):
            break
        c = c+1
##    print result
    print("User vect:")
    print user_vec
    print("Result:")
    print(result)

    
    df = pd.DataFrame(result)
    print("DF: " , df)
    stacked = df[['Type_of_meal','Genre','Class','Item1','Item2','Item3','Item4','Item5','Item6']].stack()
    print(stacked)
    df[['Type_of_meal','Genre','Class','Item1','Item2','Item3','Item4','Item5','Item6']] = pd.Series(stacked.factorize()[0], index=stacked.index).unstack()

##    print (df)
    result =df.to_dict('list')
    print("New reuslt: " , result)
    #For those categories listed above, it now is converted into just a single unique integer for each one. 
    #This picks a category for each individual description. 

    
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
    print("L:",L)

    user_vec = np.array(user_vec)
    res = np.matmul(L,user_vec)
    print "Resultant vector is",res
    #This is then all the numbers selected and put into the user vector
    res_vec = res/len(user_vec)
    print "Resultant vector divided by total number of items selected is", res_vec

    # Adding all the data to a dictionary
    reader = csv.DictReader(open("smallDBTest.csv"))
    result_all = {}
    for row in reader:
        for column, value in row.iteritems():
            result_all.setdefault(column.strip(), []).append(value.strip())
    print "New Result: " , result_all #Dictionary with all the options in it. 

    df = pd.DataFrame(result_all)
    stacked = df[['Type_of_meal','Genre','Class','Item1','Item2','Item3','Item4','Item5','Item6']].stack()
    df[['Type_of_meal','Genre','Class','Item1','Item2','Item3','Item4','Item5','Item6']] = pd.Series(stacked.factorize()[0], index=stacked.index).unstack()
##    print (df)
    result_all =df.to_dict('list')

    print("result all: " ,result_all)
    
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
    print("L_Name: " , L_name)
    L_all = np.array(L_all)
    print("L_All:",L_all) #Now all the other options. Note each row is the set of possibilities. 
##    print L_all
    print("User vector: " , res_vec)
    print("L values:    " , L_all)

    # Find the Euclidean Distance between the res_vec and all other food items
    Dist=[]
    for i in range(0,len(L_all[1])):
        vector1 = res_vec
        vector2 = L_all[0:12,i]
        diff = vector2 - vector1
        squareDistance = np.dot(diff.T, diff)
        Dist.append(squareDistance)

##    print Dist
    print("Distances: " , Dist)

    dict1={}
    for i in range(0,len(L_name)):
        dict1[L_name[i]] = Dist[i]

    dict1 = sorted(dict1.items(), key=lambda x: x[1])
    print dict1
