from django.db import models


# Dynamic data table
class DynamicCompany(models.Model):
    author_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=128)
    account_name = models.CharField(max_length=128, null=True)
    created_at = models.CharField(max_length=128, null=True)
    description = models.TextField(null=True)
    location = models.CharField(max_length=128, null=True)
    pinned_tweet_id = models.TextField(null=True)
    url = models.TextField(null=True)
    followers_count = models.IntegerField(null=True)
    following_count = models.IntegerField(null=True)
    tweet_count = models.IntegerField(null=True)
    listed_count = models.IntegerField(null=True)
    verified = models.BooleanField(null=True)


class DynamicTweet(models.Model):
    author_id = models.IntegerField()
    tweet_id = models.AutoField(primary_key=True)
    text = models.TextField(null=True)
    created_at = models.CharField(max_length=128, null=True)
    retweets = models.IntegerField(null=True)
    replies = models.IntegerField(null=True)
    likes = models.IntegerField(null=True)


# Built-in data table
class DefaultCompany(models.Model):
    author_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=128)
    account_name = models.CharField(max_length=128, null=True)
    created_at = models.CharField(max_length=128, null=True)
    description = models.TextField(null=True)
    location = models.CharField(max_length=128, null=True)
    pinned_tweet_id = models.TextField(null=True)
    url = models.TextField(null=True)
    followers_count = models.IntegerField(null=True)
    following_count = models.IntegerField(null=True)
    tweet_count = models.IntegerField(null=True)
    listed_count = models.IntegerField(null=True)
    verified = models.BooleanField(null=True)


class DefaultTweet(models.Model):
    author_id = models.IntegerField()
    tweet_id = models.AutoField(primary_key=True)
    text = models.TextField(null=True)
    created_at = models.CharField(max_length=128, null=True)
    retweets = models.IntegerField(null=True)
    replies = models.IntegerField(null=True)
    likes = models.IntegerField(null=True)
