# -*- coding: utf-8 -*-
"""
Created on Mon Aug 21 10:50:33 2023

@author: Bachs
"""

"""
Still needs some work to implement fully with the rest of the programs. 
"""

#For handling Bible API requests.
import requests

translations = {"es":"592420522e16049f-01",
                "eng":"65eec8e0b60e656b-01",
                "Mandrain":"04fb2bec0d582d1f-01",
                "Ancient_Hebrew":"0b262f1ed7f084a6-01",
                "Modern_Hebrew":"a8a97eebae3c98e4-01",
                "German":"f492a38d0e52db0f-01"}

#This is likely the only url we'll be requesting, so this method works pretty well I think. 
def form_passage_request_url(version, passage):
    return "https://api.scripture.api.bible/v1/bibles/" + str(version) + "/passages/" + str(passage)
    

def extract_text(data):
    text_list = []

    if isinstance(data, list):
        for item in data:
            text_list.extend(extract_text(item))
    elif isinstance(data, dict):
        if "type" in data and data["type"] == "text":
            if "text" in data:
                text_list.append(data["text"])
        else:
            for key, value in data.items():
                text_list.extend(extract_text(value))

    return text_list

url = form_passage_request_url("a8a97eebae3c98e4-01", "ROM.1.1-ROM.1.31")
print("url: " + url)
#url = "https://api.scripture.api.bible/v1/bibles/a8a97eebae3c98e4-01/passages/ROM.1.1-ROM.1.31"
#
"""
Still need to ask for access to:
    Kenyarwanda
    French

"""

headers = {
    "accept": "application/json",
    "api-key": "7bb973606e0feaf604d01ee796c198a4"
}

params = {
    "content-type": "json",
    "include-notes": "false",
    "include-titles": "true",
    "include-chapter-numbers": "false",
    "include-verse-numbers": "true",
    "include-verse-spans": "false",
    "use-org-id": "false"
}

response = requests.get(url, headers=headers, params=params)

if response.status_code == 200:
    # Print the JSON response
    x=1
    data = response.json().get("data").get("content") 

    text_content = extract_text(data)

    for text in text_content:
        print(text)
else:
    print(f"Request failed with status code: {response.status_code}")
    print(response.text)
