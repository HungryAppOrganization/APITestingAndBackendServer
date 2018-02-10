# This file supports the testing and all for getting Hungry? Integrating with eat API.
# We are first going to store the key, register a user, then add a card. Note that we will make methods for each of these 
import requests
import json

KEY = "308c457ee6398852"
myHead = {'X-Access-Token':KEY,'Content-Type':'application/json'}

#This registers a user
def registerUser():
	print("Registering....")
	htmlLink = "https://api.eatstreet.com/publicapi/v1/register-user"
	email = "yallhungry-exec@mit.edu"
	password = "ggg2018"
	firstName = "andy"
	lastName = "march"
	phone = "4176934622"
	jsonValue = {'email':email,'password':password,'firstName':firstName,'lastName':lastName,'phone':phone}

	response = requests.post(htmlLink,headers=myHead,json=jsonValue)

	print(response.content)

	return response.content["apiKey"]

#This signs in a user
def signInUser():
	print("Signing in...")
	htmlLink = "https://api.eatstreet.com/publicapi/v1/signin"

	email = "yallhungry-exec@mit.edu"
	password = "ggg2018"
	jsonValue = {"email":email,"password":password}

	response = requests.post(htmlLink,headers=myHead,json=jsonValue)

	print(response.content)

	return response.content

#This adds a card to a user

def addCardUser(userID):
	htmlLink = "https://api.eatstreet.com/publicapi/v1/user/"+str(userID) +"/add-card"
	print("Adding card...")
	cardholderName = "John E Peurifoy"
	cardholderStreetAddress = "300 N Atlantic Ave, Daytona Beach FL 32126"
	cardholderZip = "32126"
	cvv="822"
	cardNumber = "4147788575804634"
	expirationMonth = "08"
	expirationYear = "19"
	jsonValue = {"apiKey":userID,"cardholderName":cardholderName,"cardholderStreetAddress":cardholderStreetAddress,"cardholderZip":cardholderZip,"cvv":cvv,"cardNumber":cardNumber,"expirationMonth":expirationMonth,"expirationYear":expirationYear}

	response = requests.post(htmlLink,headers=myHead,json=jsonValue)

	print(response.content)
	

	#return response.content
	pass

#This finds their corresponding ID of the restaurant they use
def searchAddress(addr="316+W.+Washington+Ave.+Madison,+WI"):
	addr=addr.replace(" ","+")
	print("New addr:", addr)
	delMethod = "delivery"
	htmlLink = "https://api.eatstreet.com/publicapi/v1/restaurant/search?method="+str(delMethod)+"&street-address="+str(addr)

	response = requests.get(htmlLink, headers={'X-Access-Token': '308c457ee6398852'})
	
	#print(response.content)
	#print(type(response.content))
	val = json.loads(response.content)

	print json.dumps(val,sort_keys=True,indent=4)


def getMenu(restApiKey):
	htmlLink = "https://api.eatstreet.com/publicapi/v1/restaurant/"+str(restApiKey)+"/menu?includeCustomizations=false"

	response = requests.get(htmlLink, headers={'X-Access-Token': '308c457ee6398852'})
	val = json.loads(response.content)

	print json.dumps(val,sort_keys=True,indent=4)

	#print(response.content)

def addAddress(userKey):
	htmlLink = "https://api.eatstreet.com/publicapi/v1/user/"+str(userKey) + "/add-address"
	aptNumber = ""
	streetAddress = "351 Massachusetts Ave, Cambridge MA, 02139"
	city = "Cambridge"
	state = "MA"
	zipC = "02139"
	jsonValue = {"apiKey":userKey,"aptNumber":aptNumber,"streetAddress":streetAddress,"city":city,"state":state,"zip":zipC}
	response = requests.post(htmlLink,headers=myHead,json=jsonValue)
	print (response.content)



def orderItem(restApi,itemApi,specificID):
	htmlLink = "https://api.eatstreet.com/publicapi/v1/send-order"
	items = [{"apiKey":itemApi},{"apiKey":"6634369"}]
	#items = [{"apiKey":itemApi,"customizationChoices":[{"apiKey":specificID}]}]
	method = "delivery"
	payment = "card"
	tip = 1.0
	#Address should be the user address. 
	address = {
		"apiKey": "29d91c07f7f49d64595353ec00aedee4994f44c03c4c7057",
		"streetAddress": "351 Massachusetts Avenue",
		"city": "Cambridge",
		"state": "MA",
		"zip": "02139",
		"aptNumber": "0",
		"latitude":"42.3627217",
		"longitude":"-71.0991694"
	}
	card = {"apiKey":"c5aeb8c8e7e5b32a541f21c6bc6a615e1e7d021823aadac1"}
	#Note keep same api key, override name and phone.
	user = {
		"apiKey": "6773262ae51c479a95eca4d326a358f7e41ee9406039e889",
		"firstName": "Joe",
		"lastName": "Blow",
		"phone": "4176934622"
	}
	jsonValue = {"restaurantApiKey":restApi,"items":items,"method":method,"payment":payment,"tip":tip,"address":address,"recipient":user,"card":card,"comments":"Please call 417-693-4622 when you get this order for more instructions."}

	print("Requesting the order....")

	response = requests.post(htmlLink,headers=myHead,json=jsonValue)
	val = json.loads(response.content)

	print json.dumps(val,sort_keys=True,indent=4)

	#print(response.content)
	#return response.content
	pass


def testMethod000():
	#registerUser()
	signInUser()
	#userID = "6773262ae51c479a95eca4d326a358f7e41ee9406039e889"
	#Adds Card addCardUser(userID)
	#addAddress(userID)
	
	testAddress = "351 Massachusetts Ave, Cambridge MA, 02139"
	print("Nearby Restaurants to: " , testAddress)
	retVal = searchAddress(addr=testAddress)
	#return
	print(retVal)
	
	restAPiCare = "169f8819f931921f884225aec137a02ac292d4ccea4ffdd8" #This is the API key for the restaurant. 
	#restapiCare = "169f8819f931921ff15b4f2e73e76180ceaf86853e1bc0c4"
	print("Menu at: " + str(restAPiCare))
	getMenu(restAPiCare)
	itemID = "6635138"
	specificID = "6635138"
	print("Ordering: " + itemID + " and " + specificID)
	#orderItem(restAPiCare,itemID,specificID)

	#Want to order: 11947789


	#6634029

	#This is for the rest





def testMethod001():

	registerUser()
	signInUser()
	addCardUser()
	searchAddress()
	#This now has a registered user

def testMethod002():
	pass


testMethod000()



