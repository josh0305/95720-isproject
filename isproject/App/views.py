from django.http import HttpResponse
from django.db.models import Max, Min
from django.shortcuts import render
import pandas as pd
import tweepy
import datetime
import time
from App.models import *


# Create your views here.
def getTweetsCreatedTime(request):
    max_created_at = DynamicTweet.objects.all().aggregate(Max('created_at'))['created_at__max']
    min_created_at = DynamicTweet.objects.all().aggregate(Min('created_at'))["created_at__min"]

    return HttpResponse("The earliest tweet is created at {0}.\nThe latest tweet is created at {1}"
                        .format(min_created_at, max_created_at))


# TODO: User enter their BEARER_TOKEN?
BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAANAqdwEAAAAAFUzrlxj%2FmxcZAovCWHcLNUZySuw%3Dr4RV4WWMXrtdWoJ2j2JuicRBoThPsk3labOJPD5pmYactxOMf4"
# BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAADTecgEAAAAAjPIMWtasH01cgbPU9cWlIIooibo%3DEjt7nyuwkjPZXg0SQf6MAdpgVLZTXzN732igsJVQcq5IThwmbY"
client = tweepy.Client(bearer_token=BEARER_TOKEN, wait_on_rate_limit=True)
# TODO: Middleware - Exception Handling related TOKEN (basic API or academicAPI)


def extractCompanyInfoFromTwitterAPI(request):
    # Delete all the rows in Company Table
    DynamicCompany.objects.all().delete()

    # Get the username of company from csv
    df = pd.read_csv('company_twitter_username.csv')
    df.drop_duplicates(keep='first', inplace=True)
    twitterUsername_list = df['username'].tolist()

    # Set Twitter API Token and extract data
    count = 1
    for usern in twitterUsername_list:
        response = client.get_user(username=usern,
                                   user_fields=["created_at", "description", "id", "location", "name",
                                                "pinned_tweet_id", "public_metrics", "url", "username", "verified"])
        if response.data is None:
            continue
        DynamicCompany.objects.create(author_id=response.data.id,
                                      username=response.data.username,
                                      account_name=response.data.name,
                                      created_at=response.data.created_at,
                                      description=response.data.description,
                                      location=response.data.location,
                                      pinned_tweet_id=response.data.pinned_tweet_id,
                                      url=response.data.url,
                                      followers_count=response.data.public_metrics['followers_count'],
                                      following_count=response.data.public_metrics['following_count'],
                                      tweet_count=response.data.public_metrics['tweet_count'],
                                      listed_count=response.data.public_metrics['listed_count'],
                                      verified=response.data.verified)
        # 这里用公司名字会报错
        print("The profile of No.{0} start-up is updated.".format(count))
        count += 1
        time.sleep(1)

    return HttpResponse(" Success! The profile of {0} companies have been updated".format(count))


def extractTweetsFromTwitterAPI(request):

    # start_time: The next second from max_created_at
    max_created_at = DynamicTweet.objects.all().aggregate(Max('created_at'))['created_at__max']
    temp = time.strptime(max_created_at[:19], "%Y-%m-%d %H:%M:%S")
    start_time = (datetime.datetime(*temp[:6])+datetime.timedelta(seconds=1)).strftime("%Y-%m-%dT%H:%M:%SZ")
    end_time = datetime.datetime.today().strftime("%Y-%m-%dT%H:%M:%SZ")

    author_id_list = []
    for dic in DynamicCompany.objects.values("author_id"):
        author_id_list.append(dic["author_id"])

    increase = 0
    for author_id in author_id_list:
        for response in tweepy.Paginator(client.get_users_tweets,
                                         id=author_id,
                                         start_time=start_time,
                                         end_time=end_time,
                                         tweet_fields=["author_id", "created_at", "id", "text", "public_metrics"]):
            if response.data is None:
                continue

            for tweet in response.data:
                DynamicTweet.objects.create(author_id=tweet.author_id,
                                            tweet_id=tweet.id,
                                            text=tweet.text,
                                            created_at=tweet.created_at,
                                            retweets=tweet.public_metrics['retweet_count'],
                                            replies=tweet.public_metrics['reply_count'],
                                            likes=tweet.public_metrics['like_count']
                                            )

                time.sleep(1)

            increase += len(response.data)
            print("{0} tweets have been added to the database.".format(len(response.data)))

        # print(author_id)

    return HttpResponse(" Success! {0} tweets in total have been added to the database.".format(increase))


def searchCompanyInfo(request):
    # get param from response
    input = "iselect   ".strip() #WALKley
    res=[]
    # case-insensitive
    for company in DynamicCompany.objects.raw("SELECT * FROM App_dynamiccompany WHERE account_name LIKE '%{0}%'".format(input)):
        company_info_dic = {"account_name": company.account_name,
                    "description": company.description,
                    "location": company.location,
                    "pinned_tweet_id": company.pinned_tweet_id,
                    "url": company.url,
                    "followers_count": company.followers_count,
                    "following_count": company.following_count,
                    "tweet_count": company.tweet_count,
                    "listed_count": company.listed_count,
                    "verified": company.verified
                    }
                    
        pinned_tweet_dic={}
        if company_info_dic.get("pinned_tweet_id") is not None:
            for tweet in DynamicTweet.objects.raw("SELECT * FROM App_dynamictweet WHERE tweet_id = {0}".format(company_info_dic.get("pinned_tweet_id"))):
                pinned_tweet_dic = {"text": tweet.text,
                                    "created_at": tweet.created_at,
                                    "retweets": tweet.retweets,
                                    "replies": tweet.replies,
                                    "likes": tweet.likes
                                    }
        
        if pinned_tweet_dic:
            company_info_dic["pinned_tweet_id"] = pinned_tweet_dic
        else:
            company_info_dic["pinned_tweet_id"] = None
            
        res.append(company_info_dic)
        print(res)
    return HttpResponse("success")