from shapely.geometry import Point
import matplotlib.pyplot as plt
import geopandas as gpd
from utils import *
import pandas as pd
import folium
import os

# Authenticate to Twitter and get API object.
api = authpy('credentials.json')

# Get user input for the hashtag and the number of tweets
hashtag_to_search = '#'
number_of_tweets = 0

# Handle the case when the user enters an empty hashtag
while (hashtag_to_search == '#'):
    hashtag_to_search +=input('Enter the hashtag you want to search:')

    if (hashtag_to_search == '#'):
        print('You have not entered any hashtag. Please try again!')
    
print("")

# Handle the case when the user enters a number that is not an integer
while(number_of_tweets == 0):
    try:
        number_of_tweets = int(input('Enter the number of tweets you want to search:'))
    except ValueError:
        print("That was not a valid number. Try again!")
    
    if (number_of_tweets == 0):
        print('You have not entered any number. Please try again!')

# Search for the tweets
tweets = gather_tweets(api, hashtag_to_search, number_of_tweets)

'''
If the tweet has coordinates, use them, else use the coordinates of the place where the tweet was posted
Use geocoder to get the coordinates of the location of the user and append them to the list tweets_location
'''

location_from_tweeter = []
location_by_user_location = []

# Either get the coordinates from the tweet or from the place where the tweet was posted
location_from_tweeter, location_by_user_location = return_separate_tweets(tweets)


'''
Using folium to create a map with the coordinates of the tweets and then save it in a html file
Using webbrowser to open the html file
'''
create_map(location_from_tweeter, location_by_user_location)