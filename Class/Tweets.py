import argparse
import tweepy
import MeCab
import sys


def parse():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('keys', type=str, help='include four keys.')
    parser.add_argument('keyword', type=str, help='To search word.')
    parser.add_argument('user_id', type=str, help='To search id.')
    parser.add_argument('count', type=int, help='search num.')
    parser.add_argument('output_file', help='outputfile')
    args = parser.parse_args()
    return args


class Twitter_api():

    def __init__(self):
        self.keys = {}
        self.auth = None
        self.api = None
        self.keyword = ""
        self.count = 0
        self.tweets = ""
        self.sentences = []
        self.userid = ""
        self.user_names = []

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

    def connect_twitter_api(self, fname):
        self.load_keys(fname)
        self.OAuthHandler()
        self.access_token()
        self.api = tweepy.API(self.auth)

    def set_keyword(self, keyword):
        self.keyword = keyword

    def set_count(self, count):
        self.count = count

    def get_keyword_tweets(self):
        self.tweets = self.api.search(q=self.keyword, count=self.count)

    def tweets2sentences(self):
        for tweet in self.tweets:
            corpus = tweet.text  # text in tweet
            corpus = corpus.split('\n')
            for sentence in corpus:
                self.sentences.append(sentence)
                # TODO self.sentences.append(tweet.profile)
                # TODO remove RT

    def write_tweets(self, fname):
        tweet = ''
        with open(fname, 'a') as fp:
            for sentence in self.sentences:
                sentence = sentence.rstrip('\n')
                #sentence = '<BOS>' + ' ' + sentence + ' ' + '<EOS>'
                tweet += sentence + '\t'
            tweet = tweet.rstrip('\t')
            if tweet != '':
                fp.write(tweet)
                fp.write('\n')

    def sentences2wakati_sentences(self):
        wakati_sentences = []
        mecab = MeCab.Tagger("-Owakati")
        for sentence in self.sentences:
            wakati_sentence = mecab.parse(sentence)
            wakati_sentences.append(wakati_sentence)
        self.sentences = wakati_sentences

    def get_user_names(self, user_num):
        # randomに（'て、お、に、はを含む文章をとるか'）
        tweets = self.api.search('は', count=user_num)
        for tweet in tweets:
            self.user_names.append(tweet.user.screen_name)

    def get_users_tweets(self):
        for user_name in self.user_names:
            result = twitter.api.user_timeline(args.user_id, count=args.count, page=page_n)

def main():
    return 0

if __name__ == '__main__':
    main()
