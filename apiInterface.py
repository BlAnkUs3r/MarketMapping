import requests

client_id = '6Zv_bgjmdOehtmakdfNyTA'
API_KEY = 'N06Aar1UJU0EhdRbAgDPe49b5h2XmpUqQtYh5mL9IbFtngTx0s4XMH_uu5SrVGNPsHk-h4MXPzRXTqr_WB7EuEn09FSLzUcVjC-9Ar98yAzilSBy10AFYj08b25pZXYx'
ENDPOINT = 'https://api.yelp.com/v3/businesses/search'
HEADERS = {'Authorization': 'bearer %s' % API_KEY}


#parameters = {'location':'Theory Syracuse',
#              'limit':20,
#              'categories':'markets,pharmacy,grocery',
#              'open_now':True,
#              'radius': 5000,
#              }

#response = requests.get(url = ENDPOINT, params= PARAMETERS, headers=HEADERS)

#data = response.json()

#print(data)

def getStoreInfoNoSearch(location):
    parameters = {'location':location,
              'limit':35,
              'categories':'markets,convenience,grocery,electronics',
              'open_now':True,
              'radius': 10000,
              }
    
    
    response = requests.get(url = ENDPOINT, params= parameters, headers=HEADERS)

    data = response.json()

    return data

def getStoreInfoWithSearch(location, searchString):
    parameters = {
              'location':location,
              'term':searchString,
              'limit':35,
              'categories':'markets,convenience,grocery,electronics,restuarants,fashion,computers,',
              'open_now':True,
              'radius': 10000,
              }
    response = requests.get(url = ENDPOINT, params= parameters, headers=HEADERS)

    data = response.json()

    return data
