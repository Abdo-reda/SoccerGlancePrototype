
import requests
import subprocess
import pprint
import json

API_URL = 'http://10.40.37.4:8000/api/'

HEADERS = {
    'Content-type': 'application/json',
}

COOKIE = {'jwt': "b'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6IjA1MWNjNDc4LWUxNmItNGEyYy04OTU2LWFkYmMyMTQyODI0NCIsImV4cCI6MTY4MzQ1MjEwMiwiaWF0IjoxNjgyODQ3MzAyfQ.GWICvfzLenmC9WjjdCj5yNB4rxawVr4hW8hfUIN4mFE'"}

def registerUser():
    data = {
        "email": 'apiUser@good.com',
        "company_name": 'api',
        "address": 'apiA',
        "phone_number": '+000000000000',
        "password1": 'api',
        "password2": 'api',
    }
    response = requests.post(API_URL + 'register_user/', headers=HEADERS, json=data)
    print(response.cookies)


def loginUser():
    data = {
        "email": 'apiUser@good.com',
        "password": 'api',
    }
    response = requests.post(API_URL + 'login_user/', headers=HEADERS, json=data)
    print(response.cookies)

   
def matchIsLive(matchName, matchDate): 
    data = {
        "match_name": matchName,
        "match_date": matchDate
    }
    response = requests.post(API_URL + 'start_match/', headers=HEADERS, cookies=COOKIE, json=data)
    response_data = json.loads(response.text)
    match_id = response_data['match_id']
    print(match_id)
    return match_id
    
    
def endMatch(matchID): 
    data = {
        "match_id": matchID,
    }
    response = requests.post(API_URL + 'end_match/', headers=HEADERS, cookies=COOKIE, json=data)
    print(response.text)
    
    
    
def sendHighlight(matchID, highlight, action, time): 
    data = {
        "match_id": matchID,
        "body": highlight,
        "highlight_action": action,
        "match_time": time, #format mm:ss
    }
    response = requests.post(API_URL + 'add_highlight/', headers=HEADERS, cookies=COOKIE, json=data)
    print(response.text)


def getHighlight():
    response = requests.get(API_URL + 'get_latest_highlight/1', headers=HEADERS, cookies=COOKIE)
    print(response)
    
    
if __name__ == "__main__":
    #loginUser()
    #matchIsLive('testvstest', '2024-02-01')
    #endMatch('c2e5fb7e81f54bef81bc8fd36e7d7357')
    sendHighlight('c2e5fb7e81f54bef81bc8fd36e7d7357', 'this is a highlight', 'Goal', '23:14')