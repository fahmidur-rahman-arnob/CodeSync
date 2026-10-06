# ============================================================
# CODESYNC — PART 3: SOLUTION FILE PREPARATION
# ============================================================
#
# Goal:
# The purpose of Part 3 is to prepare a LeetCode solution
# for the structured GitHub repository used by CodeSync.
#
# Before a solution can be uploaded to GitHub, CodeSync needs
# to determine:
#
# - A normalized filename from the problem name
# - The correct file extension for the programming language
# - The correct GitHub directory for that language
# - The final GitHub path of the solution file
#
# Example:
#
#     Problem: Two Sum
#     Language: Python
#
#     Filename:
#         two-sum.py
#
#     GitHub Path:
#         python/two-sum.py
#
# Before implementing this functionality in the main project,
# I created a separate sandbox to research and practice:
#
# - String normalization
# - String lower() and split()
# - join() for creating slugs
# - Dictionary-based language mapping
# - Nested dictionaries
# - Dictionary .get() method
# - Input validation
# - File extension generation
# - GitHub path construction
#
# After understanding and testing these concepts in the
# sandbox, they will be applied to the actual CodeSync
# project in Part 3.
#
# ============================================================


# ============================================================
# SANDBOX 03 — SOLUTION FILE PREPARATION
# ============================================================
#
# This sandbox was created before implementing the main
# CodeSync Part 3 functionality.
#
# The purpose of this sandbox is to independently practice
# converting LeetCode problem information into a GitHub-ready
# filename and path.
#
# The sandbox takes:
#
#     Problem Name
#     Language
#
# and produces:
#
#     Filename
#     GitHub Path
#
# Example:
#
#     Two Sum + Python
#         ↓
#     two-sum.py
#         ↓
#     python/two-sum.py
#
# A nested dictionary is used to store multiple pieces of
# information for each programming language:
#
#     extension
#     directory
#
# Unsupported languages are also handled before generating
# the file information.


def get_file_info(problem_name, language):
    # Programming language → extension + GitHub directory
    # A nested dictionary is used because each language needs
    # more than one piece of information.
    #
    # Example:
    #     Python
    #         → extension: .py
    #         → directory: python

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

    # Problem name normalization
    # the lower() method(studied from GFG) converts the problem name to lowercase.
    #
    # the split() method(studied from GFG) separates the words and also handles multiple
    # spaces between words.
    #
    # the join() method(studied from GFG) then combines the words using "-".
    # Example:
    #
    #     "Valid Parentheses"
    #             ↓
    #     ["valid", "parentheses"]
    #             ↓
    #     "valid-parentheses"

    normalized_name = "-".join(problem_name.lower().split())

    # Language validation
    # the .get() method(studied from w3school) of dict. searches for the language in the dictionary.

    # language.lower() (studied from w3school) makes the language input case-insensitive.
    # Example:
    #     Python
    #     PYTHON
    #     python
    # all refer to the same dictionary key.
    

    language_data = language_info.get(language.lower())

    if language_data is None: # "At my previous version I used Not Supported but it returns None it is more pythonic way and more clean"
        print(f"Error: {language} is not a supported language!")
        return
    
    # Extracting the language-specific information from dict.

    extension = language_data["extension"]
    directory = language_data["directory"]

    # Generating the filename

    filename = f"{normalized_name}{extension}"

    # Generating the GitHub path

    github_path = f"{directory}/{filename}"

    # Display the prepared file information

    print(f"Filename: {filename}")
    print(f"Github Path: {github_path}")


# Take Input From USER 

name = input("Enter the problem name: ")
lang = input("Enter the language name: ")

get_file_info(name, lang)