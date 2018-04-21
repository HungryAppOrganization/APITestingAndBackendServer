import pyrebase
import os
from dotenv import load_dotenv
import random
import numpy as np
from datetime import datetime

dotenv_path = ".env"
load_dotenv(dotenv_path, verbose=True)

API_KEY = os.environ.get("FIREBASEAPI")
FIREBASE_DOMAIN = os.environ.get("FIREBASE_DOMAIN")
FIREBASE_DBURL = os.environ.get("FIREBASE_DBURL")
FIREBASE_STORAGE = os.environ.get("FIREBASE_STORAGE")

foodDatabaseName="foods_kc_1_15"

#This program will handle dataentry into the DB, ensuring correct structure and offering an 'API' of sorts to making sure the transactions are completed appropriately.
class TransDBConnector:
    def __init__(self):
        self.debug = False
        self.db = None
        self.verbose = False
        self.firebase = None

    def connect(self):

        config = {
              "apiKey": API_KEY,
              "authDomain": FIREBASE_DOMAIN,
              "databaseURL": FIREBASE_DBURL,
              "storageBucket": FIREBASE_STORAGE
        }
        self.firebase = pyrebase.initialize_app(config)
        self.db = self.firebase.database()
    
    def addAddress(self,add1,city,state,zipa,add2="",add3="",name=""):
        #See if address already exist.
        #val = self.db.child("address").order_by_child("add1").equal_to(add1)
        try:
            val = self.db.child("address").order_by_child("add1").equal_to(str(add1)).get().val().values()

            print ("Val: " ,val)
            #print (val.get())
            #val = val.get().val().values()
            
            if len(val) > 0:
                #print(val[0]['id'])
                print("returning my id: " , val[0]['id'])
                return val[0]['id']
        except:
            pass 
            #Record doesn't exist.
        #First get count
        #This gets the ID
        #idAssos = self.db.child('address').order_by_child("id").limit_to_last(1).get().val().values()[0]['id']+1
        print('adding')
        idAssos = self.getNextId("address")
        data = {'city':city,'add1':add1,'add2':add2,'add3':add3,'state':state,'zip':zipa,'id':idAssos,'name':name}
        print("adding: " , data)
        
        self.db.child('address').push(data)
        return idAssos

    def addCostQuote(self,cost,delId,foodId,time,websiteURL):
        pass
        #idAssos = self.getNextId("address")
        #idAssos = self.getNextId("costQuote")
        idAssos = self.getNextId("costQuote")
        data = {"cost":cost,"delId":delId,"foodId":foodId,"time":time,"websiteURL":websiteURL,"id":idAssos}
        self.db.child("costQuote").push(data)

    def addDelService(self,hostWebsite,name):
        pass
        idAssos = self.getNextId("delService")
        data = {"id":idAssos,"hotWebsite":hostWebsite,"name":name}
        self.db.child("delService").push(data)

    def addFoodItem(self,name,picLink,restidLink,estCost=0,estCal=0):
        pass
        #See if food already exist.
        
        val = self.db.child("fooditem").order_by_child("restidLink").equal_to(int(restidLink)).get()
        for vals in val.each():
            print("Vals: " , vals)
            if vals.val()['name'] == name:
                print("Matches!!!!!")
                return vals.val()['id']
        idAssos = self.getNextId("fooditem")
        data = {"id":idAssos,"name":name,"picLink":picLink,"restidLink":restidLink,"estCost":estCost,"estCal":estCal}
        self.db.child("fooditem").push(data)

    def addRestDelivery(self,restId,deliveryServiceId):
        pass
        idAssos = self.getNextId("rest_delivery_service_lnk")
        data = {"id":idAssos,"restId":restId,"deliveryServiceId":deliveryServiceId}
        self.db.child("rest_delivery_service_lnk").push(data)

    def addRestaurant(self,name,addressId,phone,openTimes=None):
        pass
        #See if restaurant already exist.
        try:
            val = self.db.child("restaurant").order_by_child("addressId").equal_to(addressId).get().val().values()
            if len(val) > 0:
                #print(val[0]['id'])
                return val[0]['id']
        except:
            pass

        idAssos = self.getNextId("restaurant")
        data = {"id":idAssos,"name":name,"addressId":addressId,"phone":phone,"openTImes":openTimes}
        self.db.child("restaurant").push(data)
        return idAssos

    def getNextId(self,cat):
        #print("Category: " , cat)
        print(self.db.child(cat).order_by_child("id").limit_to_last(1).get().val()[0])
        idAssos = self.db.child(cat).order_by_child("id").limit_to_last(1).get().val().values()[0]['id']+1
        print("next id: " , idAssos)
        return idAssos

    def getNextCard(self,idToGet=None):
        if idToGet == None:
            idToGet = random.randint(50,350)
        val = self.db.child(foodDatabaseName).order_by_child("id").equal_to(idToGet).get().val().values()[0]
        return val

    def getAllUsers(self):
        #This returns all the users in a list of the usernames
        vals = self.db.child("users").get().val().values()
        usernames = [str(val['username']) for val in vals]
        print(usernames)
        return usernames

    def getUserSwipes(self,userName,numberItems):
        user_swipes = np.zeros(numberItems)
        #Now get the swipes
        print("username: " , userName)
        val = self.db.child("users").order_by_child("username").equal_to(userName).get().val().values()[0]['swipes'].values()
        for swipe in val:
            listId = int(swipe['cardID'])
            user_swipes[listId] = float(swipe['swipe'])
        #print("Val is: " , val)
        return user_swipes

    def updateSwipes(self,cardSwipe,swipeChoice,phone_name):
        pass

        data = {"cardID":cardSwipe,"swipe":swipeChoice,"time":str(datetime.now())}

        #self.db.child("users").order_by_child("username").equal_to(phone_name).child("swipes").push(data)
        userName = self.db.child("users").order_by_child("username").equal_to(phone_name).get().val().keys()[0]

        self.db.child("users").child(userName).child("swipes").push(data)

        print("Done updating swipes....")

    def createUser(self,phone_name):
        data = {"username":phone_name,"swipes":{"first":{"cardID":1,"swipe":1,"time":str(datetime.now())}}}
        self.db.child("users").push(data)


if __name__ == "__main__":
    print "Testing Database...."

    myDb = TransDBConnector()
    myDb.connect()
    users = myDb.getAllUsers()

    #print(myDb.getUserSwipes(users[0],100))
    myDb.updateSwipes(5,1,"iggy")
    #userName = myDb.db.child("users").order_by_child("username").equal_to("iggy").get().val().keys()[0]

    #myDb.db.child("users").child(userName).child("swipes").push(data)

    #print(myDb.db.child("users").order_by_child("username").equal_to("iggy").get().val().keys()[0])

    #myDb.addAddress("2726 S Campbell Ave","Springfield","MO","65807")


    #Example Queries
    #myDb.db.child("address").order_by_child('id').limit_to_last(10).remove()

    #Example User Remove
    #db.child("users").child("Morty").remove()






