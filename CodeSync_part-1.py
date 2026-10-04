# ============================================================
# SANDBOX 01 — GitHub API Research & Concept Practice
# ============================================================
# This sandbox was written before implementing the main
# CodeSync Part 1 functionality to independently practice
# GitHub REST API requests, JSON parsing, and error handling.
# ============================================================

import requests
from requests.exceptions import HTTPError



def get_github_data (username) : 
    github_url = f"https://api.github.com/users/{username}"

    #send the GET Request
    response = requests.get(github_url)

    response.raise_for_status()

    if response.status_code == 200 : 
        user_data = response.json()
        return user_data


    #if the status_code is 404 program wont reach here because I've usedraise_for_status() method above...so this is a great way for errorhandlinga and compact code writing...
    # elif response.status_code == 404 : 
    #     print(f"User {username} not found.")
    #     return None

    else : 
        print(f"Failed to fetch data. Status Code {response.status_code}")
        return None
    #example user 
    
try:
    data = get_github_data("fahmidur-rahman-arnob")

    if data : 
        print(f"Name: {data.get('name')}")
        print(f"UserName: {data.get('login')}")
        print(f"Bio: {data.get('bio')}")
        print(f"Public Repos: {data.get('public_repos')}")
        print(f"Following: {data.get('following')}")
        print(f"Follwoers: {data.get('followers')}")

except HTTPError as http_err : 
    print(f"HTTP error occured: {http_err}")
except Exception as err : 
    print(f"Other error occured: {err}")