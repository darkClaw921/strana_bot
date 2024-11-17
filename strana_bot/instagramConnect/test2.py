from instagrapi import Client
from dotenv import load_dotenv
import os
load_dotenv()
from pprint import pprint
INSTA_USER=os.getenv('INSTA_USER')
INSTA_PASSWORD=os.getenv('INSTA_PASSWORD')
CODE=os.getenv('CODE')
cl = Client()
cl.login(INSTA_USER, INSTA_PASSWORD, verification_code=CODE)

user_id = cl.user_id_from_username(INSTA_USER)
pprint(user_id)
medias = cl.user_medias(user_id, 20)

