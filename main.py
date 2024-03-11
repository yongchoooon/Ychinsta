import os
import util

from datetime import datetime
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from instagram_private_api import Client

load_dotenv()

USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

### global variable
api = None

@app.get("/ping")
def ping():
    return {"message" : "pong"}

@app.get("/login")
def login():
    global api
    api = Client(USERNAME, PASSWORD)
    return {"message" : "login success"}

@app.get("/init")
def init():
    global api
    api = None

@app.get("/get_follower/{username}")
def get_follower(username = USERNAME):
    assert api, "You need to login first"

    user_id = api.username_info(username)['user']['pk']
    first_followers = api.user_followers(user_id, rank_token=api.generate_uuid(),)
    
    followers_info = first_followers.get('users', [])
    
    next_max_id = first_followers.get('next_max_id')
    
    while next_max_id:
        next_followers = api.user_followers(user_id, rank_token=api.generate_uuid(), max_id=next_max_id)
        followers_info.extend(next_followers.get('users', []))
        next_max_id = next_followers.get('next_max_id')

    followers_info = [
        dict(
            pk_id = follower['pk_id'],
            username = follower['username'],
        )
        for follower in followers_info
    ]
    
    now = datetime.now().strftime('%y%m%d_%H%M%S')

    util.save_json(username, 'log_followers', now, followers_info)
    
    return {"message" : "success", "num_followers" : len(followers_info), "now": now}

@app.get("/analyze/{username}")
def analyze(username = USERNAME):
    pre_followers, last_followers = util.load_json(username)
    
    if pre_followers is None:
        return {"message" : "2번 이상 get_follower를 실행해야 합니다."}
    else:
        ids_pre = set([follower['pk_id'] for follower in pre_followers])
        ids_last = set([follower['pk_id'] for follower in last_followers])
        
        ids_new_followers = ids_last - ids_pre
        ids_lost_followers = ids_pre - ids_last
        
        new_followers = [follower for follower in last_followers if follower['pk_id'] in ids_new_followers]
        lost_followers = [follower for follower in pre_followers if follower['pk_id'] in ids_lost_followers]

        return {
            "message" : "success",
            "new_followers" : list(new_followers),
            "lost_followers" : list(lost_followers),
        }

