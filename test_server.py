#This is to test the server without having to call app. It just runs test cases. 

from beta_personalization import *
import time
from trans_db import *

#Is this per user or overall?
#This should be overall. 

class ServerConnector:

    # 
    def __init__(self,db):
        self.name = "ServerConnector"
        self.user_swipes = {}
        self.user_vector = {}
        self.item_vectors = []
        self.allItems = []
        self.nextItems = {}
        self.myDb = db

        self.loadValues()

    # This will pull all items and store them in the item_vectors and allItems

    #For now, just do the csv. 

    def loadValues(self):
        
        reader = csv.DictReader(open("smallDBTest.csv"))
        allItemCategories = []
        allItems = []
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
        #print("AllItems: " , allItems)
        priceMean = sum([float(x['Price'].replace('$','')) for x in allItems])/len(allItems)
        priceUp =max([abs(float(x['Price'].replace('$',''))-priceMean) for x in allItems])
        #print(priceUp)
        zipMean = sum([float(x['Zipcode'].replace('$','')) for x in allItems])/len(allItems)
        zipUp =max([abs(float(x['Zipcode'].replace('$',''))-zipMean) for x in allItems])
        for i in xrange(0,len(allItems)):
            allItems[i]['Price'] = (float(allItems[i]['Price'].replace('$','')) - priceMean)/priceUp
            allItems[i]['Zipcode'] = (float(allItems[i]['Zipcode']) - zipMean)/zipUp
            myRow = allItems[i]
        allItemCategories = cleanList(allItemCategories)
        evalMethod = ['Zipcode','Price']
        allVecs = []
        for myRow in allItems:
            myRowVec = convertRawToVec(allItemCategories,myRow,evalMethod)
            print(myRowVec)
            allVecs.append(myRowVec)
        self.item_vectors = np.array(allVecs)

        #This should return a list of the phone numbers from the DB. 
        users = self.myDb.getAllUsers()

        for user in users:
            #This should then take in the username, go find the swipes, and store it in this vector. We will assume the metric of user_swipes[i] = float(n) will hold. 

            self.user_swipes[user] = self.myDb.getUserSwipes(user,len(allItems))
            #So this should be an array of all the possible swipes.


            self.user_vector[user] = computeUserVectorWithAverage(self.user_swipes[user],self.item_vectors)
            #Now to find similarities, I just find the dot product between that and all the items
            allItemsRanked = rankItems(self.user_vector[user],self.item_vectors)

            self.nextItems[user] = genNext(allItemsRanked,self.allItems,self.user_swipes[user],exploration_rate=0.4)
        print("All next items: " , self.nextItems)

    # This logs into the server with the username specified.
    # This will also generate the first suggestion
    # This should decay all current preferences by 50%? Or won't that just be silly?

    def login(self,phone_name):
        print("Loging in: " , phone_name)
        ##Make sure the user is in the system, and preload first suggestion.
        allUsers = self.myDb.getAllUsers()
        print("All Users: " , allUsers)
        user = None
        if phone_name in allUsers:
            #It's already in it, preload but it should be ready
            user = phone_name
        else:
            #Create the entry into the DB
            self.myDb.createUser(phone_name)
            #Then set the next one. 
            user = phone_name
        self.user_swipes[user] = self.myDb.getUserSwipes(user,len(self.item_vectors))
        self.user_vector[user] = computeUserVectorWithAverage(self.user_swipes[user],self.item_vectors)
        allItemsRanked = rankItems(self.user_vector[user],self.item_vectors)
        self.nextItems[user] = genNext(allItemsRanked,self.allItems,self.user_swipes[user],exploration_rate=0.4)


        #This should load it into the 
        return None
        pass

    # This will just return the associated next_item
    def getCardId(self,phone_name):
        print("Getting a card for: " , phone_name)
        return self.nextItems[phone_name]
        pass
    # This will update the userswipes then get a new card for them. 

    def swipeCard(self,card,swipeChoice,phone_name):
        print("Swiping: " , card , " for: " , swipeChoice , " on: " , phone_name)

        self.user_swipes[phone_name][card] = float(swipeChoice)
        self.user_vector[phone_name] = computeUserVectorWithAverage(self.user_swipes[phone_name],self.item_vectors)
        #Now to find similarities, I just find the dot product between that and all the items
        allItemsRanked = rankItems(self.user_vector[phone_name],self.item_vectors)
        #Now we have everything ranked. I want to put it into a dictionary of name: rank. 
        #We will then take the highest that is not
        self.nextItems[phone_name] = genNext(allItemsRanked,self.allItems,self.user_swipes[phone_name],exploration_rate=0.4)

        self.myDb.updateSwipes(card,float(swipeChoice),phone_name)
        return None

print("Done Loading...")


def login(phoneName):
    return servercon.login(phoneName)

def getCard(phoneName):
    return servercon.getCardId(phoneName)

def swipeCard(card,swipeChoice,phoneName):
    return servercon.swipeCard(card,swipeChoice,phoneName)

def testLoginAndSwipeSome():
    phoneName = "iggya"
    
    login(phoneName)
    card1 = getCard(phoneName)
    card2 = getCard(phoneName)
    time.sleep(2)
    swipeCard(card2,1,phoneName)
    card3 = getCard(phoneName)
    print("recommend: " , card3)

    #Now get the card.
if __name__ == "__main__":
    myDb = TransDBConnector()
    myDb.connect()
    servercon = ServerConnector(myDb)

    print("Testing....")
    testLoginAndSwipeSome()