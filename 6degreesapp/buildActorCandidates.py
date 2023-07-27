import json
import requests
import boto3

s3 = boto3.resource('s3')
API_KEY = '97e7f2d04e54e178c11c12a8523d9f05'
def func():
    page=1
    unique_actors = {}
    while(page < 8):
        response = requests.get(f'https://api.themoviedb.org/3/person/popular?api_key={API_KEY}&page={page}')
        if response.text:
            try:
                data = json.loads(response.text)
            except json.JSONDecodeError as e:
                print(f"failed decoding json")
        else:
            print(f"empty response")
        
        if 'results' in data:
            for actor in data['results']:
                name = actor['name']
                popularity = actor['popularity']
                id = actor['id']
                unique_actors[name] = id
        else:
            print(f"No results")
        page+=1 
    try:
        object = s3.Object('entity-list-6degrees','candidate-cinema-entities.json')
        object.put(Body=json.dumps(unique_actors).encode('utf-8'))
        print(f"success")
    except Exception as e:
        print(f"failed: {e}")
    return
func()
