import argparse
import tweepy
import sys
import json
import csv


def parse():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('keys', type=str, help='include four keys.')
    args = parser.parse_args()
    return args


class Twitter_connection():

    def __init__(self):
        self.keys = {}
        self.auth = None

    def load_keys(self, fname):
        with open(fname, 'r') as fp:
            for line in fp:
                line.rstrip('\n')
                name, key = line.split(' ')
                self.keys[name] = key.rstrip('\n')

    def OAuthHandler(self):
        self.auth = tweepy.OAuthHandler(self.keys['CONSUMER_KEY'],
                                        self.keys['CONSUMER_SECRET'])

    def access_token(self):
        self.auth.set_access_token(self.keys['ACCESS_TOKEN'],
                                   self.keys['ACCESS_SECRET'])


class Twitter_api():

    def __init__(self, auth):
        self.api = tweepy.API(auth)
        self.keyword = ""
        self.count = 0
        self.tweets = ""

    def set_keyword(self, keyword):
        self.keyword = keyword

    def set_count(self, count):
        self.count = count

    def get_tweets(self):
        self.tweets = self.api.search(self.keyword, self.count)
        return self.tweets


def tweets2sentences(tweets):
    sentences = []
    for tweet in tweets:
        corpus = tweet.text
        corpus = corpus.split('\n')
        for sentence in corpus:
            sentences.append(sentence + '<EOS>')
            # TODO sentences.append(tweet.profile)

    return sentences


def export_csv_data(fname, sentences):
    with open(fname, 'w') as fp:
        for sentence in sentences:
            sentence = sentence + ','
            fp.write(sentence + '\n')


def main():
    args = parse()
    twitter_connection = Twitter_connection()
    twitter_connection.load_keys(args.keys)
    twitter_connection.OAuthHandler()
    twitter_connection.access_token()

    twitter = Twitter_api(twitter_connection.auth)
    keyword = '日本語'
    count = 100
    twitter.set_keyword(keyword)
    twitter.set_count(count)


if __name__ == '__main__':
    main()

