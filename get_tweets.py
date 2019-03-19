import argparse
import tweepy
import json
import csv


def parse():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('keys', type=str, help='include four keys.')
    parser.add_argument('keyword', type=str, help='To search word.')
    parser.add_argument('count', type=int, help='search num.')
    parser.add_argument('output_file', help='outputfile is csv')
    args = parser.parse_args()
    return args


class Twitter_connection():

    def __init__(self):
        self.keys = {}
        self.auth = None

    def load_keys(self, fname):
        with open(fname, 'r') as fp:
            for line in fp:
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
        self.sentences = []

    def set_keyword(self, keyword):
        self.keyword = keyword

    def set_count(self, count):
        self.count = count

    def get_tweets(self):
        self.tweets = self.api.search(q=self.keyword, count=self.count)

    def tweets2sentences(self):
        for tweet in self.tweets:
            corpus = tweet.text # text in tweet
            corpus = corpus.split('\n')
            for sentence in corpus:
                self.sentences.append('<BOS>' + sentence + '<EOS>')
                # TODO self.sentences.append(tweet.profile)

    def export_csv_data(self, fname):
        with open(fname, 'w') as fp:
            for sentence in self.sentences:
                sentence = sentence + ','
                fp.write(sentence + '\n')


def main():
    args = parse()
    twitter_connection = Twitter_connection()
    twitter_connection.load_keys(args.keys)
    twitter_connection.OAuthHandler()
    twitter_connection.access_token()

    twitter = Twitter_api(twitter_connection.auth)
    twitter.set_keyword(args.keyword)
    twitter.set_count(args.count)
    twitter.get_tweets()
    twitter.tweets2sentences()
    twitter.export_csv_data(args.output_file)


if __name__ == '__main__':
    main()

