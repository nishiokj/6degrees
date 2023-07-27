#Build Adjancency List for top 100 entities based on popularity
#1. Find list of 100 most popular actors and actresses
#2. iterate through each actor, find all the movies they have acted in and add each co-worker. cache the list of actors for each movie
#3. repeat 2 and do not allow duplicates
#4. at the end should be able to map an entity to all of its neighbors
import requests
import json
import boto3
import time
from multiprocessing import Pool
API_KEY = '97e7f2d04e54e178c11c12a8523d9f05'
s3 = boto3.client('s3')
def get_actor_connections(args):
    actor_id, actors = args
    """Fetches all the actors that the given actor has worked with."""
    url = f'https://api.themoviedb.org/3/person/{actor_id}/movie_credits?api_key={API_KEY}'
    response = requests.get(url)
    data = json.loads(response.text)
    
    connections = {}
    if 'cast' in data:
        for movie in data['cast']:
            movie_id = movie['id']
            url = f'https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key={API_KEY}'
            response = requests.get(url)
            movie_data = json.loads(response.text)
            if 'cast' in movie_data:
                for actor in movie_data['cast']:
                    if actor['name'] in actors and actor['id'] != actor_id:
                        if actor['id'] not in connections:
                            connections[int(actor['id'])] = [movie_id]
                        else:
                            connections[int(actor['id'])].append(movie_id)
    return actor_id,connections

def build_adjacency_list(entities):
    """Builds an adjacency list of actors."""
    adjacency_list = {}
    with Pool() as p:
        results = p.map(get_actor_connections,[(entity_id, entities) for name,entity_id in actors.items()])
    for entity_id, connections in results:
        adjacency_list[entity_id] = connections
    return adjacency_list

def get_popular_entities_from_s3(bucket_name, object_name):
    """Retrieve JSON data from an S3 bucket."""
    response = s3.get_object(Bucket=bucket_name, Key=object_name)
    json_data = response['Body'].read().decode('utf-8')

    return json.loads(json_data)

if __name__ == '__main__':
    bucket_name = 'entity-list-6degrees'
    object_name = 'cinema-entities.json'
    actors = get_popular_entities_from_s3(bucket_name, object_name)
    final_list = build_adjacency_list(actors)
    with open('actor_adjacency_list.json', 'w') as f:
        json.dump(final_list, f)
    with open('actor_adjacency_list.json', 'rb') as data:
        s3.upload_fileobj(data, 'entity-list-6degrees', 'actor_adjacency_list.json')