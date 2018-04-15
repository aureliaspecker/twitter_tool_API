# -*- coding: utf-8 -*-
"""
Tool to test the Twitter API
Aurelia Specker 2018
"""
import twitter
import os


def setup_api():
    """Get user credentials from input file and setup api"""

    # Check input file exits, read in consumer and access token keys and secrets and initialise api
    filename = "api_keys.txt" # File containing user credentials
    credentials = [] # Empty list for credentials
    if os.path.isfile(filename):
        file = open(filename, "r") # Open file
        for line in file:
            credentials.append(line.split()[0]) # Read in credentials
        api = twitter.Api(consumer_key = credentials[0], consumer_secret = credentials[1],
                          access_token_key=credentials[2], access_token_secret=credentials[3]) # Initialise API
        file.close()
        print "Api initialised"
    else:
        print "Could not find user credentials, exiting"
        exit(1)

    return api


def get_profile(api):
    """Get valid twitter profile name from user"""

    # Ask user for twitter profile name until an existing profile is entered
    while True:
        profile = "" # Initialise empty string
        while len(profile) == 0: # Repeat until user enters string
            profile = raw_input("Enter Twitter profile: ")
        if profile[0] == "@": # Remove @ sign if included
            profile = profile[1:]
        try:
            api.GetUser(screen_name = profile) # Make call to api to make sure user exists
            break
        except:
            print "Profile does not exist"

    return profile


def get_followers(api, profile):
    """Get followers of provided profile"""

    followers = api.GetFollowers(screen_name = profile) # Make api call

    return followers


def get_tweets(api, profile, number_tweets = 100):
    """Get latest tweets and convert to dictionary"""

    tweets = api.GetUserTimeline(screen_name = profile, count = number_tweets)
    tweets = [t.AsDict() for t in tweets]

    return tweets


def analyse_profile(followers, tweets):
    """Get total number of likes and retweets"""

    # Set up dictionary and counters
    analysis = {}
    total_likes = 0
    total_retweets = 0

    # Analyse tweets
    total_followers = len(followers)
    for tweet in tweets:
        try: total_likes += int(tweet["favorite_count"])
        except: pass
        try: total_retweets += int(tweet["retweet_count"])
        except: pass

    # Populate dictionary
    analysis["total_followers"] = total_followers
    analysis["total_likes"] = total_likes
    analysis["total_retweets"] = total_retweets

    return analysis


def display_results(profile, analysis):
    """Print results of profile analysis to screen"""

    print "Results of analysis of the profile: {0}".format(profile)
    print "Total followers: {0}".format(analysis["total_followers"])
    print "Total likes: {0}".format(analysis["total_likes"])
    print "Total retweets: {0}".format(analysis["total_retweets"])


def main():
    """Set up api with user credentials, get followers and tweets of supplied twitter profile, analyse and print results"""

    twitter_api = setup_api() # Initialise api

    input_profile = get_profile(twitter_api) # Get name of twitter profile from user

    profile_followers = get_followers(twitter_api, input_profile) # Get all followers of profile

    profile_tweets = get_tweets(twitter_api, input_profile) # Get most recent tweets of profile

    profile_analysis = analyse_profile(profile_followers, profile_tweets) # Analyse followers and tweets

    display_results(input_profile, profile_analysis) # Display data


# Execute code only if main file
if __name__ == "__main__":
    main()
