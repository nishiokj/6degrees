#Build Adjancency List for top 100 entities based on popularity
#1. Find list of 100 most popular actors and actresses
#2. iterate through each actor, find all the movies they have acted in and add each co-worker. cache the list of actors for each movie
#3. repeat 2 and do not allow duplicates
#4. at the end should be able to map an entity to all of its neighbors
import requests
import json
import boto3
import time
API_KEY = '97e7f2d04e54e178c11c12a8523d9f05'
s3 = boto3.client('s3')
def get_actor_connections(actor_id):
    """Fetches all the actors that the given actor has worked with."""
    url = f'https://api.themoviedb.org/3/person/{actor_id}/movie_credits?api_key={API_KEY}'
    response = requests.get(url)
    data = json.loads(response.text)
    
    connections = set()
    if 'cast' in data:
        for movie in data['cast']:
            movie_id = movie['id']
            url = f'https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key={API_KEY}'
            response = requests.get(url)
            movie_data = json.loads(response.text)

            if 'cast' in movie_data:
                for actor in movie_data['cast']:
                    connections.add(actor['id'])

    return list(connections)

def build_adjacency_list(actors):
    """Builds an adjacency list of actors."""
    adjacency_list = {}
    for actor,info in actors.items():
        actor_id = info[1]
        adjacency_list[actor_id] = get_actor_connections(actor_id)
        time.sleep(.1)
    return adjacency_list

def get_popular_actors_from_s3(bucket_name, object_name):
    """Retrieve JSON data from an S3 bucket."""
    response = s3.get_object(Bucket=bucket_name, Key=object_name)
    json_data = response['Body'].read().decode('utf-8')

    return json.loads(json_data)

bucket_name = 'entity-list-6degrees'
object_name = 'popularActors.json'
actors = get_popular_actors_from_s3(bucket_name, object_name)
final_list = build_adjacency_list(actors)
with open('actor_adjacency_list.json', 'w') as f:
    json.dump(final_list, f)
with open('actor_adjacency_list.json', 'rb') as data:
    s3.upload_fileobj(data, 'entity-list-6degrees', 'actor_adjacency_list.json')