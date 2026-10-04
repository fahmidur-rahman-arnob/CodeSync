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