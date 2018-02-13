#This method contains everything of what we need to order things.
#We will get the food name and restaurant.

import requests
import json

KEY = "308c457ee6398852"
myHead = {'X-Access-Token':KEY,'Content-Type':'application/json'}

#This method passes in the foodname of what you want to order.
#Also the restaurant of where you want to get it from
#And finally the restaurant from where you want to get it.
#Note that the address should be the complete address.
#Note this is open to both delivery methods.
def getIDOfRest(restName,restAddress):
	delMethod = "both"
	addr = restAddress
	searchParam = restName

	htmlLink = "https://api.eatstreet.com/publicapi/v1/restaurant/search?method="+str(delMethod)+"&street-address="+str(addr)+"&search="+str(searchParam)

	response = requests.get(htmlLink, headers={'X-Access-Token': '308c457ee6398852'})

	val = json.loads(response.content)

	retVal = json.dumps(val,sort_keys=True,indent=4)
	try:
		return val["restaurants"][0]["apiKey"]
	except:
		print retVal
		return None

#This is a list of the categories that the restaurant offers.
def getRestMenu(restId):
	htmlLink = "https://api.eatstreet.com/publicapi/v1/restaurant/"+str(restId)+"/menu?includeCustomizations=false"

	response = requests.get(htmlLink, headers={'X-Access-Token': '308c457ee6398852'})
	val = json.loads(response.content)

	print json.dumps(val,sort_keys=True,indent=4)
	print(val)
	return val


def getFoodID(foodName, menu):
	#Okay so I should space through each one. 
	#Categories
	retVal = None
	for ele in menu:
		#This is each dict there. GO through the items
		for indItem in ele["items"]:
			if (indItem["name"] == foodName):
				return indItem["apiKey"]
			#Print each name.
	return retVal

#This gets you the price of the food with the associated ID's
def getFoodPrice(restId,foodId):
	pass
	#Get the Menu
	menu = getRestMenu(restId)
	#Parse through to find the price
	for ele in menu:
		for indItem in ele["items"]:
			if (indItem["apiKey"] == foodId):
				return indItem["basePrice"]
	return None

#This orders the food from the restaurant and specifies the given instructions.
def orderFood(restId,foodIds,orderAddressID,cardID,userID,tip,instructions):
	#
	htmlLink = "https://api.eatstreet.com/publicapi/v1/send-order"
	items = []
	for food in foodIds:
		newVal = {"apiKey":food}
		items.append(newVal)
	method = "delivery"
	payment = "card"
	tip = tip
	address = {"apiKey":orderAddressID}
	card = {"apiKey":cardID}
	recipient = {"apiKey":userID}
	jsonValuie = {"restaurantApiKey":restId,"items":items,"method":method,"payment":payment,"tip":tip,"address":address,"recipient":recipient,"card":card,"comments":instructions}
	
	response = requests.post(htmlLink,headers=myHead,json=jsonValue)
	val = json.loads(response.content)

	print json.dumps(val,sort_keys=True,indent=4)

#This registers a user
#Note this must be done with each customer. 
#Returns user ID
def registerUser(email,firstName,lastName,password,phone):
	print("Registering....")
	htmlLink = "https://api.eatstreet.com/publicapi/v1/register-user"
	jsonValue = {'email':email,'password':password,'firstName':firstName,'lastName':lastName,'phone':phone}

	response = requests.post(htmlLink,headers=myHead,json=jsonValue)
	return response.content["apiKey"]

#This method signs in the user.
def signInUser(email,password):
	print("Signing in...")
	htmlLink = "https://api.eatstreet.com/publicapi/v1/signin"
	jsonValue = {"email":email,"password":password}
	response = requests.post(htmlLink,headers=myHead,json=jsonValue)
	print(response.content)

#This adds an address for a delivery.
#Returns the ID for the address
def addAddress(userID,streetAddress,city,state,zipC,extra):
	htmlLink = "https://api.eatstreet.com/publicapi/v1/user/"+str(userKey) + "/add-address"
	aptNumber = extra
	apiKey = userID
	streetAddress = streetAddress + "," + city + " " + state + ", " + str(zipC)
	jsonValue = {"apiKey":userKey,"aptNumber":aptNumber,"streetAddress":streetAddress,"city":city,"state":state,"zip":zipC}
	response = requests.post(htmlLink,headers=myHead,json=jsonValue)
	print (response.content)
	return response.content["apiKey"]

#Note the address should be the complete address.
#Cardnumber should not have any formatting.
#Cardholder name should be the complete name with everything.
def addCardUser(userID,cardholderName,cardholderStreetAddress,cardZip,cvv,cardNumber,expirationMonth,expirationYear):
	htmlLink = "https://api.eatstreet.com/publicapi/v1/user/"+str(userID) +"/add-card"
	print("Adding card...")
	#cardholderName = "John E Peurifoy"
	jsonValue = {"apiKey":userID,"cardholderName":cardholderName,"cardholderStreetAddress":cardholderStreetAddress,"cardholderZip":cardholderZip,"cvv":cvv,"cardNumber":cardNumber,"expirationMonth":expirationMonth,"expirationYear":expirationYear}

	response = requests.post(htmlLink,headers=myHead,json=jsonValue)

	print(response.content)

def printMenu(restMenu):
	for ty in restMenu:
		for ele in ty['items']:
			print ele['name']



#China One Express	11176 Antioch Rd, Overland park KS, 66210


#restName = "Oklahoma Joe's BBQ & Catering"
restName = "China One Express"
restAddr = "11176 Antioch Rd, Overland park KS, 66210"
#restAddr = "3002 West 47th Avenue, Kansas City KS, 66103"
foodName = 'The Z-Man Sandwich'
restId = getIDOfRest(restName,restAddr)
#print("Rest ID: " , restId)
#Do this by similarity. Find the most similar item. 
restMenu = getRestMenu(restId)
printMenu(restMenu)

foodId = getFoodID(foodName,restMenu)
print("Food ID: " , foodId)
































































