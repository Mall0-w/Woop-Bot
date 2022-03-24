from twitchAPI.twitch import Twitch
from pprint import pprint
import os

twitch = Twitch(os.environ.get("TWITCH_CLIENT_ID"), os.environ.get("TWITCH_CLIENT_SECRET_ID"))
#setting up authentication call but not passing any authentication, since not needed
#doing this because rate limits for authenticated apps are better
twitch.authenticate_app([])

def check_user_online(username=os.environ.get("USERNAME")):
    try:
        resp = twitch.get_streams(user_login=[username])
        #if no ongoing streams
        if(len(resp.data) == 0):
            return None
        #otherwise return data
        return resp.data
    except:
        return None