import json
import tweepy

'''
Authenticate to Twitter and get API object.
'''
def authpy(credentials='credentials.json'):
    
    creds = read_creds(credentials)
    key, secrets = creds['api_key'], creds['api_secrets']
    tk, tk_secrets = creds['access_token'], creds['access_secret']
 
    # Authenticate to Twitter
    auth = tweepy.OAuthHandler(key,secrets)
    auth.set_access_token(tk,tk_secrets)
 
    # Create the API object
    api = tweepy.API(auth, wait_on_rate_limit=True)
    return api

'''
Used to read the credentials from a JSON file. 
'''
def read_creds(filename):
    with open(filename) as f:
        credentials = json.load(f)
    return credentials

'''
Used to plot the location of the tweets on a map.
'''
# def plot_on_map():
    