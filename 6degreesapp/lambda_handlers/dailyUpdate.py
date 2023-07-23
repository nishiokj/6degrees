import boto3
import json
# other necessary imports
import random 
from datetime import date
import redis
import requests
from collections import deque

def lambda_handler(event, context):
    category = event['category']
    today = date.today().strftime('%Y%m%d')
    if category == 'NBA':
        nba_easy = select_entities("NBA","easy")
        nba_ent1 = nba_easy[0][0]
        nba_ent2 = nba_easy[1][0]
        shortest = compute_shortest_path(nba_ent1, nba_ent2)
        id = generate_unique_id(nba_ent1, nba_ent2)
        put_puzzle(id,nba_ent1,nba_ent2,shortest,"NBA","easy",today)
        cache_first_degree(nba_ent1,category)
        cache_first_degree(nba_ent2,category)
    elif category == 'Cinema':
        cinema_easy = select_entities("Cinema","easy")
        cin_ent1 = cinema_easy[0][0]
        cin_ent2 = cinema_easy[1][0]
        shortest = compute_shortest_path(cin_ent1, cin_ent2)
        id = generate_unique_id(cin_ent1, cin_ent2)
        put_puzzle(id,cin_ent1,cin_ent2,shortest,"NBA","easy",today)
        cache_first_degree(cin_ent1,category)
        cache_first_degree(cin_ent2,category)
    return 0

    # Assuming you're using DynamoDB for caching
def put_puzzle(id,ent1,ent2,shortestPath,category,difficulty,date):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Puzzles')
    
    table.put_item(
        Item={
            'id':id,
            'Entity1': ent1,
            'Entity2': ent2,
            'ShortestPath': shortestPath,
            'Date': date,
            'Category': category,
            'Difficulty': difficulty
        }
    )
#Have not added functionality for different difficulties
def select_entities(category,difficulty):
    # logic for selecting entities
    # return entity1, entity2
    s3 = boto3.client('s3')
    used_entities = s3.get_object(Bucket='entity_list',key=category+'used.json')
    used_content = used_entities['Body'].read().decode('utf-8')
    response = s3.get_object(Bucket='entity_list', key=category+'entities.json')
    file_content = response['Body'].read().decode('utf-8')
    data = json.loads(file_content)
    keys = list(data.keys())
    past_data = json.loads(used_content)
    while(True):
        random_keys = random.sample(keys,2)
        pair_key = '-'.join(sorted([random_keys[0],random_keys[1]]))
        if pair_key in past_data:
            continue
        else:
            past_data[pair_key]=True
            entity1 = [pair_key[0],data[pair_key[0]]]
            entity2 = [pair_key[1],data[pair_key[1]]]
            break
    s3.put_object(Body=json.dumps(past_data), Bucket='entity_list', key=category+'entities.json')
    ans = []
    ans.append(entity1)
    ans.append(entity2)
    return ans
#Bidirectional Breadth-First_Search
#Using cached first-degree relationship
#Compute the degrees of separation between Entities
def compute_shortest_path(entity1, entity2, category):
    # Create a queue to store the paths
    s3 = boto3.resource('s3')
    
    queue = deque([[entity1]])
    # Keep track of visited nodes
    visited = set([entity1])
    while queue:
        # Get the first path from the queue
        path = queue.popleft()

        # Get the last node from the path
        node = path[-1]

        # Check if we've found the destination
        if node == actor2:
            return path

        # Add neighbors of the node to the queue
        for neighbor in adj_list[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                new_path = list(path)
                new_path.append(neighbor)
                queue.append(new_path)

    return None  # Return None if no path is found

# Assume we have the adjacency list as a dictionary
# adj_list = {...}

# To find the shortest path
# path = shortest_path(actor1_id, actor2_id, adj_list)
# if path is None:
#     print("No path found")
# else:
#     print("Path: ", path)


def get_first_degree(entity,category):
    if category == 'cinema':
        response = requests.get(f"https://api.themoviedb.org/3/person/{entity}/movie_credits?api_key=97e7f2d04e54e178c11c12a8523d9f05")
        data = json.loads(response.txt)
        ids = [movie['id'] for movie in data['cast']]
        return ids
def generate_unique_id(entity1, entity2,date,difficulty):
    # logic for generating unique id
    # return unique_id
    return f'{date}_{difficulty}_{entity1}_{entity2}'

def cache_first_degree(entity,category):
    if category == 'cinema':
        response = requests.get(f"https://api.themoviedb.org/3/person/{entity}/movie_credits?api_key=97e7f2d04e54e178c11c12a8523d9f05")
        data = json.loads(response.txt)
        ids = [movie['id'] for movie in data['cast']]
    elif category == 'NBA':
        response = requests.get(f"https://api.themoviedb.org/3/person/{entity}/movie_credits?api_key=97e7f2d04e54e178c11c12a8523d9f05")
        data = json.loads(response.txt)
        
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('cached_first_degree')

    for id in ids:
        table.put_item(
            Item={
                'entity_id': category + '-'+ entity,
                'first_degree_entities': id
            }
        )
    return 

