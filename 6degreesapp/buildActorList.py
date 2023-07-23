import pandas as pd
import requests
import json
import boto3
API_KEY = '97e7f2d04e54e178c11c12a8523d9f05'
s3 = boto3.resource('s3')
def create_bucket(bucket_name):
    if s3.Bucket(bucket_name) not in s3.buckets.all():
        s3.create_bucket(Bucket=bucket_name)

def build_actors():
    create_bucket('entity-list-6degrees')
    df = pd.read_csv('actorfilms.csv')
    unique_actors = df['Actor'].unique()
    unique_ids = {}
    for actor in unique_actors:
        if actor not in unique_ids:
            response = requests.get(f'https://api.themoviedb.org/3/search/person?api_key={API_KEY}&query={actor}')
            data = json.loads(response.text)

            if data['results']:
                id = data['results'][0]['id']
                unique_ids[actor] = id
            else:
                print(f"No results for {actor}")
    try:
        object = s3.Object('entity-list-6degrees','cinemaentities.json')
        object.put(Body=json.dumps(unique_ids).encode('utf-8'))
        print(f"success")
    except Exception as e:
        print(f"failed")
    return


build_actors()