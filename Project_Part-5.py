# CodeSync - Part 5
# Duplicate Detection and Existing File Update
#
# Part 5 integrates the previous CodeSync components
# into one complete workflow.
#
# Current functionality:
# 1. Load GitHub token from .env
# 2. Prepare GitHub filename and path
# 3. Read a local solution file
# 4. Check whether the destination file already exists
# 5. Create a new file if it does not exist
# 6. Update the existing file if it already exists
# 7. Handle HTTP, network, file, and response errors


import os
import base64
import requests

from requests.exceptions import HTTPError
from dotenv import load_dotenv


# CODESYNC — ENVIRONMENT VARIABLE CONFIGURATION
#
# We use a .env file to keep the GitHub token separate
# from the Python source code.
#
# Example .env file:
#
# GITHUB_TOKEN=your_actual_github_token
#
# IMPORTANT:
# - Never commit .env to GitHub.
# - Add .env to .gitignore.
# - Never expose the token publicly.
# - If the token is exposed, revoke it and create a new one.
#
# load_dotenv() loads variables from the local .env file
# into the current process environment.
#
# After loading, os.getenv("GITHUB_TOKEN") can retrieve
# the token normally.

load_dotenv()


# PART 3: SOLUTION FILE PREPARATION
#
# Goal:
# Prepare the filename and destination path for a solution.
#
# Example:
#
# Problem:
#     Two Sum
#
# Language:
#     Python
#
# Result:
#     Filename: two-sum.py
#     GitHub Path: python/two-sum.py
#
# Part 3 determines WHERE the solution should be stored
# inside the GitHub repository.


def get_file_info(problem_name, language):

    language_info = {
        "python": {
            "extension": ".py",
            "directory": "python"
        },
        "c++": {
            "extension": ".cpp",
            "directory": "cpp"
        },
        "java": {
            "extension": ".java",
            "directory": "java"
        },
        "golang": {
            "extension": ".go",
            "directory": "go"
        },
        "c": {
            "extension": ".c",
            "directory": "c"
        },
        "javascript": {
            "extension": ".js",
            "directory": "javascript"
        }
    }

    # Convert the problem name into a GitHub-friendly filename.
    #
    # Example:
    # "Two Sum" -> "two-sum"
    normalized_name = "-".join(
        problem_name.lower().split()
    )

    # Find the extension and directory for the selected language.
    language_data = language_info.get(
        language.lower()
    )

    # Stop if the language is unsupported.
    if language_data is None:
        return None

    extension = language_data["extension"]
    directory = language_data["directory"]

    filename = f"{normalized_name}{extension}"
    github_path = f"{directory}/{filename}"

    return filename, github_path


# PART 4 + PART 5: GITHUB FILE UPLOAD / UPDATE
#
# Part 3 determines WHERE the file goes.
#
# This function determines HOW the file is uploaded.
#
# Workflow:
#
# Local file
#     ↓
# Read file content
#     ↓
# Convert content to Base64
#     ↓
# Check GitHub destination
#     ↓
# ┌───────────────────────────────┐
# │ Does the file already exist?  │
# └───────────────────────────────┘
#        ↓                 ↓
#       YES               NO
#        ↓                 ↓
# Get existing SHA       No SHA needed
#        ↓                 ↓
#       PUT               PUT
#        ↓                 ↓
#       UPDATE           CREATE
#
# GitHub requires the existing file's SHA when updating it.


def upload_file_to_github(
    owner,
    repo,
    github_path,
    file_content,
    commit_msg
):

    # GITHUB TOKEN

    # Retrieve the GitHub token loaded from the .env file.
    token = os.getenv("GITHUB_TOKEN")

    # Stop if the token could not be found.
    if not token:
        print(
            "Error: GITHUB_TOKEN was not found.\n"
            "Check that your .env file exists, contains "
            "GITHUB_TOKEN=your_token, and is being loaded."
        )
        return

    # REQUEST HEADERS

    # Headers tell GitHub how we want to authenticate
    # and communicate with the API.
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "Python-CodeSync"
    }

    # BASE64 ENCODING
    #
    # GitHub Contents API expects the file content in Base64.
    #
    # Original string
    #       ↓
    # UTF-8 bytes
    #       ↓
    # Base64 bytes
    #       ↓
    # Base64 string

    encoded_content = base64.b64encode(
        file_content.encode("utf-8")
    ).decode("utf-8")

    # GITHUB API URL
    #
    # Example:
    #
    # owner = fahmidur-rahman-arnob
    # repo = Leetcode_Solutions
    # github_path = python/two-sum.py
    #
    # Result:
    #
    # https://api.github.com/repos/
    # fahmidur-rahman-arnob/
    # Leetcode_Solutions/
    # contents/python/two-sum.py

    url = (
        f"https://api.github.com/repos/"
        f"{owner}/{repo}/contents/{github_path}"
    )

    # INITIAL PAYLOAD
    #
    # For a new file, GitHub needs:
    #
    # message
    # content
    #
    # For an existing file, we will add:
    #
    # sha

    payload = {
        "message": commit_msg,
        "content": encoded_content
    }

    # These variables are initialized as None so that
    # the error handler can safely inspect them later.

    response = None
    existing_file_response = None

    try:

        # STEP 1: CHECK WHETHER THE FILE ALREADY EXISTS

        existing_file_response = requests.get(
            url,
            headers=headers,
            timeout=30
        )

        #Content Comparison and debugging 
        if existing_file_response.status_code == 200:
            existing_file_data = existing_file_response.json()
            payload["sha"] = existing_file_data["sha"]

            github_encoded_content = existing_file_data["content"].replace("\n", "")
            github_content = base64.b64decode(
                github_encoded_content
            ).decode("utf-8")

            if file_content == github_content:
                print("No changes detected. GitHub file is already up to date.")
                return

            print("Existing file found. It will be updated.")

        # FILE DOES NOT EXIST

        elif existing_file_response.status_code == 404:

            # No SHA is required when creating a new file.
            print(
                "File does not exist yet. "
                "A new file will be created."
            )

        # UNEXPECTED RESPONSE

        else:

            # This can catch problems such as:
            # - authentication failure
            # - permission problems
            # - invalid repository
            # - rate limiting
            #
            # raise_for_status() converts an HTTP error status
            # into an HTTPError exception.

            existing_file_response.raise_for_status()

        # STEP 2: CREATE OR UPDATE THE FILE

        print("\nUploading file to GitHub...")

        response = requests.put(
            url,
            headers=headers,
            json=payload,
            timeout=30
        )

        # Raise HTTPError if GitHub returns a 4xx or 5xx status.
        response.raise_for_status()

    # HTTP ERROR

    except HTTPError as http_err:

        print(
            f"\nHTTP error occurred: {http_err}"
        )

        # If the PUT request produced the error,
        # show its response.
        if response is not None:

            print(
                f"Response Details: {response.text}"
            )

        # Otherwise, show the GET response that failed.
        elif existing_file_response is not None:

            print(
                "Response Details: "
                f"{existing_file_response.text}"
            )

        return

    # REQUEST / NETWORK ERROR

    except requests.RequestException as err:

        # Handles request-related problems such as:
        # - connection failure
        # - timeout
        # - DNS/network problems

        print(
            f"\nRequest error occurred: {err}"
        )

        return

    # JSON / DATA PROCESSING ERROR

    except (ValueError, KeyError) as err:

        # ValueError:
        # GitHub response could not be processed as JSON.
        #
        # KeyError:
        # Expected data such as "sha" was missing.

        print(
            f"\nCould not process GitHub's response: {err}"
        )

        return

    # UNEXPECTED ERROR

    except Exception as err:

        print(
            f"\nAn unexpected error occurred: {err}"
        )

        return

    # PROCESS SUCCESSFUL RESPONSE

    try:

        response_data = response.json()

        print(
            "\nFile uploaded/updated successfully!"
        )

        # Path of the file inside GitHub.
        print(
            f"File path: "
            f"{response_data['content']['path']}"
        )

        # SHA of the commit created by this operation.
        print(
            f"Commit SHA: "
            f"{response_data['commit']['sha']}"
        )

    except (ValueError, KeyError) as err:

        print(
            "\nThe request succeeded, but the response "
            f"could not be processed correctly: {err}"
        )


# MAIN PROGRAM
#
# The main program connects Part 3 and Part 4/5.
#
# Workflow:
#
# User Input
#     ↓
# GitHub username
#     ↓
# Repository
#     ↓
# Problem name
#     ↓
# Programming language
#     ↓
# Generate filename + GitHub path
#     ↓
# Ask for local solution file
#     ↓
# Read complete file content
#     ↓
# Ask commit message
#     ↓
# Check GitHub
#     ↓
# Create OR Update



if __name__ == "__main__":

    print("=== CodeSync Part 5 ===")

    # BASIC GITHUB INFORMATION

    owner = input(
        "Enter GitHub Username: "
    ).strip()

    repo = input(
        "Enter Repository Name: "
    ).strip()

    # PROBLEM INFORMATION

    problem_name = input(
        "Enter LeetCode Problem Name: "
    ).strip()

    language = input(
        "Enter Programming Language: "
    ).strip()

    # PART 3: PREPARE GITHUB DESTINATION PATH

    file_info = get_file_info(
        problem_name,
        language
    )

    # Stop if the selected language is unsupported.
    if file_info is None:

        print(
            f"Error: {language} "
            "is not a supported language."
        )

    else:

        filename, github_path = file_info

        print(
            f"\nPrepared Filename: {filename}"
        )

        print(
            f"Prepared GitHub Path: {github_path}"
        )

        # READ LOCAL SOLUTION FILE
        #
        # CodeSync works with an existing source file instead
        # of asking the user to paste the complete code into
        # the terminal.
        #
        # Example:
        #
        # F:\ALL ABOUT PYTHON\LEETCODE\EASY\Two_Sum.py

        local_file_path = input(
            "\nEnter Solution File Path: "
        ).strip().strip('"').strip("'")

        try:

            # Open the local solution file in read mode.
            with open(
                local_file_path,
                "r",
                encoding="utf-8"
            ) as solution_file:

                # Read the complete source code
                # into a Python string.
                file_content = solution_file.read()

        # FILE NOT FOUND

        except FileNotFoundError:

            print(
                "\nError: The specified solution "
                "file was not found."
            )

        # PERMISSION ERROR        

        except PermissionError:

            print(
                "\nError: Permission denied while "
                "reading the solution file."
            )

        # OTHER FILE SYSTEM ERROR

        except OSError as err:

            print(
                f"\nError while reading the "
                f"solution file: {err}"
            )

        # FILE WAS READ SUCCESSFULLY

        else:

            # Ask the user for the Git commit message.
            commit_msg = input(
                "Enter Commit Message: "
            ).strip()

            # UPLOAD / UPDATE
            

            upload_file_to_github(
                owner,
                repo,
                github_path,
                file_content,
                commit_msg
            )