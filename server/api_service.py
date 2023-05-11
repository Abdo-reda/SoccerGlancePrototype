
import requests
import subprocess
import pprint
import json

API_URL = 'http://10.40.41.4:8000/api/'

HEADERS = {
    'Content-type': 'application/json',
}

COOKIE = {'jwt': "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6ImM0NzNkYWQyLWUxZGQtNGQ4YS1iZjJkLWZhY2JmNWM0MGFjYiIsImV4cCI6MTY4NDQ1MDc4NCwiaWF0IjoxNjgzODQ1OTg0fQ.mpFmzcb8MR2nSjZFbfBU83QMfHiYFdgCVF-M0aeRcu0"}

def registerUser():
    data = {
        "email": 'modelServer@auc.com',
        "company_name": 'model',
        "address": 'model',
        "phone_number": '+000000000000',
        "password1": 'modelServer',
        "password2": 'modelServer',
    }
    response = requests.post(API_URL + 'register_user/', headers=HEADERS, json=data)
    print('status_code: ' + response.cookies)
    print(response)


def loginUser():
    data = {
        "email": 'modelServer@auc.com',
        "password": 'modelServer',
    }
    response = requests.post(API_URL + 'login_user/', headers=HEADERS, json=data)
    print(response.status_code)
    return response.cookies.get('jwt')

   
def matchIsLive(matchName, matchDate, cookie): 
    data = {
        "match_name": matchName,
        "match_date": matchDate
    }
    response = requests.post(API_URL + 'start_match/', headers=HEADERS, cookies=cookie, json=data)
    response_data = json.loads(response.text)
    match_id = response_data['match_id']
    print(response.status_code)
    return match_id
    
    
def endMatch(matchID, cookie): 
    data = {
        "match_id": matchID,
    }
    response = requests.post(API_URL + 'end_match/', headers=HEADERS, cookies=cookie, json=data)
    print(response.text)
    
    
    
def sendHighlight(matchID, highlight, action, time, cookie): 
    data = {
        "match_id": matchID,
        "body": highlight,
        "highlight_action": action,
        "match_time": time, #format mm:ss
    }
    response = requests.post(API_URL + 'add_highlight/', headers=HEADERS, cookies=cookie, json=data)
    print(response.text)


def getHighlight(id,cookie):
    response = requests.get(API_URL + f'get_latest_highlight/{id}', headers=HEADERS, cookies=cookie)
    print(response)
    
    
if __name__ == "__main__":
    #registerUser()
    #loginUser()
    matchIsLive('testvstest', '2023-05-12', COOKIE)
    #endMatch('c2e5fb7e81f54bef81bc8fd36e7d7357')
    #sendHighlight('c2e5fb7e81f54bef81bc8fd36e7d7357', 'this is a highlight', 'Goal', '23:14')