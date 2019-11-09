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

    def connect_twitter_api(self, fname):
        self.load_keys(fname)
        self.OAuthHandler()
        self.access_token()


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
        tweet = ''
        with open(fname, 'w') as fp:
            for sentence in self.sentences:
                sentence = sentence.rstrip('\n')
                #sentence = '<BOS>' + ' ' + sentence + ' ' + '<EOS>'
                tweet += sentence + '\t'
            tweet = tweet.rstrip('\t')
            fp.write(tweet)
            fp.write('\n')

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
    twitter_connection.connect_twitter_api(args.keys)

    twitter = Twitter_api(twitter_connection.auth)
    twitter.set_keyword(args.keyword)
    twitter.set_count(args.count)
    #twitter.get_keyword_tweets()
    #print(twitter.api.user_timeline(user_name, count=args.count))
    # TODO 適当なワードでツイートを取得
    # ツイートからユーザid or ユーザ名を取得
    # ユーザ名からツイートをn件取得
    # 書き込む
    tweet_ = twitter.api.search('は', count=args.count)
    print(tweet_[0])
    print(tweet_[0].text)
    #user_name = tweet_[entitys].screen_name
    #user_name = tweet_[0].entities.user_mentions
    user_name = tweet_[0].entities

    #print(twitter.api.user_timeline(user_name, count=args.count))
    pages = []
    for page_n in range(1):
        result = twitter.api.user_timeline(args.user_id, count=args.count, page=page_n)
        pages.append(result)
    #twitter.set_keyword(user_name)
    #twitter.get_keyword_tweets()
    #print(twitter.tweets)
    #twitter.tweets2sentences()

    # TODO api.report_spam でスパム指定できるそうなのでコレはありがたいかも
    for result in pages:
        for status in result:
            tweet = status.text
            tweet = tweet.rstrip('\n')
            words = tweet.split('\n')
            tweet = ''
            # ひとまずスペースで分割して写真のタグを取り除く。ついでに連結すれば問題ない
            for i in range(len(words)):
                tweet += words[i]
            if tweet[0] != '@' and tweet[0:2] != 'RT': # remove reply and RT
                twitter.sentences.append(tweet)
    twitter.sentences2wakati_sentences()
    twitter.write_tweets(args.output_file)

if __name__ == '__main__':
    main()
