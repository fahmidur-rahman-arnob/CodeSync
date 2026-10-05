# ============================================================
# CODESYNC — PART 2: REPOSITORY SELECTION & VERIFICATION
# ============================================================
#
# Goal:
# The purpose of Part 2 is to verify whether a GitHub
# repository exists and is accessible before CodeSync attempts
# to work with that repository.
#
# In Part 1, I learned how to communicate with the GitHub
# REST API, send GET requests, parse JSON responses, and
# extract repository information.
#
# Before implementing the next stage of CodeSync, I created
# a separate sandbox to research and practice how HTTP
# responses and errors should be handled when communicating
# with an external API.
#
# This sandbox focuses on understanding how:
# - HTTP status codes represent different outcomes
# - raise_for_status() handles unsuccessful HTTP responses
# - HTTPError can be caught and handled separately
# - A specific status code such as 404 can be identified
# - Successful API responses can be converted into JSON
# - Application logic can be based on API response status
#
# The main scenario practiced here is:
#
# Repository exists:
#     API returns a successful response
#     → continue execution
#     → parse repository information
#
# Repository does not exist:
#     API returns 404
#     → raise_for_status() raises HTTPError
#     → identify the 404 status
#     → inform the user that the repository doesn't exist
#
# Other HTTP errors:
#     API returns another 4xx/5xx status
#     → catch HTTPError
#     → display the corresponding error
#
# Concepts practiced:
# - Python functions
# - User input
# - REST API / HTTP GET requests
# - HTTP status codes
# - requests library
# - raise_for_status()
# - HTTPError exception
# - Specific exception handling
# - JSON response parsing
# - Dictionary and nested dictionary access
# - Conditional logic
# - General exception handling
#
# After understanding and testing these concepts in the
# sandbox, they will be applied to the actual CodeSync
# project in Part 2.
#
# Future parts will use this foundation to verify the target
# repository before CodeSync attempts to create or update
# solution files through the GitHub API.
# ============================================================


# ============================================================
# SANDBOX 02 — GITHUB REPOSITORY VERIFICATION
# ============================================================
#
# This sandbox was created before implementing the main
# CodeSync Part 2 functionality.
#
# The purpose of this sandbox was to independently research
# and practice:
# - GitHub repository API requests
# - HTTP response status codes
# - raise_for_status()
# - HTTPError handling
# - Detecting a 404 Not Found response
# - Handling different HTTP errors
# - Parsing successful JSON responses
# - Extracting repository information
#
# The main lesson from this sandbox was understanding that
# raise_for_status() does not return True or False to indicate
# whether a request was successful.
#
# Instead:
#
#     Successful response
#         → execution continues normally
#
#     Unsuccessful response
#         → an HTTPError is raised
#
# This allowed me to handle a 404 response separately from
# other HTTP errors before moving the logic into the main
# CodeSync project.
# ============================================================


import requests
from requests.exceptions import HTTPError



def github_data (owner, repo) : 
    github_url = f"https://api.github.com/repos/{owner}/{repo}"

    #send the GET Request
    response = requests.get(github_url)

    response.raise_for_status()

    # if exists : 
    print("Repository Exists.")
    user_data = response.json()
    return user_data
    # else : 
        # user_data = response.json()
        # return user_data
    
try:
    owner = input("Enter The Owner's UserName: ") #string
    repo = input("Enter The Repository Name: ") #string
    data = github_data(owner, repo)

    if data : 
        print(f"Owner of this repo: {data.get('owner', {}).get('login')}")
        print(f"Repo Name: {data.get('name')}")
        print(f"Description: {data.get('description')}")
        print("Private" if data.get('private') else "Public")
        print(f"Default Branch: {data.get('default_branch')}")

except HTTPError as http_err : 
    if http_err.response.status_code == 404 : 
        print("Repo Doesn't Exist.")
    else : 
        print(f"HTTP error occured: {http_err}")
except Exception as err : 
    print(f"Other error occured: {err}")