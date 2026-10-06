
# GOAL:
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
# In Sandbox 03, I independently researched and practiced
# the concepts required for this functionality before applying
# them to the main CodeSync project.
#
# Concepts researched and practiced:
# - String normalization
# - lower()
# - split()
# - join()
# - Dictionary-based language mapping
# - Nested dictionaries
# - Dictionary .get()
# - Input validation
# - File extension mapping
# - Filename generation
# - GitHub path construction
# - Returning multiple values from a function
#
# ============================================================
#
# ============================================================
# MAIN IMPLEMENTATION
# ============================================================
#
# The concepts researched and tested in Sandbox 03 are now
# applied to the actual CodeSync project.
#
# The implementation accepts a LeetCode problem name and
# programming language from the user.
#
# The problem name is normalized into a GitHub-friendly
# filename format by:
#
#     - converting the name to lowercase
#     - removing unnecessary whitespace
#     - replacing spaces with hyphens
#
# The selected programming language is then used to determine:
#
#     - the appropriate file extension
#     - the appropriate GitHub directory
#
# Finally, the implementation generates:
#
#     - the solution filename
#     - the complete GitHub repository path
#
# Unsupported languages are validated before generating the
# file information.
#
# Unlike the sandbox version, this implementation returns
# the prepared file information instead of directly printing
# it inside the function.
#
# This makes the function reusable by future CodeSync
# components, particularly the GitHub upload functionality
# that will be implemented in Part 4.
#
# Example:
#
#     Input:
#         Problem: Two Sum
#         Language: Python
#
#     Output:
#         Filename: two-sum.py
#         GitHub Path: python/two-sum.py
#
# ============================================================

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


    normalized_name = "-".join(problem_name.lower().split())

    language_data = language_info.get(language.lower())

    if language_data is None: # "At my previous version I used Not Supported but it returns None it is more pythonic way and more clean"
        # print(f"Error: {language} is not a supported language!")
        return None

    extension = language_data["extension"]
    directory = language_data["directory"]

    filename = f"{normalized_name}{extension}"

    github_path = f"{directory}/{filename}"

    return filename, github_path


# Take Input From USER 

name = input("Enter the problem name: ")
lang = input("Enter the language name: ")

file_info = get_file_info(name, lang)

if file_info is None : 
    print(f"Error: {lang} is not a supported language.")
else : 
    filename, github_path = file_info
    print(f"Filename: {filename}")
    print(f"Github Path: {github_path}")