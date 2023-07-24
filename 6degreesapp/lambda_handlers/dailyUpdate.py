import boto3
import json
# other necessary imports
import random 
from datetime import date
import redis
import requests
from collections import deque
import traceback
s3 = boto3.resource('s3')
def create_bucket(bucket_name):
    if s3.Bucket(bucket_name) not in s3.buckets.all():
        s3.create_bucket(Bucket=bucket_name)
        print(f"new bucket {bucket_name} created")
def create_obj(bucket_name,obj_name):
    s3.Object('entity-list-6degrees',obj_name).put(Body='')
    print(f"new obj {obj_name} created")

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
def compute_shortest_path(entity1, entity2, category):
    # Create a queue to store the paths
    try:
        s3 = boto3.client('s3')
        adj_list = s3.get_object(Bucket='entity-list-6degrees',Key='actor_adjacency_list.json')
        adj_list_string = adj_list['Body'].read().decode('utf-8')
        adj_list = json.loads(adj_list_string)
    except Exception:
        print(f"error getting adjacency list")
        traceback.print_exc()
    try:
        entity1 = entity1[1]
        entity2 = entity2[1]
        if entity1 == entity2:
            return [entity1]
        queue_start = deque([[(str(entity1),[])]])
        queue_end = deque([[(str(entity2),[])]])
        visited_start = {entity1}
        visited_end = {entity2}
    except Exception:
        print(f"error initializing bfs")
        traceback.print_exc()
    try:
        while queue_start and queue_end:
            path_start = queue_start.popleft()
            path_end = queue_end.popleft()

            node_start = path_start[-1][0]
            node_end = path_end[0][0]

            for neighbor, movie in adj_list[str(node_start)].items():
                if neighbor not in visited_start:
                    visited_start.add(neighbor)
                    new_path = path_start + [(neighbor, movie)]
                    if neighbor in visited_end:
                        intersection_path = path_end
                        while intersection_path[0][0] != neighbor:
                            intersection_path = intersection_path[1:]
                        return new_path + intersection_path[1:]
                    queue_start.append(new_path)

            for neighbor, movie in adj_list[str(node_end)].items():
                if neighbor not in visited_end:
                    visited_end.add(neighbor)
                    new_path = [(neighbor, None)] + path_end
                    if neighbor in visited_start:
                        intersection_path = path_start
                        while intersection_path[-1][0] != neighbor:
                            intersection_path = intersection_path[:-1]
                        return intersection_path + new_path[1:]
                    queue_end.append(new_path)
    except Exception:
        print('error running bfs')
        traceback.print_exc()
        if not queue_start:
            print(f"Exhausted all paths from {entity1}, no connection to {entity2}")
            return None

        if not queue_end:
            print(f"Exhausted all paths from {entity2}, no connection to {entity1}")
            return None

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

def get_names_from_actorid(actorid):
    response = requests.get(f"https://api.themoviedb.org/3/person/{actorid}?api_key=97e7f2d04e54e178c11c12a8523d9f05")
    data = json.loads(response.text)
    return data['name']
def get_title_from_movieid(movieid):
    if len(movieid)==0:
        return 'none'
    response = requests.get(f"https://api.themoviedb.org/3/movie/{movieid[0]}?api_key=97e7f2d04e54e178c11c12a8523d9f05")
    data = json.loads(response.text)
    if 'title' in data:
        return data['title']
    else:
        return 'blank'
def lambda_handler():
    try:
        categories = ["cinema"]
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

                except Exception as e:
                    print(f"error in computing shortest path")

            try:
                id = generate_unique_id(ent1, ent2, today, "easy")
            except Exception as e:
                print(f"error in generating unique id")
      #      put_puzzle(id, ent1, ent2, shortest, category, "easy", today)
    except Exception as e:
        print(f"error in lambda handler")
    # Assuming you're using DynamoDB for caching
    print(f"the shortest path between {ent1} and {ent2} is {shortest} nodes")
    for i in range(len(shortest)):
        name = get_names_from_actorid(shortest[i][0])
        if i !=0:
            movie = get_title_from_movieid(shortest[i][1])
            print(f"is in {movie} with ")
        print(f"{name}")
if __name__ == "__main__":
    lambda_handler()