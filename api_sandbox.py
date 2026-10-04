#public API theke data ber korar jonno amdr first e ekta GET request pathate hobe 
# tarpor response take python er dict. e convert korte hobe 
# and then shei dictionary theke easily name username and email ber kora jabe


#program

#first e request library import korte hobe 
import requests
from requests.exceptions import HTTPError

#ekta public API url lagbe ... jeta user Data provide kore & shetake ekta variable er moddhe as a string store korte hobe

public_api_url = "https://dragonball-api.com/api/characters?race=Saiyan&affiliation=Z fighter"

#ekhon ei API er kache amader GET request pathathe hobe request library use kore

# response = requests.get(public_api_url)

def process_character(character) : 
    print(character["name"])
    print(character["ki"])
    print(character["maxKi"])

#ekhon amra check korbo j request ta successful hoyeche ki-na with the status code 200...meaning server jodi 200 return kore tahole successful hoyeche
try : 
    response = requests.get(public_api_url)

    #if the response was successful, nothing happens. If it's a 404, 500, etc it jumps straigt to the except block.
    response.raise_for_status() #this is a built-in method used to automatically throw an exception if an HTTP request fails. if a response is successful this method does nothing and returns none. if not then instantly raises an error requests.exceptions.HTTPError.

    if response.status_code == 200 :
    #json data ke dictionary te convert korte hobe ekhon  
        user_data = response.json()


        if isinstance(user_data, dict) : 
            #single resource 
            process_character(user_data)
        elif isinstance(user_data, list) :
            #multiple resource 
            # process_character(user_data, dict) : 
            # process_character(user_data)
            for character in user_data : 
                process_character(character)

    else : 
        print(f"Data is not available. CODE {response.status_code}")

except HTTPError as http_err : 
    print(f"HTTP error occured: {http_err}")
except Exception as err : 
    print(f"Other error occured: {err}")
