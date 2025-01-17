import requests
import os
import shutil
import json


def api_test():
    urls_dict = {

        'repos' : 'https://api.github.com/search/repositories?q='
        }

    query = "dumprun"
    test_response = requests.get(urls_dict["repos"]+query)

    if test_response.status_code == 200:
        response = test_response.json()
        print(response)

    else:
        print(f"Didn't Work, Response code: {test_response.status_code}")

def setup_boilerplate():
    global search

    urls_dict = {
        'repos' : 'https://api.github.com/search/repositories?q='
    }

    def search(query):
        search_response = requests.get(urls_dict["repos"]+query)

        if search_response.status_code == 200:
            return search_response

        else:
            print(f"Search did not work, returned following status code: {search_response.status_code}")
            return search_response.status_code

def basic_repo_search(query, pages=2):
    #This will simply search for all the repos with the query in it and write down the repo properties, like name, description, and link.
    #This can then be used later to search through repos README's and Codes look for terms and count them.
    #CURRENTLY, does not serve this function and is just used for testing, once this line is removed that means it is serving this function.
    
    if os.path.exists("repos_info.json"):
        try:
            os.remove("repos_info.json")
        except:
            print("Removal of previous data did not work, please remove it manually.")
            print("Exiting Program...")
            exit


    for page in range(0, pages-1):

        if isinstance(search(query), int):
            print(f"ERROR: Could not perform search, returned status code:{search(query)}")
            print("Exiting Program...")
            exit
        
        try:
            search_response = search(query).json()
        except AttributeError:
            print("You have likley made too many requests in a short period of time. Wait some time and try again.")
            print("Exiting Prorgram...")
            exit()

        repos_info = []
        items = search_response.get('items', [])

        for item in items:
            repo_info = {
                "title": item['name'],
                "url": item['html_url']
            }   
            repos_info.append(repo_info)
            print("Item appended to repo info json.")
        

    with open("repos_info.json", "w") as json_file:
        json.dump(repos_info, json_file, indent=4)
        print("JSON data has been dumped.")



def main(query):
    setup_boilerplate()
    basic_repo_search(query)

main("dumprun")
