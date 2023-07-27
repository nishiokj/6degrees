import boto3
import json
# other necessary imports
import random 
from datetime import date
from datetime import datetime
import requests
from collections import deque
import traceback 
import openai
import pytz
from botocore.exceptions import BotoCoreError, ClientError
import base64
import os #newchange
s3 = boto3.resource('s3')
def get_image_url(id):
    # Setup S3 client
    s3 = boto3.client('s3')

    # Get id-url map from S3
    id_url_map_obj = s3.get_object(Bucket='entity-list-6degrees', Key='actor_id_url_map.json')
    id_url_map = json.loads(id_url_map_obj['Body'].read().decode('utf-8'))

    # Look up the URL for the given ID
    url = id_url_map.get(id)
    
    # If we found a URL, return it; otherwise, return an error message
    if url:
        return url
    else:
        return url
def create_bucket(bucket_name):
    if s3.Bucket(bucket_name) not in s3.buckets.all():
        s3.create_bucket(Bucket=bucket_name)
        print(f"new bucket {bucket_name} created")
def create_obj(bucket_name,obj_name):
    s3.Object('entity-list-6degrees',obj_name).put(Body='')

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
def delete_s3_object(bucket_name, object_key):
    s3 = boto3.resource('s3')
    s3.Object(bucket_name, object_key).delete()
def select_entities(category,difficulty):
    # logic for selecting entities
    # return entity1, entity2
    s3 = boto3.client('s3')
    create_obj('entity-list-6degrees',category+'-used.json')
    try:
        used_entities = s3.get_object(Bucket='entity-list-6degrees',Key=category+'-'+'used.json')
        used_content = used_entities['Body'].read().decode('utf-8')
    except Exception as e:
        print(f"Error in getting used entities: {str(e)}")
        return None  # Return early on failure
    try:
        if used_content:
            past_data = json.loads(used_content)
        else:
            past_data = {}
    except Exception as e:
        print(f"Error in loading JSON data from used entities content: {str(e)}")
        return None  # Return early on failure
    try:
        response = s3.get_object(Bucket='entity-list-6degrees', Key='candidate'+'-'+category+'-'+'entities.json')
        file_content = response['Body'].read().decode('utf-8')
    except Exception as e:
        print(f"Error in getting entities.json: {str(e)}")
        return None  # Return early on failure
    try:
        data = json.loads(file_content)
    except Exception as e:
        print(f"Error in loading JSON data from entities content: {str(e)}")
        return None  # Return early on failure
    keys = list(data.keys())
    while True:
        try:
            random_keys = random.sample(keys, 2)
        except Exception as e:
            print(f"Error in sampling keys: {str(e)}")
            return None  # Return early on failure
        pair_key = '-'.join(sorted([random_keys[0], random_keys[1]]))
        if not past_data or pair_key not in past_data:
            past_data[pair_key] = True
            try:
                entity1 = [random_keys[0], data[random_keys[0]]]
                entity2 = [random_keys[1], data[random_keys[1]]]
                break
            except Exception as e:
                print(f"Error in getting entity data: {str(e)}")
                return None  # Return early on failure
    try:
        s3.put_object(Body=json.dumps(past_data), Bucket='entity-list-6degrees', Key=category+'-'+'used.json')
    except Exception as e:
        print(f"Loading bucket failed: {str(e)}")

    ans = [entity1, entity2]
    return ans

#Bidirectional Breadth-First_Search
#Using cached first-degree relationship
#Compute the degrees of separation between Entities
def get_adj_list(bucket_name, category):
    try:
        s3 = boto3.client('s3')
        if category == 'cinema':
            adj_list = s3.get_object(Bucket='entity-list-6degrees',Key='actor_adjacency_list.json')
        adj_list_string = adj_list['Body'].read().decode('utf-8')
        adj_list = json.loads(adj_list_string)
        return adj_list
    except Exception:
        print(f"error getting adjacency list")
        traceback.print_exc()
def compute_shortest_path(entity1, entity2, category):
    # Create a queue to store the paths
    adj_list = get_adj_list('entity-list-6degrees',category)
    try:
        entity1 = entity1[1]
        entity2 = entity2[1]
        if entity1 == entity2:
            return [entity1]
        queue_start = deque([entity1])
        queue_end = deque([entity2])
        visited_start = {entity1: (None, None)}
        visited_end = {entity2: (None, None)}
        while queue_start and queue_end:
            path_start = queue_start.popleft()
            path_end = queue_end.popleft()
            for neighbor, edge in adj_list[str(path_start)].items():
                if neighbor not in visited_start:
                    visited_start[neighbor] = (path_start, edge)
                    queue_start.append(neighbor)
                if neighbor in visited_end:
                    path = []
                    curr_node = neighbor
                    while curr_node != entity1:
                        parent_node, connecting_edge = visited_start[curr_node]
                        path.append((curr_node, connecting_edge))
                        curr_node = parent_node
                    path.append((entity1, None))
                    path.reverse()
                    curr_node = neighbor
                    while curr_node != entity2:
                        parent_node, connecting_edge = visited_end[curr_node]
                        path.append((curr_node, connecting_edge))
                        curr_node = parent_node
                    path.append((entity2, None))
                    return path
            for neighbor, edge in adj_list[str(path_end)].items():
                if neighbor not in visited_end:
                    visited_end[neighbor] = (path_end, edge)
                    queue_end.append(neighbor)
                if neighbor in visited_start:
                    path = []
                    curr_node = neighbor
                    while curr_node != entity1:
                        parent_node, connecting_edge = visited_start[curr_node]
                        path.append((curr_node, connecting_edge))
                        curr_node = parent_node
                    path.append((entity1, None))
                    path.reverse()
                    curr_node = neighbor
                    while curr_node != entity2:
                        parent_node, connecting_edge = visited_end[curr_node]
                        path.append((curr_node, connecting_edge))
                        curr_node = parent_node
                    path.append((entity2, None))
                    return path
    except Exception:
        print('error running bfs')
        traceback.print_exc()
        if not queue_start:
            print(f"Exhausted all paths from {entity1}, no connection to {entity2}")
            return None

        if not queue_end:
            print(f"Exhausted all paths from {entity2}, no connection to {entity1}")
            return None

def generate_unique_id(entity1, entity2,date,difficulty):
    # logic for generating unique id
    # return unique_id
    return f'{date}_{difficulty}_{entity1}_{entity2}'
def ai_image(entity_name):
    openai.api_key=os.getenv("OPEN_AI_KEY")
    words = "beautiful natural background image with 3D perspective. " 
    response = openai.Image.create(prompt=words,n=1,size="256x256",
                                   )
    return response['data'][0]['url']
def put_entity_stats(entity1,entity2,category):
    dynamodb= boto3.resource('dynamodb')
    table = dynamodb.Table('Entities')
    rating1 = 0
    rating2 = 0
    
    eastern = pytz.timezone('US/Eastern')
    eastern_time = datetime.now(eastern)
    current_date = eastern_time.date()
    today = current_date.strftime('%Y-%m-%d')
    print(today)
    try:
        openai.api_key=os.getenv("OPEN_AI_KEY")
        response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
                {"role": "system", "content": "You are a movie buff and know a lot of fun facts about actors"},
                {"role": "user", "content": "write a fun fact about "+ entity1[0]+"?"}
            ],
        max_tokens=150
        )
        funFacts1 = response['choices'][0]['message']['content']
        response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
                {"role": "system", "content": "You are a movie buff and know a lot of fun facts about actors"},
                {"role": "user", "content": "write a fun fact about "+ entity2[0]+"?"}
            ],
        max_tokens=150
        )
        funFacts2 = response['choices'][0]['message']['content']
    except Exception:
        traceback.print_exc()
    img1 = get_image_url(str(entity1[1]))
    img2 = get_image_url(str(entity2[1]))
    backdrop1 = ai_image(str(entity1[0]))
    backdrop2 = ai_image(str(entity2[0]))
    if category=='cinema':
        type = "actor"
    table.put_item(
        Item={
            'date': category+'-'+today,
            'entity1' : {
                        'id':entity1[1],
                        'name': entity1[0],
                        'rating': rating1,
                        'funFacts':funFacts1,
                        'img':img1,
                        'type':type,
                        'background':backdrop1},

            'entity2': {'id': entity2[1],
                        'name':entity2[0],
                        'rating':rating2,
                        'funFacts':funFacts2,
                        'img':img2,
                        'type':type,
                        'background':backdrop2}
        }
    )
    return
def get_names_from_actorid(actorid,TMDB_KEY):
    response = requests.get(f"https://api.themoviedb.org/3/person/{int(actorid)}?api_key={TMDB_KEY}")
    data = json.loads(response.text)
    return data['name']
def get_title_from_movieid(movieid,TMDB_KEY):
    if movieid == None:
        return ""
    response = requests.get(f"https://api.themoviedb.org/3/movie/{int(movieid)}?api_key={TMDB_KEY}")
    data = json.loads(response.text)
    if 'title' in data:
        return data['title']
    else:
        return 'blank'
def lambda_handler(event,context):
    try:
        categories = event['categories']
        # the above line defines the categories you will work with. You can add more categories if you wish.
        for category in categories:
            # this is the main loop that will run for each category you have defined.
            today = date.today().strftime('%Y%m%d')
            shortest = None
            while not shortest:
                try:
                    entities = select_entities(category, "easy")
                    ent1 = entities[0]
                    ent2 = entities[1]
                except Exception as e:
                    print(f"error in selecting entities")
                    traceback.print_exc()
                try:
                    shortest = compute_shortest_path(ent1,ent2,category)
                    while(len(shortest) < 3):
                        entities = select_entities(category, "easy")
                        ent1 = entities[0]
                        ent2 = entities[1]
                        shortest = compute_shortest_path(ent1,ent2,category)
                    delete_s3_object('entity-list-6degrees',category+'-used.json')
    
                    print(f"Finding the shortest path between {ent1[0]} and {ent2[0]}...")
                   # print(f"the shortest path between {ent1[0]} and {ent2[0]} is {shortest}")
                    try:
                        print_path(shortest,category)
                    except Exception:
                        traceback.print_exc()
                except Exception as e:
                    print(f"exception: generating new entities")
            try:
                id = generate_unique_id(ent1, ent2, today, "easy")
            except Exception as e:
                print(f"error in generating unique id")
        
      #      put_puzzle(id, ent1, ent2, shortest, category, "easy", today)
            put_entity_stats(ent1,ent2,category)
    except Exception as e:
        traceback.print_exc()
        print(f"error in lambda handler")
    # Assuming you're using DynamoDB for caching
    
def print_path(path,category):
    seen = {}
    i = 0
    TMDB_KEY = os.getenv("TMDB_KEY")
    while True:
        ent1, _ = path[i]
        ent2, edgeids = path[i+1]

        if ent1 in seen:
            break

        seen[ent1] = 1
        if category=='cinema':
            
            ent1_name = get_names_from_actorid(ent1,TMDB_KEY)
            ent2_name = get_names_from_actorid(ent2,TMDB_KEY)

        # skip if ent1 and ent2 are the same
        if ent1 != ent2 and edgeids is not None: 
            if category=='cinema': 
                movie_names = [get_title_from_movieid(edge_id,TMDB_KEY) for edge_id in edgeids]
                print(f"{ent1_name} was in {', '.join(movie_names)} with {ent2_name}")
        i += 1
    j = len(path) - 1
    reverse_statements = []
    while True:
        ent1, _ = path[j]
        ent2, edgeids = path[j-1]

        if ent1 in seen:
            break

        seen[ent1] = 1
        if category=='cinema':
            ent1_name = get_names_from_actorid(ent1,TMDB_KEY)
            ent2_name = get_names_from_actorid(ent2,TMDB_KEY)

        if ent1 != ent2 and edgeids is not None:  
            if category=='cinema':
                movie_names = [get_title_from_movieid(edge_id,TMDB_KEY) for edge_id in edgeids]
                statement = f"{ent2_name} was in {', '.join(movie_names)} with {ent1_name}"
                reverse_statements.append(statement)
        j -= 1

    # Print the statements in reverse order
    for statement in reversed(reverse_statements):
        print(statement)

if __name__ == '__main__':
    event = {}
    event['categories'] = ['cinema']
    lambda_handler(event,None)