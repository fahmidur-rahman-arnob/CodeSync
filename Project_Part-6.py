# CodeSync - Part 6
# Input Validation and Improved Error Handling
#
# Part 6 builds on the complete workflow from Part 5.
#
# Part 5 already supports:
# 1. GitHub API authentication
# 2. Filename and GitHub path generation
# 3. Local solution file reading
# 4. New file creation
# 5. Existing file detection
# 6. Existing file update
# 7. Duplicate content detection
#
# Part 6 adds:
# 8. Input validation
# 9. Empty input protection
# 10. Better handling of unsupported languages
# 11. Better commit message validation
# 12. Better protection against unnecessary API requests


import os
import base64
import requests

from requests.exceptions import HTTPError
from dotenv import load_dotenv


# ENVIRONMENT VARIABLE CONFIGURATION
#
# The GitHub Personal Access Token is stored inside a .env file.
#
# Example:
#
# GITHUB_TOKEN=your_actual_github_token
#
# We should NEVER write the actual token directly inside
# this Python source code.
#
# load_dotenv() searches for the .env file and loads the
# variables into the current environment.
#
# After this:
#
# os.getenv("GITHUB_TOKEN")
#
# can be used to retrieve the token.
#

load_dotenv()


# PART 3: SOLUTION FILE PREPARATION
#
# This function decides:
#
# 1. What filename should be used on GitHub?
# 2. Which language directory should contain the file?
# 3. What complete GitHub path should be used?
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
#
# Filename:
#     two-sum.py
#
# GitHub path:
#     python/two-sum.py
#

def get_file_info(problem_name, language):

    # Each supported programming language has:
    #
    # extension -> file extension
    # directory -> GitHub folder
    #
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

    # Convert the problem name to lowercase and split it
    # into separate words.
    #
    # Example:
    #
    # "Two Sum"
    #
    # becomes:
    #
    # ["two", "sum"]
    #
    # Then join them using "-":
    #
    # "two-sum"
    #
    normalized_name = "-".join(
        problem_name.lower().split()
    )

    # Search for the selected programming language.
    #
    # language.lower() makes the input case-insensitive.
    #
    # So:
    #
    # Python
    # PYTHON
    # python
    #
    # will all become:
    #
    # python
    #
    language_data = language_info.get(
        language.lower()
    )

    # If the language does not exist in language_info,
    # get() returns None.
    #
    # Returning None tells the main program that the
    # language is unsupported.
    #
    if language_data is None:
        return None

    # Extract the extension and directory.
    extension = language_data["extension"]
    directory = language_data["directory"]

    # Create the final filename.
    #
    # Example:
    #
    # normalized_name = "two-sum"
    # extension = ".py"
    #
    # filename = "two-sum.py"
    #
    filename = f"{normalized_name}{extension}"

    # Create the complete GitHub path.
    #
    # Example:
    #
    # directory = "python"
    # filename = "two-sum.py"
    #
    # Result:
    #
    # python/two-sum.py
    #
    github_path = f"{directory}/{filename}"

    return filename, github_path


# PART 4 + PART 5 + PART 6
# GITHUB FILE CREATE / UPDATE / DUPLICATE DETECTION
#
# This function handles communication with GitHub.
#
# There are three possible situations:
#
# 1. File does not exist
#       -> Create a new file
#
# 2. File exists but content is different
#       -> Update the existing file
#
# 3. File exists and content is identical
#       -> Do nothing
#
# Part 6 keeps this logic from Part 5 and adds stronger
# protection around the API interaction.
#

def upload_file_to_github(
    owner,
    repo,
    github_path,
    file_content,
    commit_msg
):

    # GITHUB TOKEN
    #
    # Retrieve the GitHub token from the environment.
    #
    token = os.getenv("GITHUB_TOKEN")

    # If the token is missing, there is no reason to continue.
    #
    # We return before making any API request.
    #
    if not token:

        print(
            "\nError: GITHUB_TOKEN was not found."
        )

        print(
            "Check that your .env file exists "
            "and contains GITHUB_TOKEN."
        )

        return

    # REQUEST HEADERS
    #
    # These headers are sent with every GitHub API request.
    #
    headers = {

        # Authentication using the GitHub token.
        "Authorization": f"Bearer {token}",

        # Tell GitHub that we are using the GitHub JSON API.
        "Accept": "application/vnd.github+json",

        # Specify the GitHub API version.
        "X-GitHub-Api-Version": "2022-11-28",

        # Identify our application to GitHub.
        "User-Agent": "Python-CodeSync"
    }

    # BASE64 ENCODING
    #
    # GitHub Contents API expects file content as Base64.
    #
    # Our local file content is a normal Python string.
    #
    # Example:
    #
    # "print('Hello')"
    #
    # First:
    #
    # string -> UTF-8 bytes
    #
    # Then:
    #
    # UTF-8 bytes -> Base64 bytes
    #
    # Finally:
    #
    # Base64 bytes -> Base64 string
    #

    encoded_content = base64.b64encode(
        file_content.encode("utf-8")
    ).decode("utf-8")

    # GITHUB API URL
    #
    # GitHub Contents API endpoint:
    #
    # https://api.github.com/repos/{owner}/{repo}/contents/{path}
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
    #

    url = (
        f"https://api.github.com/repos/"
        f"{owner}/{repo}/contents/{github_path}"
    )

    # INITIAL PAYLOAD
    #
    # GitHub needs:
    #
    # message -> commit message
    # content -> Base64 encoded file content
    #
    # If the file already exists, we will later add:
    #
    # sha -> current SHA of the GitHub file
    #
    payload = {

        "message": commit_msg,
        "content": encoded_content
    }

    # These variables start as None.
    #
    # If an error occurs later, we can safely check which
    # request produced the error.
    #
    response = None
    existing_file_response = None

    try:

        # STEP 1: CHECK WHETHER THE FILE ALREADY EXISTS
        #
        # We send a GET request to the file's GitHub path.
        #
        # If GitHub returns:
        #
        # 200 -> file exists
        # 404 -> file does not exist
        #
        existing_file_response = requests.get(
            url,
            headers=headers,
            timeout=30
        )

        # FILE ALREADY EXISTS

        if existing_file_response.status_code == 200:

            # Convert GitHub's JSON response into a Python dict.
            existing_file_data = (
                existing_file_response.json()
            )

            # GitHub requires the existing file's SHA when
            # updating that file.
            #
            # Without the SHA, GitHub cannot safely update
            # the existing file.
            #
            payload["sha"] = existing_file_data["sha"]

            # GET CURRENT GITHUB CONTENT
            #
            # GitHub returns the existing file content as
            # Base64 encoded data.
            #
            # Sometimes the Base64 string contains newline
            # characters, so we remove them first.
            #
            github_encoded_content = (
                existing_file_data["content"]
                .replace("\n", "")
            )

            # Decode the Base64 content back into normal text.
            #
            # This allows us to compare the GitHub file with
            # our local file.
            #
            github_content = base64.b64decode(
                github_encoded_content
            ).decode("utf-8")

            # DUPLICATE CONTENT CHECK
            #
            # If the local file content and GitHub content
            # are exactly the same, there is no reason to
            # create another commit.
            #
            if file_content == github_content:

                print(
                    "\nNo changes detected."
                )

                print(
                    "GitHub file is already up to date."
                )

                # Stop the function.
                #
                # This prevents an unnecessary PUT request
                # and unnecessary GitHub commit.
                #
                return

            # If we reach here, the file exists but its
            # content is different from the local file.
            #
            print(
                "\nExisting file found."
            )

            print(
                "It will be updated."
            )

        # FILE DOES NOT EXIST

        elif existing_file_response.status_code == 404:

            # No SHA is required when creating a completely
            # new file.
            #
            print(
                "\nFile does not exist yet."
            )

            print(
                "A new file will be created."
            )

        # UNEXPECTED GET RESPONSE

        else:

            # If the response is something other than 200
            # or 404, raise an HTTP error.
            #
            # Examples:
            #
            # 401 -> authentication problem
            # 403 -> permission/rate-limit problem
            # 500 -> GitHub server problem
            #
            existing_file_response.raise_for_status()

        # STEP 2: CREATE OR UPDATE THE FILE
        #
        # If the file is new:
        #
        # -> GitHub creates it.
        #
        # If the file exists:
        #
        # -> GitHub updates it using the SHA.
        #
        print(
            "\nUploading file to GitHub..."
        )

        response = requests.put(
            url,
            headers=headers,
            json=payload,
            timeout=30
        )

        # If GitHub returns a 4xx or 5xx response,
        # raise_for_status() creates an HTTPError.
        #
        response.raise_for_status()

    # HTTP ERROR
    #
    # Handles HTTP errors returned by GitHub.
    #
    except HTTPError as http_err:

        print(
            f"\nHTTP error occurred: {http_err}"
        )

        # If the PUT request caused the error,
        # show its response.
        if response is not None:

            print(
                f"Response Details: {response.text}"
            )

        # Otherwise, the GET request probably failed.
        elif existing_file_response is not None:

            print(
                "Response Details: "
                f"{existing_file_response.text}"
            )

        return

    # NETWORK / REQUEST ERROR
    #
    # Handles problems such as:
    #
    # - Internet connection failure
    # - Timeout
    # - DNS problem
    # - Connection reset
    #
    except requests.RequestException as err:

        print(
            f"\nRequest error occurred: {err}"
        )

        return

    # JSON / DATA PROCESSING ERROR
    #
    # ValueError:
    # GitHub returned data that could not be processed.
    #
    # KeyError:
    # Expected data such as "sha" was missing.
    #
    except (ValueError, KeyError) as err:

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
    #
    # If the PUT request was successful, GitHub returns
    # information about:
    #
    # - the uploaded file
    # - the created commit
    #
    try:

        response_data = response.json()

        print(
            "\nFile uploaded/updated successfully!"
        )

        # Display the path of the file inside GitHub.
        print(
            f"File path: "
            f"{response_data['content']['path']}"
        )

        # Display the SHA of the new commit.
        print(
            f"Commit SHA: "
            f"{response_data['commit']['sha']}"
        )

    except (ValueError, KeyError) as err:

        print(
            "\nThe request succeeded, but the response "
            f"could not be processed correctly: {err}"
        )


# MAIN PROGRAM(CHAT GPT HELPED A LOT WITH THE LOGICS & FIXING BUGS)
#
# The main program connects all the previous parts together.
#
# Complete workflow:
#
# User Input
#     ↓
# Validate GitHub username
#     ↓
# Validate repository
#     ↓
# Validate problem name
#     ↓
# Validate programming language
#     ↓
# Generate filename + GitHub path
#     ↓
# Validate local file path
#     ↓
# Read solution file
#     ↓
# Validate commit message
#     ↓
# Check GitHub
#     ↓
# ┌─────────────────────────────┐
# │ File exists?                │
# └─────────────────────────────┘
#       ↓                ↓
#      YES              NO
#       ↓                ↓
# Compare content     Create file
#       ↓
# Same? ───── YES ───> Stop
#       │
#       NO
#       ↓
#     Update
#

if __name__ == "__main__":

    print(
        "=== CodeSync Part 6 ==="
    )

    # GITHUB USERNAME VALIDATION
    #
    # strip() removes spaces from the beginning and end.
    #
    # Example:
    #
    # "  arnob  "
    #
    # becomes:
    #
    # "arnob"
    #
    owner = input(
        "Enter GitHub Username: "
    ).strip()

    # Check whether the username is empty.
    #
    # If the user only presses Enter,
    # owner becomes an empty string.
    #
    if not owner:

        print(
            "Error: GitHub username cannot be empty."
        )

        raise SystemExit

    # REPOSITORY VALIDATION

    repo = input(
        "Enter Repository Name: "
    ).strip()

    if not repo:

        print(
            "Error: Repository name cannot be empty."
        )

        raise SystemExit

    # PROBLEM NAME VALIDATION

    problem_name = input(
        "Enter LeetCode Problem Name: "
    ).strip()

    if not problem_name:

        print(
            "Error: Problem name cannot be empty."
        )

        raise SystemExit

    # PROGRAMMING LANGUAGE VALIDATION

    language = input(
        "Enter Programming Language: "
    ).strip()

    if not language:

        print(
            "Error: Programming language cannot be empty."
        )

        raise SystemExit

    # PART 3: GENERATE FILE INFORMATION
    #
    # get_file_info() checks whether the selected language
    # is supported and creates the correct filename/path.
    #

    file_info = get_file_info(
        problem_name,
        language
    )

    # None means the language was not found in our
    # supported language dictionary.
    #
    if file_info is None:

        print(
            f"Error: '{language}' is not a supported language."
        )

        print(
            "Supported languages: "
            "Python, C++, Java, Golang, C, JavaScript."
        )

        raise SystemExit

    # Extract the filename and GitHub path.
    filename, github_path = file_info

    print(
        f"\nPrepared Filename: {filename}"
    )

    print(
        f"Prepared GitHub Path: {github_path}"
    )

    # LOCAL FILE PATH VALIDATION
    #
    # The user provides the location of the local solution
    # file.
    #
    # Example:
    #
    # F:\ALL ABOUT PYTHON\LEETCODE\EASY\Two_Sum.py
    #

    local_file_path = input(
        "\nEnter Solution File Path: "
    ).strip().strip('"').strip("'")

    # Prevent an empty file path from being passed to open().
    #
    if not local_file_path:

        print(
            "Error: Solution file path cannot be empty."
        )

        raise SystemExit

    # READ LOCAL SOLUTION FILE

    try:

        # Open the solution file in read mode.
        #
        # encoding="utf-8" allows Python to correctly read
        # normal source-code text.
        #
        with open(
            local_file_path,
            "r",
            encoding="utf-8"
        ) as solution_file:

            # Read the complete source code into a string.
            file_content = solution_file.read()

    # FILE NOT FOUND

    except FileNotFoundError:

        print(
            "\nError: The specified solution file "
            "was not found."
        )

        raise SystemExit

    # PERMISSION ERROR

    except PermissionError:

        print(
            "\nError: Permission denied while "
            "reading the solution file."
        )

        raise SystemExit

    # OTHER FILE SYSTEM ERROR

    except OSError as err:

        print(
            f"\nError while reading the solution file: {err}"
        )

        raise SystemExit

    # EMPTY FILE VALIDATION
    #
    # A file may exist but contain no code.
    #
    # We do not want CodeSync to upload an empty solution
    # accidentally.
    #
    # strip() is used only for checking.
    #
    # It does NOT modify file_content.
    #

    if not file_content.strip():

        print(
            "\nError: The solution file is empty."
        )

        raise SystemExit

    # COMMIT MESSAGE VALIDATION
    #
    # GitHub commits need a meaningful commit message.
    #
    commit_msg = input(
        "Enter Commit Message: "
    ).strip()

    if not commit_msg:

        print(
            "Error: Commit message cannot be empty."
        )

        raise SystemExit

    # UPLOAD / UPDATE
    #
    # All required input has now been validated.
    #
    # The program can safely call the GitHub upload function.
    #

    upload_file_to_github(
        owner,
        repo,
        github_path,
        file_content,
        commit_msg
    )