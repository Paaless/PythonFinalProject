from geopandas import GeoDataFrame
from shapely.geometry import Point
import matplotlib.pyplot as plt
from utils import authpy
import geopandas as gpd
import pandas as pd
import webbrowser
import geocoder
import folium
import tweepy
import os

api = authpy('credentials.json')

#print(api)
hashtag_to_search = '#'
number_of_tweets = 0

while (hashtag_to_search == '#'):
    hashtag_to_search +=input('Enter the hashtag you want to search:')

    if (hashtag_to_search == '#'):
        print('You have not entered any hashtag. Please try again!')
    
print("")

while(number_of_tweets == 0):
    try:
        number_of_tweets = int(input('Enter the number of tweets you want to search:'))
    except ValueError:
        print("That was not a valid number. Try again!")
    
    if (number_of_tweets == 0):
        print('You have not entered any number. Please try again!')


version = 0
while(version==0):
    try:
        print("1.Low resolution map")
        print("2.High resolution map")
        version = int(input('Enter the version of the map you want to use:'))
        print("")
    except ValueError:
        print("Oops!  That was not a valid number.  Try again...")
        
    if (version != 1 and version != 2 and version != 0):
        print('Please try again.')
        version = 0
        
tweets = tweepy.Cursor(api.search_tweets, q=hashtag_to_search, geocode=f'{44.426765},{26.102537},1000km').items(number_of_tweets)
tweets_location = []

'''
If the tweet has coordinates, use them, else use the coordinates of the place where the tweet was posted
Use geocoder to get the coordinates of the location of the user and append them to the list tweets_location
'''

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
                    if(version == 1):
                        tweets_location.append([xy[1],xy[0]])
                    else:
                        tweets_location.append([xy[0],xy[1]])
                
                except TypeError:
                    print("No coordinates")
    else:
        #print("tweet.coordinates.coordinates")
        if(version == 1):
            tweet_coord=[tweet.coordinates['coordinates'][1],tweet.coordinates['coordinates'][0]]
        else:
            tweet_coord=[tweet.coordinates['coordinates'][0],tweet.coordinates['coordinates'][1]]
        print(tweet_coord)
        print("")
        tweets_location.append(tweet_coord)

filename='map.html'
if (version == 1):
#this is a simple map that goes with geopandas
    df = pd.DataFrame(tweets_location, columns=['lat', 'lon'])
    #print(df)
    geometry = [Point(xy) for xy in zip(df.lat, df.lon)]
    gdf = GeoDataFrame(df, geometry=geometry)
    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    gdf.plot(ax=world.plot(figsize=(10, 7)), marker='x', color='red', markersize=10);
    #show the map
    plt.title('Tweets location')
    plt.show()

else:
    '''
    Using folium to create a map with the coordinates of the tweets and then save it in a html file
    Using webbrowser to open the html file
    '''
    new_map = folium.Map()
    for i in tweets_location:
        new_map.add_child(folium.Marker(location=i,icon=folium.Icon(color='red')))
    new_map.save(filename)
    webbrowser.open('file://' + os.path.realpath(filename))