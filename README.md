# CodeSync 🚀

**CodeSync** is a Python-based automation tool that syncs local coding solutions to a GitHub repository using the **GitHub REST API**.

Instead of manually copying a solution file into a GitHub repository, CodeSync allows the user to provide the local solution file, problem name, programming language, and commit message. It then determines the appropriate GitHub path and automatically creates or updates the solution file.

---

## 📌 Project Overview

CodeSync was built as a practical project to learn and apply:

- Python
- REST API integration
- HTTP requests
- GitHub Contents API
- Authentication with GitHub Personal Access Token
- JSON data handling
- Base64 encoding and decoding
- File handling
- Environment variables
- Error handling
- Input validation
- Conditional logic
- GitHub file SHA management

The project follows a step-by-step development approach where new functionality is added and tested incrementally.

---

## ✨ Key Features

### 🔐 Secure GitHub Authentication

The GitHub Personal Access Token is stored in a `.env` file instead of being hardcoded into the Python source code.

```env
GITHUB_TOKEN=your_github_token
```

The token is loaded using `python-dotenv`.

---

### 📁 Automatic File & Path Generation

CodeSync generates a GitHub-friendly filename and directory based on the problem name and programming language.

For example:

```text
Problem: Two Sum
Language: Python
```

CodeSync generates:

```text
Filename:
two-sum.py

GitHub Path:
python/two-sum.py
```

Supported languages currently include:

- Python
- C++
- Java
- Golang
- C
- JavaScript

---

### 📤 Create New Solution Files

If the requested solution does not already exist in the repository, CodeSync creates a new file automatically.

Example:

```text
python/two-sum.py
```

---

### 🔄 Update Existing Solution Files

If the solution already exists and the local version has changed, CodeSync updates the existing GitHub file.

GitHub requires the existing file's **SHA** when updating a file, so CodeSync retrieves and uses the current SHA automatically.

---

### 🔍 Duplicate Content Detection

Before updating an existing file, CodeSync compares the local file content with the content currently stored on GitHub.

If both are identical:

```text
No changes detected.
GitHub file is already up to date.
```

No unnecessary update request or commit is created.

---

### 📝 Automatic Git Commit

When a new file is created or an existing file is updated, CodeSync sends the supplied commit message to GitHub.

After a successful operation, CodeSync displays:

```text
File uploaded/updated successfully!
File path: python/two-sum.py
Commit SHA: <commit-sha>
```

---

### 🛡️ Input Validation

CodeSync validates important user inputs before making GitHub API requests.

It checks for:

- Empty GitHub username
- Empty repository name
- Empty problem name
- Empty programming language
- Unsupported programming language
- Empty solution file path
- Missing solution file
- Empty solution file
- Empty commit message

---

### ⚠️ Error Handling

The project handles different categories of errors, including:

- HTTP errors
- Authentication and permission problems
- Network/request errors
- File not found errors
- Permission errors
- File system errors
- Invalid or unexpected API responses
- Missing response data

The goal is to provide useful error messages instead of allowing the program to fail unexpectedly.

---

# 🏗️ Project Architecture

CodeSync currently follows a simple modular workflow:

```text
User Input
    ↓
Input Validation
    ↓
Problem + Language Processing
    ↓
GitHub Filename & Path Generation
    ↓
Local Solution File Reading
    ↓
Base64 Encoding
    ↓
GitHub API Request
    ↓
Check Existing File
    ↓
┌─────────────────────────────┐
│ Does the file exist?        │
└─────────────────────────────┘
        ↓             ↓
       YES            NO
        ↓             ↓
Compare Content     Create File
        ↓
   ┌────┴────┐
   ↓         ↓
 Same      Different
   ↓         ↓
 Skip      Update
```

---

# 🔧 Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Requests | HTTP/API communication |
| GitHub REST API | Repository file management |
| python-dotenv | Loading environment variables |
| Base64 | Encoding/decoding file content |
| GitHub Contents API | Creating and updating repository files |

---

# 📂 Project Structure

A simplified project structure looks like:

```text
CodeSync/
│
├── CodeSync_Part-1.py
├── CodeSync_Part-2.py
├── CodeSync_Part-3.py
├── CodeSync_Part-4.py
├── CodeSync_Part-5.py
├── CodeSync_Part-6.py
│
├── .env
├── .gitignore
└── README.md
```

> The `.env` file should never be committed to GitHub.

---

# ⚙️ Installation & Setup

## 1. Clone the Repository

```bash
git clone <your-repository-url>
```

Move into the project directory:

```bash
cd CodeSync
```

---

## 2. Install Required Packages

CodeSync requires `requests` and `python-dotenv`.

Install them with:

```bash
pip install requests python-dotenv
```

---

## 3. Create a GitHub Personal Access Token

Create a GitHub Personal Access Token with the required repository permissions.

The token is required because CodeSync needs permission to read, create, and update files in the target repository.

**Never hardcode the token inside the Python source code.**

---

## 4. Create a `.env` File

Create a file named:

```text
.env
```

Add:

```env
GITHUB_TOKEN=your_github_token
```

Replace `your_github_token` with your actual token.

---

## 5. Protect the `.env` File

Add `.env` to `.gitignore`:

```gitignore
.env
```

This prevents the GitHub token from being accidentally committed to the repository.

---

# ▶️ How to Run

Run the latest version:

```bash
python CodeSync_Part-6.py
```

CodeSync will ask for information such as:

```text
=== CodeSync Part 6 ===

Enter GitHub Username:
Enter Repository Name:
Enter LeetCode Problem Name:
Enter Programming Language:
Enter Solution File Path:
Enter Commit Message:
```

Example:

```text
Enter GitHub Username: fahmidur-rahman-arnob
Enter Repository Name: Leetcode_Solutions
Enter LeetCode Problem Name: Two Sum
Enter Programming Language: Python
Enter Solution File Path: F:\LeetCode\Two_Sum.py
Enter Commit Message: Add Two Sum solution
```

CodeSync will then determine the destination automatically:

```text
python/two-sum.py
```

---

# 🔄 Example Workflows

## Case 1 — New File

If:

```text
python/two-sum.py
```

does not exist on GitHub:

```text
File does not exist yet.
A new file will be created.

Uploading file to GitHub...

File uploaded/updated successfully!
```

---

## Case 2 — Existing File With Changes

If the file already exists but the local solution has changed:

```text
Existing file found.
It will be updated.

Uploading file to GitHub...

File uploaded/updated successfully!
```

The modified local content will then appear in the GitHub repository.

---

## Case 3 — No Changes

If the local solution is already identical to the GitHub version:

```text
No changes detected.
GitHub file is already up to date.
```

No unnecessary update is performed.

---

# 🔐 Security

CodeSync uses an environment variable to keep the GitHub token outside the source code.

### Do:

```env
GITHUB_TOKEN=your_token
```

### Don't:

```python
token = "ghp_your_real_token_here"
```

Never commit:

```text
.env
```

to GitHub.

If a GitHub token is accidentally exposed, revoke it immediately and generate a new token.

---

# 🧠 What I Learned From This Project

CodeSync was developed as a hands-on Python and API integration project.

Through the project, I practiced:

### Python

- Functions
- Dictionaries
- Conditional statements
- String manipulation
- File handling
- Exception handling
- Environment variables
- Modular programming

### APIs

- HTTP GET requests
- HTTP PUT requests
- API endpoints
- Request headers
- JSON payloads
- HTTP status codes
- API response handling

### GitHub API

- GitHub REST API
- Contents API
- Repository file management
- File SHA
- Creating files through API
- Updating files through API
- Commit creation

### Data Processing

- JSON → Python dictionaries
- Base64 encoding
- Base64 decoding
- Content comparison

### Software Development

- Input validation
- Error handling
- Debugging
- Incremental development
- Testing different scenarios
- Preventing unnecessary API requests

---

# 🧪 Testing

The current implementation has been tested for the following scenarios:

- [x] New GitHub file creation
- [x] Existing file detection
- [x] Existing file update
- [x] Duplicate content detection
- [x] Local file reading
- [x] Unsupported language handling
- [x] Empty input validation
- [x] Empty solution file validation
- [x] Empty commit message validation
- [x] Missing GitHub token handling
- [x] HTTP/API error handling
- [x] Network/request error handling

---

# 🚀 Future Improvements

Possible future improvements include:

- Automatic detection of the local solution language
- Interactive repository selection
- Better CLI interface
- More advanced GitHub repository validation
- Automated test suite
- Configuration file support
- Logging system
- Additional programming languages
- Improved project structure
- Optional command-line arguments
- Packaging CodeSync as a reusable CLI tool

These features are not part of the current implementation and may be added in future versions.

---

# 📌 Current Status

**CodeSync V1 — Active Development**

Current development has reached **Part 6**.

The core GitHub synchronization workflow is already functional:

```text
Local Solution
      ↓
CodeSync
      ↓
GitHub REST API
      ↓
Create / Update / Skip
      ↓
GitHub Repository
```

---

# 👨‍💻 Author

**Fahmidur Rahman Arnob**

Software Engineering Student  
Python Backend Development Learner

---

## ⭐ Project Goal

The main goal of CodeSync is to build a practical understanding of **Python backend development, REST API integration, authentication, file processing, and GitHub automation** through a real-world project rather than isolated coding exercises.