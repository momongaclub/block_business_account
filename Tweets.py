import argparse
import tweepy
import MeCab


def parse():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('keys', type=str, help='include four keys.')
    parser.add_argument('keyword', type=str, help='To search word.')
    parser.add_argument('user_id', type=str, help='To search id.')
    parser.add_argument('count', type=int, help='search num.')
    parser.add_argument('output_file', help='outputfile')
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
        self.userid = ""

    def set_keyword(self, keyword):
        self.keyword = keyword

    def set_count(self, count):
        self.count = count

    def get_keyword_tweets(self):
        self.tweets = self.api.search(q=self.keyword, count=self.count)
    
    def get_user_tweets(self):
        pass
        #self.tweets = self.api.search(self.userid, count=self.count)

    def tweets2sentences(self):
        for tweet in self.tweets:
            corpus = tweet.text  # text in tweet
            corpus = corpus.split('\n')
            for sentence in corpus:
                self.sentences.append(sentence)
                # TODO self.sentences.append(tweet.profile)
                # TODO remove RT

    def write_tweets(self, fname):
        with open(fname, 'w') as fp:
            for sentence in self.sentences:
                sentence = sentence.rstrip('\n')
                #sentence = '<BOS>' + ' ' + sentence + ' ' + '<EOS>'
                fp.write(sentence + '\n')

    def sentences2wakati_sentences(self):
        wakati_sentences = []
        mecab = MeCab.Tagger("-Owakati")
        for sentence in self.sentences:
            wakati_sentence = mecab.parse(sentence)
            wakati_sentences.append(wakati_sentence)
        self.sentences = wakati_sentences


def main():
    args = parse()
    twitter_connection = Twitter_connection()
    twitter_connection.load_keys(args.keys)
    twitter_connection.OAuthHandler()
    twitter_connection.access_token()

    twitter = Twitter_api(twitter_connection.auth)
    #print(twitter.api.user_timeline())
    data = twitter.api.user_timeline(args.user_id, count=1)
    print(data[0].text)
    for status in twitter.api.user_timeline(args.user_id, count=100):
        #print(status.user.name, status.text)
        tweet = status.text
        if tweet[0] != '@' and tweet[0] != '@' and tweet[0:2] != 'RT':
           twitter.sentences.append('START')
           twitter.sentences.append(tweet)
           twitter.sentences.append('END')
    #twitter.set_keyword(args.keyword)
    #twitter.set_count(args.count)
    #twitter.get_keyword_tweets()
    #twitter.get_userid_tweets()
    twitter.tweets2sentences()
    #twitter.sentences2wakati_sentences()
    twitter.write_tweets(args.output_file)


if __name__ == '__main__':
    main()
