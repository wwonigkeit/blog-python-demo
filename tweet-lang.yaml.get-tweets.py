#
# This is an example of a script that collects Tweets based on a filter input.
# This is an edit
#

import json
import sys, getopt
import tweepy #required for connecting to the Twitter API

def main(argv):  
    try:
        opts, args = getopt.getopt(argv,"b:t:m:",["bearer_token=","twitter_searchstring=","max_search_returns="])
    except getopt.GetoptError:
        print('py-tweets.py -b <bearer_token> -t <twitter_searchstring> -m <max_search_returns>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('py-tweets.py -b <bearer_token> -t <twitter_searchstring> -m <max_search_returns>')
            sys.exit()
        elif opt in ("-b", "--bearer_token"):
            bearer_token = arg
        elif opt in ("-t", "--twitter_searchstring"):
            twitter_searchstring = arg
        elif opt in ("-m", "--max_search_returns"):
            max_search_returns = arg

    try:
        # Set up the authentication for Twitter
        client = tweepy.Client(bearer_token=bearer_token)

        # Search Recent Tweets
        # This endpoint/method returns Tweets from the last seven days
        response = client.search_recent_tweets(twitter_searchstring, max_results=max_search_returns)

    except tweepy.TweepyException as e:
        # Print the errors for the tweepy call
        print("Tweepy failed with the following error:",e)
        sys.exit(2)

    # In this case, the data field of the Response returned is a list of Tweet
    # objects
    tweets = response.data
    tweet_list = []

    for tweet in tweets:
        obj = {}
        obj["tweet_id"] = tweet.id
        obj["tweet_text"] = tweet.text
        tweet_list.append(obj)

    print(json.dumps(tweet_list, ensure_ascii=False, sort_keys=True, indent=3))

if __name__ == "__main__":
   main(sys.argv[1:])
