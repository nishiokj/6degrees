import boto3
import json
import requests
import pandas as pd
import time
def build_athletes():
    df = pd.read_csv('nbaallstars.csv')
    unique_athletes = df['Name']
    unique_athletes = unique_athletes.unique()
    unique_ids = {}
    for player in unique_athletes:
        if player not in unique_ids:
            response = requests.get(f'https://www.balldontlie.io/api/v1/players?search={player}')  
            time.sleep(.8) 
            if response.text:
                try:
                    data = json.loads(response.text)
                except json.JSONDecodeError as e:
                    print(f"failed decoding json")
            else:
                print(f"empty response")
            if data['data']:
                id = data['data'][0]['id']
                unique_ids[player] = id 
            else:
                print(f"{player} not found")

    try:
        s3 = boto3.resource('s3')
        object = s3.Object('entity-list-6degrees','athletesentities.json')
        object.put(Body=json.dumps(unique_ids).encode('utf-8'))
        print(f"success")
    except Exception as e:
        print(f"failed")
    return
build_athletes()