from __future__ import absolute_import, print_function

from tweepy import OAuthHandler, Stream, StreamListener

import json
import datetime
import time

# The consumer key and secret have been generated after I created the app
consumer_key = "Wd5QP2axUwW8z0Pd9kKG5xg91"
consumer_secret = "F5MsIHGHzNwlwmsW3Tkj03JC3vQVU58coeWVXRETKisElumnsg"

# The access token and the access token secret have been generated after I created the app
access_token = "1205453452500975616-yk1rxRYZGOVeAdaIMaOb7dRe129g6b"
access_token_secret = "3m3MuUQ4Wl1NwCj9TeusZAZrP9MKqNcHDLb1TZKYNwAUv"

# This function is used to verify if a 'tweet' is coming from a certain location (identified by
# 'location_name' and 'location_coordinates') and, if that's the case, increment a 'counter' (that
# counts how many tweets have been found coming from the location)
def increment_location_counter(location_name, location_coordinates, tweet, counter):
    tweet_coordinates = tweet["coordinates"]
    tweet_place = tweet["place"]
    # NB: tweet_coordinates[0] is the X and tweet_coordinates[1] is the Y
    if tweet_coordinates is not None:
        # Verifies if the tweet_coordinates are inside the location's bounding box (in our case inside Schiphol's
        # bounding box) and increment the counter if that's the case
        if ((tweet_coordinates["coordinates"][0] >= location_coordinates[0] and tweet_coordinates["coordinates"][0] <=
             location_coordinates[2]) and
                (tweet_coordinates["coordinates"][1] >= location_coordinates[1] and tweet_coordinates["coordinates"][1]
                 <= location_coordinates[3])):
            print("Schiphol TWEET!\n")
            counter += 1
    else:
        if tweet_place is not None:
            # Verifies if the name of the place of the tweet corresponds the location's name (in our case 'Schiphol')
            # and increment the counter if that's the case
            if tweet_place["name"] == location_name:
                print("Schiphol TWEET!\n")
                counter += 1
    return counter

# A listener handles tweets that are received from the stream.
# This is a listener that just analyzes the tweets coming from Amsterdam and keeps
# some counters to compute how many of the tweets are english, how many in dutch and how many are from Schiphol
class AmsterdamListener(StreamListener):
    
    # this method of a stream listener receives all messages and calls functions according to the message type
    def on_data(self, data):
        # transforms the data (in json) in a dictionary
        tweet = json.loads(data)
        #if(time.time() > start_time + PERIOD_OF_TIME):
            #print("Execution ended at" + str(time.time()))
            #print("The id of the first tweet is: " + tweets[0]["id"])
            #print("The id of the last tweet is: " + tweets[len(tweets) - 1]["id"])
            #print("The number of crawled tweets is: " + str(len(tweets)))
            #size = os.path.getsize('C:\\Python27\\Lib\\genericpath.py')
            #print("The size in byte of the result is: " + str(size))
            #stream.disconnect()
        #adds the tweet's details represented as a dictionary to the list 'tweets'
        tweets.append(tweet)
        # counters
        global num_tweets_en
        global num_tweets_nl
        global num_tweets_Schiphol
        # verifies if the tweet is in english and increments the counter in that case
        if(tweet["lang"]) == "en":
            num_tweets_en += 1
        # verifies if the tweet is in dutch and increments the counter in that case
        if(tweet["lang"] == "nl"):
            num_tweets_nl += 1
        # verifies if the tweet comes from Schiphol (by invoking 'increment_location_counter with the correct
        # parameters) and increments the counter in that case
        num_tweets_Schiphol = increment_location_counter("Schiphol", Schiphol_coordinates, tweet, num_tweets_Schiphol)
        # prints some information on the place and the data
        if tweet["place"] is not None:
            print("This is the name of the place: " + tweet["place"]["name"])
        if tweet["coordinates"] is not None:
            print("These are the coordinates: " + str(tweet["coordinates"]["coordinates"][0]) +
                  ", " + str(tweet["coordinates"]["coordinates"][1]))
        print(data)
        # add the data related to the tweet to the JSON file --> not required
        file.write(data) #TOREMOVE
        #print("The number of crawled tweets is: " + str(len(tweets)))
        #print("The number of tweets written in english is: " + str(num_tweets_en))
        #print("The number of tweets written in dutch is: " + str(num_tweets_nl))
        #print("The number of tweets sent from Schiphol is: " + str(num_tweets_Schiphol))
        return True

    def on_error(self, status):
        print(status)

if __name__ == '__main__':

    num_tweets_en = 0
    num_tweets_nl = 0
    num_tweets_Schiphol = 0
    Schiphol_coordinates = [4.73, 52.29, 4.77, 52.32]
    # 2 hours
    PERIOD_OF_TIME = 7200
    starting_time = datetime.datetime.now()
    print("The execution is starting at " + str(starting_time))
    file = open('result_1_3.json', 'w+')
    tweets = []

    # creates the StreamListener and sets the authorization parameters
    l = AmsterdamListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    #In Tweepy, an instance of tweepy.Stream establishes a streaming session and routes messages to StreamListener instance
    stream = Stream(auth, l)
    stream.filter(locations = [4.73,52.29,5.04,52.43] , is_async = True) #is_async is used to let the stream on another thread

    # halts the control for PERIOD_OF_TIME seconds (2 hours in our case)
    time.sleep(PERIOD_OF_TIME)
    # disconnects the stream and stop streaming
    stream.disconnect()
    # prints the final information
    print("Execution started at " + str(starting_time))
    print("Execution ended at " + str(datetime.datetime.now()))
    print("The number of crawled tweets is: " + str(len(tweets)))
    print("The number of tweets sent from Schiphol is: " + str(num_tweets_Schiphol))
    print("The number of tweets written in english is: " + str(num_tweets_en))
    print("The number of tweets written in dutch is: " + str(num_tweets_nl))
