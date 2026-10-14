username = input("Enter Your Username: ").strip()
repo = input("Enter Your Repo Name: ").strip()

if username == "" and repo == "" : 
    print("Username Can't Be Empty.")
    print("Repo Cant Be Empty.")

else : 
    print(f"{username}")
    print(f"{repo}")
