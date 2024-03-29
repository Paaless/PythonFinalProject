import json
import tweepy
import geocoder
import folium
import webbrowser
import os
'''
Authenticate to Twitter and get API object.
'''
def authpy(
            credentials='credentials.json'):
    
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
def read_creds(
            filename: str):
    with open(filename) as f:
        credentials = json.load(f)
    return credentials

'''
This function pulls the tweets from the Twitter's API

It uses the 'Cursor' method so that the number of tweets pulled from the API is not limited to 100

api represents the Twitter API object
hashtag represents the desired hashtag to be searched 
number_of_tweets repesents the desired number of the tweets
'''
def gather_tweets(
                api, 
                hashtag,
                number_of_tweets):
    tweets = tweepy.Cursor(api.search_tweets, q=hashtag, geocode=f'{44.426765},{26.102537},1000km').items(number_of_tweets)
    return tweets

'''
This function returns a tuple containing 2 arrays
Both of the arrays are made of arrays of size 2 that represent the latitude and longitude of the tweets
'''
def return_separate_tweets(
                            tweets):
    location_from_tweeter = []
    location_by_user_location = []
    
    for tweet in tweets:
        if tweet.coordinates == None:
            if tweet.place == None:
                if(tweet.user.location == None):
                    print("No coordinates")
                    print("")
                else:
                    try:
                        coord=geocoder.osm(tweet.user.location)
                        #print("geocoder.osm(tweet.user.location).latlng")
                        print(coord)
                        print("")
                        xy=coord.latlng
                        location_by_user_location.append([xy[0],xy[1]])
                    
                    except TypeError:
                        print("No coordinates")
        else:
            #print("tweet.coordinates.coordinates")
            
            tweet_coord=[tweet.coordinates['coordinates'][0],tweet.coordinates['coordinates'][1]]
            print(tweet_coord)
            print("")
            location_from_tweeter.append(tweet_coord)
    return location_from_tweeter, location_by_user_location

'''
This function is used to create the map

location_from_tweeter represents the array that contains the latitude and longitude extracted from the tweet data
location_by_user_location represents the array that contains the latitude and longitude generated by the location of the tweet's account
filename represents the desired name that the created map should have
 
'''

def create_map(
                location_from_tweeter,
                location_by_user_location,
                filename='map.html'):    
    # This is a more complex map that goes with folium
    '''
    Using folium to create a map with the coordinates of the tweets and then save it in a html file
    Using webbrowser to open the html file
    '''
    new_map = folium.Map()
    for i in location_from_tweeter:
        new_map.add_child(folium.Marker(location=i,icon=folium.Icon(color='green')))

    for j in location_by_user_location:
        new_map.add_child(folium.Marker(location=j,icon=folium.Icon(color='red')))

    new_map.save(filename)
    webbrowser.open('file://' + os.path.realpath(filename))