# ============================================================
# CODESYNC — PART 2: GITHUB REPOSITORY SELECTION & VERIFICATION
# ============================================================
#
# Goal:
# The purpose of Part 2 is to verify that the GitHub repository
# selected for CodeSync exists and can be accessed before the
# application performs any further operation on it.
#
# In Part 1, I established basic communication between Python
# and the GitHub REST API and learned how to retrieve repository
# information from a GitHub endpoint.
#
# In Part 2, the focus is on validating the external resource
# before CodeSync continues with future operations such as
# creating or updating solution files.
#
# The implementation accepts a GitHub repository owner and
# repository name from the user and sends a GET request to the
# corresponding GitHub repository endpoint.
#
# Repository endpoint:
#     /repos/{owner}/{repo}
#
# The response is then handled according to its HTTP status.
#
# Successful request:
#     - raise_for_status() completes without raising an error.
#     - The repository is considered accessible.
#     - The JSON response is parsed.
#     - Relevant repository information is returned.
#
# Repository not found:
#     - GitHub returns HTTP 404.
#     - raise_for_status() raises an HTTPError.
#     - The exception response is checked to identify the 404.
#     - The user is informed that the repository does not exist.
#
# Other HTTP errors:
#     - Other 4xx/5xx responses are handled through HTTPError.
#     - The corresponding error is displayed instead of allowing
#       the application to fail silently.
#
# Concepts applied from the Part 2 sandbox:
# - REST API communication
# - HTTP GET requests
# - HTTP status codes
# - raise_for_status()
# - HTTPError handling
# - Specific HTTP status detection
# - JSON response parsing
# - Nested dictionary access
# - Python functions and return values
# - Conditional logic
# - General exception handling
#
# The repository information returned by this function will
# provide the foundation for later CodeSync operations.
# Future parts can use the verified repository to prepare and
# upload LeetCode solution files through the GitHub API.
#
# This separation also keeps repository verification logic
# independent from future file preparation and upload logic.
# ============================================================


# ============================================================
# MAIN IMPLEMENTATION
# ============================================================
#
# This section contains the actual CodeSync Part 2
# implementation.
#
# The logic developed and tested independently in Sandbox 02
# is now applied to the main project.
#
# The function below is responsible for communicating with
# GitHub, verifying the repository, and returning its data.
# ============================================================



import requests
from requests.exceptions import HTTPError



def github_repo_data (owner, repo) : 
    github_url = f"https://api.github.com/repos/{owner}/{repo}"

    #send the GET Request
    response = requests.get(github_url)

    response.raise_for_status()

    print("Repository Exists.")
    repo_data = response.json()
    return repo_data
    
try:
    owner = input("Enter The Owner's UserName: ") #string
    repo = input("Enter The Repository Name: ") #string
    data = github_repo_data(owner, repo)

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