'''GOAL/Targetted topics to learn of part-5 is -
1. Duplicate file বলতে কী বোঝায়
2. GitHub API দিয়ে existing file check করা
3. SHA কেন দরকার
4. Create বনাম Update request-এর difference
5. একই solution আবার upload করলে কীভাবে handle করব
6. 200, 404 response-এর practical meaning
7. Existing file থাকলে overwrite/update করার logic
8. পরে main CodeSync-এ এই logic cleanভাবে integrate করা
আর একটা গুরুত্বপূর্ণ ব্যাপার:
Part 4-এ আমরা SHA handling-এর basic implementation already করেছি। তাই Part 5-এ সেটা শুধু আবার লিখব না। বরং আমরা এটাকে আলাদা concept হিসেবে গভীরভাবে বুঝব এবং cleaner/robust logic বানাব, যাতে পরে main project-এ properly integrate করতে পারি।


১. SHA মানে কী? (What is SHA?)

SHA-এর পূর্ণরূপ হলো Secure Hash Algorithm (সিকিউর হ্যাশ অ্যালগরিদম)। এটি একটি গাণিতিক ক্রিপ্টোগ্রাফিক ফাংশন।
সহজ কথায়, এটি একটি ডিজিটাল ফিঙ্গারপ্রিন্ট বা ডিজিটাল হাতের ছাপের মতো। আপনি এই ফাংশনে যেকোনো সাইজের ডেটা বা ফাইল (সেটা একটা ছোট শব্দ হতে পারে, আবার ৪ জিবি-র কোনো সিনেমাও হতে পারে) ইনপুট দিলে, এটি আউটপুট হিসেবে একটি নির্দিষ্ট দৈর্ঘ্যের ইউনিক (অনন্য) কোড তৈরি করে দেয়। এই কোডটিকে বলা হয় "Hash" বা "Checksum"।
যেমন, SHA-1 অ্যালগরিদম ব্যবহার করলে যেকোনো ফাইলের জন্য একটি ৪০ অক্ষরের কোড (যেমন: 2fd4e1c67a2d28fced849ee1bb76e7391b93eb12) তৈরি হয়।



২. SHA কেন দরকার হয়? (Why do we need SHA?)

গিটহাব (GitHub) বা যেকোনো ভার্সন কন্ট্রোল সিস্টেমে SHA মূলত দুটি কারণে অত্যন্ত জরুরি:
• ফাইলের সততা ও পরিবর্তন যাচাই (Data Integrity): আপনি যদি একটি ফাইলের ভেতর মাত্র একটি ডট (.) বা স্পেসও পরিবর্তন করেন, তবে ফাইলটির SHA কোড সম্পূর্ণ বদলে যাবে। এর মাধ্যমে গিটহাব বুঝতে পারে যে ফাইলটি পরিবর্তন করা হয়েছে নাকি আগের মতোই আছে।
• ইউনিক আইডি হিসেবে (Unique Identification): গিটহাবে হাজার হাজার ফাইল এবং কমিট (Commit) থাকে। কোন ফাইলটির কোন ভার্সন পরিবর্তন হচ্ছে, তা ট্র্যাক করার জন্য প্রত্যেকটির একটি ইউনিক আইডি বা নাম দরকার। SHA সেই ইউনিক আইডির কাজ করে।


৩. SHA কীভাবে খুঁজে বের করবেন? (How to find/figure out SHA?)

আপনি যে প্রজেক্টের কথা বলছেন (GitHub Contents API), সেখানে ফাইল আপডেট করতে হলে গিটহাবকে বলতে হয়, "আমি অমুক SHA আইডির ফাইলটি আপডেট করতে চাই।" এটি যেভাবে খুঁজে পাবেন:
• এপিআই (API) এর মাধ্যমে (Automated): গিটহাবের Contents API-তে একটি GET রিকোয়েস্ট পাঠালে গিটহাব ওই ফাইলের বিস্তারিত তথ্য (JSON ফরম্যাটে) পাঠায়। সেখানে "sha": "..." নামে একটি ফিল্ড থাকে। কোডিংয়ের মাধ্যমে স্বয়ংক্রিয়ভাবে সেখান থেকে SHA সংগ্রহ করা হয়।
• গিটহাব ওয়েবসাইট থেকে (Manually): গিটহাবে আপনার রিপোজিটরিতে গিয়ে যেকোনো ফাইলের উপর ক্লিক করুন। এরপর ফাইলের Blame বা History অপশনে গেলে ওই ফাইলের সর্বশেষ পরিবর্তনের SHA কোডটি (সাধারণত প্রথম ৭-৮ অক্ষর) দেখতে পাবেন।
• কমান্ড লাইনে (Local Git): আপনার কম্পিউটারের টার্মিনালে git log অথবা git ls-tree HEAD <filename> কমান্ড লিখলে ফাইলের SHA কোডটি স্ক্রিনে চলে আসবে।


৪. বাস্তব জীবনে (Real-World) SHA এর ব্যবহার কোথায় হয়?

গিটহাব ছাড়াও আমাদের দৈনন্দিন প্রযুক্তিতে SHA-এর প্রচুর ব্যবহার রয়েছে:
• পাসওয়ার্ড সুরক্ষা (Password Hashing): ফেসবুক বা গুগলের মতো বড় কোম্পানিগুলো আপনার আসল পাসওয়ার্ড (যেমন: MyPassword123) তাদের সার্ভারে সংরক্ষণ করে না। তারা পাসওয়ার্ডের SHA হ্যাশ ভ্যালু সংরক্ষণ করে। ফলে হ্যাকাররা সার্ভার হ্যাক করলেও আপনার আসল পাসওয়ার্ড জানতে পারে না।
• সফটওয়্যার ডাউনলোড যাচাই (File Verification): বড় কোনো সফটওয়্যার (যেমন: Linux OS বা Windows ISO) ডাউনলোড করার সময় ওয়েবসাইটে একটি SHA-256 কোড দেওয়া থাকে। ডাউনলোড শেষে আপনার কম্পিউটারের ফাইলের SHA কোডের সাথে ওয়েবসাইটের কোডটি মিলিয়ে দেখতে পারেন। দুটি মিলে গেলে নিশ্চিত হওয়া যায় যে ডাউনলোডের সময় ফাইলটি নষ্ট বা হ্যাক হয়নি।
• ব্লকচেইন ও ক্রিপ্টোকারেন্সি (Blockchain & Bitcoin): বিটকয়েন বা অন্যান্য ক্রিপ্টোকারেন্সির মূল ভিত্তি হলো SHA-256। প্রতিটা লেনদেনের ডেটা সিকিউর রাখতে এবং চেইন আকারে জুড়ে দিতে এই SHA ব্যবহার করা হয়।
• ডিজিটাল সিগনেচার (Digital Signatures): বিভিন্ন সরকারি বা প্রাতিষ্ঠানিক ডিজিটাল ডকুমেন্টে স্বাক্ষর বা সত্যতা যাচাইয়ের জন্য SHA ব্যবহার করা হয়।

got to clear this SHA concept a little more..having trouble and getting a lot of bugs...

'''


import os
import base64
import requests

from dotenv import load_dotenv
from requests.exceptions import RequestException


# ---------------------------------------------------------
# PART 5 — DUPLICATE DETECTION + SHA EXTRACTION + UPDATE (Modified using AI and comments are from AI as well ... gave it a prompt to explain this to me so that I get a clear idea in future whenever I try to open )
# ---------------------------------------------------------
#
# COMPLETE FLOW:
#
# .env থেকে token load
#          ↓
# GET request দিয়ে file check
#          ↓
#     ┌────┴─────┐
#     ↓          ↓
#   200 OK      404
#     ↓          ↓
# File exists   File missing
#     ↓          ↓
# Extract SHA   No update request
#     ↓
# Prepare new content
#     ↓
# Base64 encode
#     ↓
# PUT request with SHA
#     ↓
# ┌───┴──────────┐
# ↓              ↓
# Success        Failure
# ↓              ↓
# Print commit   Print error
# SHA            details
# ---------------------------------------------------------


# ---------------------------------------------------------
# STEP 0 — Load GitHub token from .env
#
# At First in the PowerShell I had to set the GITHUB_TOKEN manually
# NOW Iam using python-dotenv to collect token load from local .env file
# Not Hard coding the token into the source file
# .env file MUST stay in .gitignore


load_dotenv()

#collectinng token using python-dotenv 
token = os.getenv("GITHUB_TOKEN")


# if the token is not available then dont need to send API req
if not token:
    print("Error: GITHUB_TOKEN was not found.")
    print("Check your .env file and GITHUB_TOKEN variable.")


else: # if the token is available 

    # GitHub API URL
    # Format:
    # https://api.github.com/repos/OWNER/REPO/contents/PATH
    
    url = (
        "https://api.github.com/repos/"
        "fahmidur-rahman-arnob/"
        "Leetcode_Solutions/"
        "contents/python/two-sum.py"
    )


    # -----------------------------------------------------
    # Headers
    # -----------------------------------------------------
    #
    # Authorization: is for sending authenticated request to github
    # Accept: is for letting github API response know the expected media type 
    #
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json"
    }

    # STEP 1 — Existing file detection using GET
    # asking github is the file existing or not
    # timeout=20:
    # Network response waiting time maximum 20 seconds
    #
    try:

        response = requests.get(
            url,
            headers=headers,
            timeout=20
        )


        # CASE 1 — File already exists (HTTP 200)

        if response.status_code == 200:

            print("File already exists in the GitHub repository.")

            # GitHubs JSON file information।
            file_data = response.json()

            # Existing files blob SHA, this SHA has to be passed to update request of payload...github will use this SHA to check the existing file version
            #
            file_sha = file_data["sha"]

            print("Existing File SHA:", file_sha)

            # STEP 2 — Prepare new file content
            #
            # this is a test content for sandbox
            # if I upload this content then the existing content will change 
            #
            new_content = """print("Hello from CodeSync Part 5")
print("This file was updated using GitHub API.")
"""


            # ---------------------------------------------
            # STEP 3 — Encode content using Base64
            # first from string to UTF-8 bytes
            # then from bytes to Base64 encode
            # and lastly from encoded bytes to string conversion
            #
            # GitHub Contents API  content field accepts base64 encoded file content
            encoded_content = base64.b64encode(
                new_content.encode("utf-8")
            ).decode("utf-8")


            # STEP 4 — Prepare update payload
            #
            # message:
            # GitHub-এ prepared ccommit message
            #
            # content:
            # new file content, Base64-encoded
            #
            # sha:
            # first GET requests existing file SHA।
            #
            # IMPORTANT:
            # Existing file update this SHA needs to be passed
            #
            payload = {
                "message": "Update file using CodeSync Part 5",
                "content": encoded_content,
                "sha": file_sha
            }


            # ---------------------------------------------
            # OPTIONAL TEST — Force an update failure
            #
            # Scenario 2 test
            # temporary uncomment 
            # instead of sending actual SHA an invalid SHA will be sent to check github update rejects or not to see error handling
            #
            # payload["sha"] = "deliberately-invalid-sha"

            # STEP 5 — Send PUT request
            # using put req. in github content api one can get existing file or create a new file
            # এই file-এর ক্ষেত্রে GET-এ 200 পাওয়া গেছে এবং in case of this file in get req 200 has been found , payload contains the SHA that's why I am updating it
            #
            try:

                update_response = requests.put(
                    url,
                    headers=headers,
                    json=payload,
                    timeout=20
                )


                if update_response.status_code in (200, 201):

                    print("File updated successfully!")

                    update_data = update_response.json()

                    # commit.sha হলো নতুন commit-এর SHA।
                    # এটি file_sha-এর সঙ্গে এক জিনিস নয়।
                    #
                    print(
                        "New Commit SHA:",
                        update_data["commit"]["sha"]
                    )

                else:

                    print("File update failed.")

                    print(
                        "Status Code:",
                        update_response.status_code
                    )

                    print(
                        "Response:",
                        update_response.text
                    )


            except RequestException as error:

                # Network error,
                # if any  problem comes then it'll come here. 
                print("Network error during file update.")
                print("Error:", error)


        # -------------------------------------------------
        # CASE 3 — File does not exist (HTTP 404)
        #
        # GitHub-এ expected file not found
        #
        # this sandbox's goal is duplicate detection & existing file update 
        #
        # so that's why we're not sending PUT request 
        #
        elif response.status_code == 404:

            print("File does not exist in the GitHub repository.")
            print("No update request was sent.")

        else:

            print("Could not check the existing file.")

            print("Status Code:", response.status_code)
            print("Response:", response.text)


    except RequestException as error:
        print("Network error during file detection.")
        print("Error:", error)
