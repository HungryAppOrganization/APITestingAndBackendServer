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

        dataFile="Rest_DB_2 - Complete_DB_5_5_server.csv"
        
        reader = csv.DictReader(open(dataFile,'rU'))
        allItemCategories = []
        allItems = []
        for row in reader:
            #print(row)
            allItems.append(row)
            myRow = row
            #print(row)

            #Add all the items to the allItemCategories
            allItemCategories.append(row['Item1'])
            allItemCategories.append(row['Item2'])
            allItemCategories.append(row['Item3'])
            allItemCategories.append(row['Item4'])
            allItemCategories.append(row['Item5'])
            allItemCategories.append(row['Item6'])
            allItemCategories.append(row['Item7'])
            allItemCategories.append(row['Item8'])
            allItemCategories.append(row['Item9'])
            allItemCategories.append(row['Item10'])
            allItemCategories.append(row['Item11'])
            allItemCategories.append(row['Item13'])
            allItemCategories.append(row['Item14'])
            allItemCategories.append(row['Item15'])
            allItemCategories.append(row['Item16'])
            allItemCategories.append(row['Item17'])
            allItemCategories.append(row['Item18'])
            allItemCategories.append(row['Item19'])
            allItemCategories.append(row['Item20'])
            allItemCategories.append(row['Item21'])
            allItemCategories.append(row['Item22'])
            allItemCategories.append(row['Item23'])
            allItemCategories.append(row['Genre'])
            allItemCategories.append(row['Class1'])
            allItemCategories.append(row['Class2'])
            allItemCategories.append(row['Type_of_meal'])
            allItemCategories.append(row['Dietary'])
        #Now go through and fix the price/zipCode (normalize it)
        #print("AllItems: " , allItems)
        for i in xrange(0,len(allItems)):
            if str(allItems[i]['Price']) == "":
		allItems[i]["Price"] = "$0.00" 
        priceMean = sum([float(x['Price'].replace('$','')) for x in allItems])/len(allItems)
        priceUp =max(max([abs(float(x['Price'].replace('$',''))-priceMean) for x in allItems]),.001)
        #print(priceUp)
        for i in xrange(0,len(allItems)):
            allItems[i]['Price'] = (float(allItems[i]['Price'].replace('$','')) - priceMean)/priceUp
            myRow = allItems[i]
        allItemCategories = cleanList(allItemCategories)

        self.allItemCategories = allItemCategories
        evalMethod = ['Price']
        allVecs = []
        for myRow in allItems:
            myRowVec = convertRawToVec(allItemCategories,myRow,evalMethod)
            #print(myRowVec)
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
        #print("All next items: " , self.nextItems)

    # This logs into the server with the username specified.
    # This will also generate the first suggestion
    # This should decay all current preferences by 50%? Or won't that just be silly?

    def login(self,phone_name,fId="",fToken="",eId="",pId=""):
        print("Loging in: " , phone_name)
        ##Make sure the user is in the system, and preload first suggestion.
        allUsers = self.myDb.getAllUsers()
        #print("All Users: " , allUsers)
        user = None
        if phone_name in allUsers:
            #It's already in it, preload but it should be ready
            user = phone_name
        else:
            #Create the entry into the DB
            self.myDb.createUser(phone_name,fId=fId,fToken=fToken,eId=eId,pId=pId)
            #Then set the next one. 
            user = phone_name
        self.user_swipes[user] = self.myDb.getUserSwipes(user,len(self.item_vectors))
        self.user_vector[user] = computeUserVectorWithAverage(self.user_swipes[user],self.item_vectors)
        allItemsRanked = rankItems(self.user_vector[user],self.item_vectors)
        self.nextItems[user] = genNext(allItemsRanked,self.allItems,self.user_swipes[user],exploration_rate=0.4)
        #This should load it into the 
        return None
        pass

    #This prints a user's taste profile
    def printTasteProfile(self,phone_name):
        allUsers = self.myDb.getAllUsers()
        #print("All Users: " , allUsers)
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
        print()
        print(self.user_vector[user])
        print(self.allItemCategories)
        return self.user_vector[user] , self.allItemCategories





    # This will just return the associated next_item
    def getCardId(self,phone_name):
        print("Getting a card for: " , phone_name)
        print("Card id is: " , self.nextItems[phone_name])
        #Give it a 5% chance for randomness.
        ranNum = random.uniform(0, 1)
        print("my random number: " , ranNum)
        if (ranNum < 0.1):
              return int(random.uniform(0,100))
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
        #This is so the next card is not seen.
        self.user_swipes[phone_name][self.nextItems[phone_name]] = float(.001)
        print("Next card is now: " , self.nextItems[phone_name])
        self.myDb.updateSwipes(card,float(swipeChoice),phone_name)
        return None

    #This method sends the swipe, and stores the new card. 
    def swipe_and_getID(self,card,swipeChoice,phone_name):
        print("Swiping: " , card , " for: " , swipeChoice , " on: " , phone_name)

        self.user_swipes[phone_name][card] = float(swipeChoice)
        self.user_vector[phone_name] = computeUserVectorWithAverage(self.user_swipes[phone_name],self.item_vectors)
        #Now to find similarities, I just find the dot product between that and all the items
        allItemsRanked = rankItems(self.user_vector[phone_name],self.item_vectors)
        #Now we have everything ranked. I want to put it into a dictionary of name: rank. 
        #We will then take the highest that is not
        self.nextItems[phone_name] = genNext(allItemsRanked,self.allItems,self.user_swipes[phone_name],exploration_rate=0.4)
        #This is so the next card is not seen.
        self.user_swipes[phone_name][self.nextItems[phone_name]] = float(.001)
        print("Next card is now: " , self.nextItems[phone_name])
        self.myDb.updateSwipes(card,float(swipeChoice),phone_name)

        #Now the nextItem
        ranNum = random.uniform(0, 1)
        print("my random number: " , ranNum)
        retVal = 0 
        if (ranNum < 0.1):
            retVal = int(random.uniform(0,100))
        else:
            retVal = self.nextItems[phone_name]
        print("Returning: " , retVal)
        return retVal

    #This prints a user's taste profile
    def printTasteProfile(self,phone_name):
        allUsers = self.myDb.getAllUsers()
        #print("All Users: " , allUsers)
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
        print()
        print(self.user_vector[user])
        print(self.allItemCategories)
        return self.user_vector[user] , self.allItemCategories



print("Done Loading...")

def analyzeUser(phoneName="Rachel s iPhone"):
    vec,cats  = servercon.printTasteProfile(phoneName)
    print('\n')
    print("Vector: " , vec)
    print("Cats  : ", cats)
    saveUserPrefToFile(vec,cats,phoneName)
    return
    vals = vec.argsort()[-20:][::-1]
    for val in vals:
        print cats[val]

    #Now least fav. 
    print('\n')
    vals = vec.argsort()[:10][::-1]
    for val in vals:
        try:
            print cats[val]
        except:
            pass

def analyzeAllUsers(myDb):
    users = myDb.getAllUsers()
    for user in users:
        analyzeUser(str(user)

)
def saveUserPrefToFile(vec,cats,userName="test"):
    print("Vecotr: " , vec)
    print("Cats:   " , cats)
    filename = "userdata/"+ userName + "_vec.csv"
    np.savetxt(filename,vec,delimiter=",")
    myfile = open("userdata/" + userName + "_cat.csv",'w')
    for cat in cats:
        myfile.write("\n " + str(cat))
    myfile.flush()
    myfile.close()

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
def analyzeUser():
    phoneName = "Rachel s iPhone"
    vec,cats  = servercon.printTasteProfile(phoneName)

    print('\n')
    vals = vec.argsort()[-20:][::-1]
    for val in vals:
        print cats[val]

    #Now least fav. 
    print('\n')
    vals = vec.argsort()[:10][::-1]
    for val in vals:
        try:
            print cats[val]
        except:
            pass

if __name__ == "__main__":
    myDb = TransDBConnector()
    myDb.connect()
    servercon = ServerConnector(myDb)

    print("Testing....")
    #analyzeAllUsers(myDb)
    #analyzeUser()
    #testLoginAndSwipeSome()
    testLoginAndSwipeSome()

    #user_swipes = servercon.myDb.getUserSwipes(user,len(self.item_vectors))
    #    self.user_vector[user] = computeUserVectorWithAverage(self.user_swipes[user],self.item_vectors)
