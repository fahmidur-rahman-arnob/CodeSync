#public API theke data ber korar jonno amdr first e ekta GET request pathate hobe 
# tarpor response take python er dict. e convert korte hobe 
# and then shei dictionary theke easily name username and email ber kora jabe


#program

#first e request library import korte hobe 
import requests

#ekta public API url lagbe ... jeta user Data provide kore & shetake ekta variable er moddhe as a string store korte hobe

public_api_url = "https://dragonball-api.com/api/characters?race=Saiyan&affiliation=Z fighter"

#ekhon ei API er kache amader GET request pathathe hobe request library use kore

response = requests.get(public_api_url)

def process_character(character) : 
    print(character["name"])
    print(character["ki"])
    print(character["maxKi"])

#ekhon amra check korbo j request ta successful hoyeche ki-na with the status code 200...meaning server jodi 200 return kore tahole successful hoyeche
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

    # erpor amader necessary data gulo ber kora 

    # for data in user_data : 

    #     if isinstance(user_data, dict) :
    #         # single resource 
    #         process_character(data)

    #     elif isinstance(user_data, dict) : 
    #         for character in user_data : 
    #             process_character(character)
        # elif isinstance(data, list) : 
        #     for character in data : 
        #         process_character(character)

        # name = data["name"]
        # ki = data["ki"]
        # max_ki = data["maxKi"]

        #now output dekhabo 

        # print(f"name: {name}")
        # print(f"username: {ki}")
        # print(f"Email: {max_ki}")
        # print("-" * 30) 

else : 
    print(f"Data is not available. CODE {response.status_code}")
