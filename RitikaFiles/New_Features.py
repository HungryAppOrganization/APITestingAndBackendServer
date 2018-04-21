import csv
import pandas as pd
import numpy as np
##from scipy.spatial.distance import cosine
        
if __name__ == "__main__":
    user_vec = [] # Vector for user's choices 
    csv_path = "DB_Test - Sheet1.csv" # Read the CSV file
    df1 = pd.read_csv(csv_path)
    df_view = df1[['Number', 'Description']]
    print df_view

    # User enters his choices 
    for i in range(1, (len(df1.index)+1)):
        print "Choose -1, 0, 1 for Dislike, Love or Like respectively for item", i, "or press q to quit"
        n = raw_input()
        if n == '-1' or n == '0' or n == '1':
            user_vec.append(n)
        elif n == 'q':
            break
##    print user_vec
    
    # Adding all the data to a dictionary
    reader = csv.DictReader(open(csv_path))
    result_all = {}
    for row in reader:
        for column, value in row.iteritems():
            result_all.setdefault(column.strip(), []).append(value.strip())
##    print result_all

    result_all['Zipcode'] = [int(i) for i in result_all['Zipcode']]
    result_all['Price'] = [float(i.strip('$')) for i in result_all['Price']]
    result_all['Offer_Delivery'] = [int(i) for i in result_all['Offer_Delivery']]

    df1 = pd.DataFrame(result_all)
    df1_new = pd.unique(df1[['Type_of_meal','Genre','Class','Item1', 'Item2', 'Item3', 'Item4', 'Item5', 'Item6']].values.ravel('K'))
    l1 = df1_new.tolist()
    for i in l1:
        df1[i] = pd.Series(data = 0, index=df1.index, dtype = 'int')
    for index in range(0,len(df1.index)):
        pd.set_option('mode.chained_assignment', None)
        col_name1 = df1['Type_of_meal'][index]
        df1[col_name1][index] = 1
        col_name2 = df1['Genre'][index]
        df1[col_name2][index] = 1
        col_name3 = df1['Class'][index]
        df1[col_name3][index] = 1
        col_name4 = df1['Item1'][index]
        df1[col_name4][index] = 1
        col_name5 = df1['Item2'][index]
        df1[col_name5][index] = 1
        col_name6 = df1['Item3'][index]
        df1[col_name6][index] = 1
        col_name7 = df1['Item4'][index]
        df1[col_name7][index] = 1
        col_name8 = df1['Item5'][index]
        df1[col_name8][index] = 1
        col_name9 = df1['Item6'][index]
        df1[col_name9][index] = 1

    cols_to_norm = ['Zipcode','Price']
    df1[cols_to_norm] = df1[cols_to_norm].apply(lambda x: (x - x.min()) / (x.max() - x.min()))
    result_all =df1.to_dict('list')
    print("results:")
    print(result_all)

    # Add all the data to a List and Names of food items to another List
    L_all=[]
    L_name=[]
    for key, value in result_all.iteritems():
        if key == "Zipcode":
            L_all.append(value)
        elif key == "Price":
            L_all.append(value)
        elif key == "Offer_Delivery":
            L_all.append(value)
        elif key in l1:
            L_all.append(value)
        elif key == "Description":
            L_name.append(value)
##    print L_all

    L_name = L_name[0]
    L_all = np.array(L_all)
##    print L_all
    
    df1.to_csv("DB_Test - Output.csv", sep =',')
    
    # Adding the data user selected to a dictionary
    reader = csv.DictReader(open("DB_Test - Output.csv"))
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
    print result
   
    # Change the vector from string to int type
    for i in range(0,len(user_vec)):
        user_vec[i] = int(user_vec[i])
    
    # Add the data to a List
    L=[]
    for key, value in result.iteritems():
        if key == "Zipcode":
            L.append(value)
        elif key == "Price":
            L.append(value)
        elif key == "Offer_Delivery":
            L.append(value)
        elif key in l1:
            L.append(value)
##    print L

    L = np.array(L, dtype = 'float')
    user_vec = np.array(user_vec)
    res = np.matmul(L,user_vec)
##    print "Resultant vector is",res
    res_vec = res/len(user_vec)
##    print "Resultant vector divided by total number of items selected is", res_vec
    
    # Find the Euclidean Distance between the res_vec and all other food items
    dist=[]
    for i in range(0,len(L_all[1])):
        vector1 = res_vec
        vector2 = L_all[0:75,i]
        diff = vector2 - vector1
        squareDistance = np.dot(diff.T, diff)
        dist.append(squareDistance)

    rec={}
    for i in range(0,len(L_name)):
        rec[L_name[i]] = dist[i]

    rec = sorted(rec.items(), key=lambda x: x[1])
    print rec
