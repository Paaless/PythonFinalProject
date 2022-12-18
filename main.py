from utils import authpy

api = authpy('credentials.json')

hashtag_to_search = '#'
number_of_tweets = 0

while (hashtag_to_search == '#'):
    hashtag_to_search +=input('Enter the hashtag you want to search:')

    if (hashtag_to_search == '#'):
        print('You have not entered any hashtag. Please try again.')
    
print("")

while(number_of_tweets == 0):
    try:
        number_of_tweets = int(input('Enter the number of tweets you want to search:'))
    except ValueError:
        print("Oops!  That was not a valid number.  Try again...")
    
    if (number_of_tweets == 0):
        print('You have not entered any number. Please try again.')

'''
Select the region and based of that create variables with latitude and longitude in the center of the region
'''
selected = 0
while(selected==0):
    try:
        print('Select the region you want to search:')
        print('1.West Europe\n2.Middle Asia\n3.North Africa\n4.North America')
        selected=int(input('Select from 1 through 4: '))
        if(selected==1):
            print('You have selected Europe')
            center_latitude =0
            center_longitude =0
        elif(selected==2):
            print('You have selected Asia')
            center_latitude =0
            center_longitude =0
        elif(selected==3):
            print('You have selected Africa')
            center_latitude =0
            center_longitude =0
        elif(selected==4):
            print('You have selected America')
            center_latitude =0
            center_longitude =0
        else:
            print('You have selected an invalid option. Please try again.')
            selected=0    
    except ValueError:
        print("Oops!  That was not a valid option.  Try again...")
        

print(hashtag_to_search)
print(number_of_tweets)


