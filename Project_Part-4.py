
import os
import base64
import requests

from requests.exceptions import HTTPError
from dotenv import load_dotenv


# CODESYNC — ENVIRONMENT VARIABLE CONFIGURATION
# WHY ARE WE USING A .env FILE?
#
# In the earlier version of CodeSync, the GitHub token was
# retrieved using:
#
#     token = os.getenv("GITHUB_TOKEN")
#
# However, this approach only works when GITHUB_TOKEN is
# already available in the current process's environment.
#
# Previously, we had to configure the token manually through
# PowerShell before running the program.
#
# For example, in PowerShell:
#
#     $env:GITHUB_TOKEN = "your_github_token"
#
# This was inconvenient because:
#
# 1. We had to configure the token repeatedly in new
#    PowerShell sessions.
#
# 2. The configuration was tied to the current terminal
#    session unless we configured it persistently.
#
# 3. It made running and testing CodeSync less convenient.
#
# NEW APPROACH: .env + python-dotenv
#
# We now store the token in a local .env file and use the
# python-dotenv library to load it into the environment.
#
# The .env file contains:
#
#     GITHUB_TOKEN=your_actual_github_token
#
# The following function loads variables from that file:
#
#     load_dotenv()
#
# After loading, the existing os.getenv() call can retrieve
# GITHUB_TOKEN just like any other environment variable.
#
# WHY IS THIS BETTER FOR OUR DEVELOPMENT WORKFLOW?
#
# - We configure the token once in the local project.
# - We do not need to set it manually in every terminal session.
# - The token is kept separate from the Python source code.
# - We can share the project code without including the token.
# - We can use a different token on another machine without
#   modifying the Python implementation.
#
# IMPORTANT SECURITY NOTES:
#
# - The .env file is NOT automatically encrypted.
# - Do not commit or push .env to GitHub.
# - Add .env to .gitignore.
# - Never publish your token in source code, screenshots,
#   README files, or public repositories.
# - If a token is exposed, revoke it and create a replacement.
#
# NOTE:
# load_dotenv() normally searches for a .env file starting
# from the script's directory context and nearby directories.
# Keep .env in the CodeSync project folder for this project.


# Load environment variables from the local .env file.
#
# This must run before os.getenv("GITHUB_TOKEN") is called.
#
# By default, load_dotenv() does not overwrite an environment
# variable that already exists in the process environment.
# This lets an explicitly configured environment variable
# take precedence over the value in .env.
load_dotenv()

# CODESYNC — PART 3: SOLUTION FILE PREPARATION

# Goal:
# Prepare the GitHub destination path for a LeetCode solution.
#
# Example:
# Problem: Two Sum
# Language: Python
#
# Filename:
#     two-sum.py
#
# GitHub path:
#     python/two-sum.py
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

    # Convert the problem name to a GitHub-friendly filename.
    # Example: "Two Sum" -> "two-sum"
    normalized_name = "-".join(problem_name.lower().split())

    # Find the extension and directory for the selected language.
    language_data = language_info.get(language.lower())

    # Stop if the language is unsupported.
    if language_data is None:
        return None

    extension = language_data["extension"]
    directory = language_data["directory"]

    filename = f"{normalized_name}{extension}"
    github_path = f"{directory}/{filename}"

    return filename, github_path


# PART 4: GITHUB FILE UPLOAD

# Part 3 decides WHERE the solution goes.
# Part 4 handles HOW the solution is uploaded.
#
# Before uploading, this function checks whether the file
# already exists in the destination repository.
#
# New file:
#     Send message + Base64 content.
#
# Existing file:
#     Send message + Base64 content + existing file SHA.
#
# GitHub requires the SHA when updating an existing file.



def upload_file_to_github(
    owner,
    repo,
    github_path,
    file_content,
    commit_msg
):


    # GITHUB TOKEN CONFIGURATION — USING .env
    #
    # OLD APPROACH:
    #
    # Earlier, we had to configure the token manually in
    # PowerShell before running CodeSync:
    #
    #     $env:GITHUB_TOKEN = "your_github_token"
    #
    # That value was available to programs launched from
    # that PowerShell session, but a new session would not
    # automatically inherit a value configured only in the
    # previous session.
    #
    # NEW APPROACH:
    #
    # We now call load_dotenv() near the top of this file.
    # That loads variables from the local .env file into
    # the process environment.
    #
    # We can therefore keep using os.getenv() here.
    #
    # The token is not written directly into this Python file.
    # This separates configuration/secrets from application code.
    #
    # IMPORTANT:
    # A .env file is plain text, not an encrypted vault.
    # Its safety depends on keeping the file private and
    # preventing it from being committed to Git.

    token = os.getenv("GITHUB_TOKEN")

    if not token:
        print(
            "Error: GITHUB_TOKEN was not found.\n"
            "Check that your .env file exists, contains "
            "GITHUB_TOKEN=your_token, and is being loaded."
        )
        return

    # Prepare the headers used for GitHub API requests.
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "Python-CodeSync"
    }

    # GitHub Contents API expects file content in Base64 format.
    #
    # Original string
    #     -> UTF-8 bytes
    #     -> Base64 bytes
    #     -> Base64 string
    #
    # The local file content itself is not modified.
    encoded_content = base64.b64encode(
        file_content.encode("utf-8")
    ).decode("utf-8")

    # This is the DESTINATION path inside GitHub.
    # Example: python/two-sum.py
    url = (
        f"https://api.github.com/repos/"
        f"{owner}/{repo}/contents/{github_path}"
    )

    # Create the payload required by the GitHub Contents API.
    payload = {
        "message": commit_msg,
        "content": encoded_content
    }

    response = None
    existing_file_response = None

    try:


        # CHECK WHETHER THE DESTINATION FILE ALREADY EXISTS

        # HTTP 200: File exists; response includes its SHA.
        # HTTP 404: File does not exist; create a new file.
        #
        # GitHub requires the existing file's SHA when using
        # PUT to update that file.

        existing_file_response = requests.get(
            url,
            headers=headers,
            timeout=30
        )

        if existing_file_response.status_code == 200:

            existing_file_data = existing_file_response.json()

            # Include the current SHA for the update request.
            payload["sha"] = existing_file_data["sha"]

            print("Existing file found. It will be updated.")

        elif existing_file_response.status_code == 404:

            # No SHA is needed when creating a new file.
            print(
                "File does not exist yet. "
                "A new file will be created."
            )

        else:

            # Raise an error for unexpected HTTP responses,
            # such as authentication or permission errors.
            existing_file_response.raise_for_status()

        # UPLOAD OR UPDATE THE FILE

        print("\nUploading file to GitHub...")

        response = requests.put(
            url,
            headers=headers,
            json=payload,
            timeout=30
        )

        # Raise HTTPError if GitHub returns a 4xx or 5xx status.
        response.raise_for_status()

    except HTTPError as http_err:

        print(f"\nHTTP error occurred: {http_err}")

        # Display the response body to help diagnose API errors.
        if response is not None:
            print(f"Response Details: {response.text}")

        elif existing_file_response is not None:
            print(
                "Response Details: "
                f"{existing_file_response.text}"
            )

        return

    except requests.RequestException as err:

        # Handle network problems and other Requests-related errors.
        print(f"\nRequest error occurred: {err}")
        return

    except (ValueError, KeyError) as err:

        # Handle unexpected JSON data or a missing SHA field.
        print(f"\nCould not process GitHub's response: {err}")
        return

    except Exception as err:

        print(f"\nAn unexpected error occurred: {err}")
        return

    # DISPLAY THE SUCCESSFUL RESPONSE

    try:

        response_data = response.json()

        print("\nFile uploaded/updated successfully!")
        print(f"File path: {response_data['content']['path']}")
        print(f"Commit SHA: {response_data['commit']['sha']}")

    except (ValueError, KeyError) as err:

        print(
            "\nThe request succeeded, but the response "
            f"could not be processed correctly: {err}"
        )


# MAIN PROGRAM

# The main program connects Part 3 and Part 4.
#
# Local solution file
#       |
#       v
# Read complete file content
#       |
#       v
# Generate GitHub destination path
#       |
#       v
# Check if destination file exists
#       |
#       v
# Create or update through GitHub API


if __name__ == "__main__":

    print("=== CodeSync Part 4 ===")

    owner = input("Enter GitHub Username: ").strip()
    repo = input("Enter Repository Name: ").strip()

    problem_name = input(
        "Enter LeetCode Problem Name: "
    ).strip()

    language = input(
        "Enter Programming Language: "
    ).strip()


    # PART 3: PREPARE THE GITHUB DESTINATION PATH

    file_info = get_file_info(problem_name, language)

    if file_info is None:

        print(
            f"Error: {language} is not a supported language."
        )

    else:

        filename, github_path = file_info

        print(f"\nPrepared Filename: {filename}")
        print(f"Prepared GitHub Path: {github_path}")

        # ====================================================
        # OLD APPROACH: ASKING THE USER TO PASTE THE CODE
        # ====================================================
        #
        # Previously, we asked the user to paste the solution
        # directly into the terminal:
        #
        # file_content = input("\nEnter Solution Code: ")
        #
        # We are keeping the old approach commented out to
        # document why the design was changed.
        #
        # CodeSync should synchronize an existing source file.
        # Asking the user to paste multi-line code into input()
        # is inconvenient and makes formatting harder to manage.
        #
        # ====================================================

        # ----------------------------------------------------
        # NEW APPROACH: READ THE SOLUTION FROM A LOCAL FILE
        # ----------------------------------------------------
        #
        # Local path example:
        # F:\ALL ABOUT PYTHON\LEETCODE\EASY\Two_Sum.py
        #
        # GitHub destination example:
        # python/two-sum.py
        #
        # The local path tells CodeSync where to READ the code.
        # The GitHub path tells CodeSync where to STORE the code.
        # ----------------------------------------------------

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

                # Read the entire source code as a string.
                file_content = solution_file.read()

        except FileNotFoundError:

            print(
                "\nError: The specified solution file "
                "was not found."
            )

        except PermissionError:

            print(
                "\nError: Permission denied while reading "
                "the solution file."
            )

        except OSError as err:

            print(
                f"\nError while reading the solution file: {err}"
            )

        else:

            commit_msg = input(
                "Enter Commit Message: "
            ).strip()

            # Pass the file content and GitHub destination path
            # to the upload function.
            upload_file_to_github(
                owner,
                repo,
                github_path,
                file_content,
                commit_msg
            )


# Forgot to create a separate project file ... did all the stuffs on my sandbox file ... now importing it all on the project file and making a commit