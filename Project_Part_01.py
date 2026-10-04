# ============================================================
# CODESYNC — PART 1: GITHUB API INTEGRATION
# ============================================================
#
# Goal:
# The purpose of Part 1 is to establish communication between
# CodeSync and the GitHub REST API.
#
# Before implementing the main project functionality, I first
# created a separate API sandbox to independently research and
# practice REST API requests, JSON parsing, response handling,
# and HTTP error handling.
#
# After understanding and testing those concepts in the
# sandbox, I applied them here to the actual CodeSync project.
#
# Part 1 currently allows the user to provide a GitHub
# repository owner and repository name, then retrieves and
# displays basic repository information through the GitHub API.
#
# Concepts applied:
# - Python functions
# - User input
# - REST API / HTTP GET requests
# - requests library
# - JSON response parsing
# - Dictionary and nested dictionary data extraction
# - HTTP error handling
# - Exception handling
# - Ternary operator
#
# Future parts will build on this foundation to implement
# GitHub file creation, updating, authentication, and the
# complete CodeSync synchronization workflow.
# ============================================================





import requests
from requests.exceptions import HTTPError



def github_data (owner, repo) : 
    github_url = f"https://api.github.com/repos/{owner}/{repo}"

    #send the GET Request
    response = requests.get(github_url)

    response.raise_for_status()

    user_data = response.json()
    return user_data
    
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
    print(f"HTTP error occured: {http_err}")
except Exception as err : 
    print(f"Other error occured: {err}")