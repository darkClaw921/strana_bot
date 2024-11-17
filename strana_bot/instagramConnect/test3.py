from ensta import Mobile
from dotenv import load_dotenv
import os
load_dotenv()
INSTA_USER=os.getenv('INSTA_USER')
INSTA_PASSWORD=os.getenv('INSTA_PASSWORD')
CODE=os.getenv('CODE')
#https://github.com/diezo/Ensta?tab=readme-ov-file
mobile = Mobile(INSTA_USER, INSTA_PASSWORD, totp_token=CODE)  # Or use email
# direct = mobile.direct()

profile = mobile.profile(INSTA_USER)

print(profile.full_name)
print(profile.biography)
print(profile.follower_count)

# direct.send_text("Hello", thread_id)