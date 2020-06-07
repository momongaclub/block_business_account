from Class import Tweets
import argparse
import sys

RESULT = 0
TAB = '\t'
SEP = '\n'
SPACE = ' '

def parser():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('keys', type=str, help='include four keys.')
    parser.add_argument('keyword', type=str, help='To search word.')
    parser.add_argument('count', type=int, help='search num.')
    parser.add_argument('page_num', type=int, help='page_num')
    parser.add_argument('output_file', help='outputfile')
    args = parser.parse_args()
    return args


def write_data(fname, all_user_data):
    with open(fname, 'a') as fp:
        for user_data in all_user_data:
            for datum in user_data:
                datum = str(datum)
                fp.writelines(datum + TAB)
            fp.write('\n')

def text2sentence(text):
    text = text.split(SEP)
    # print('RT', text[0], 'bool', str(text[0]) == 'RT')
    sentence = ''.join(text)
    return sentence


def is_location(location):
    if location == '':
        location = None
    return location

def is_url(entities):
    url = ''
    try:
        url = entities['url']['urls'][0]['display_url']
    except:
        url = 'None'
    return url

def datetime2date(datetime):
    date = datetime.split(SPACE)[0]
    return date

class User():

    def __init__(self):
        self.name = ''
        self.id = ''
        self.description = ''
        self.location = ''
        self.url = ''
        self.created_at = ''
        self.followers_count = 0
        self.friends_count = 0
        self.favorites_count = 0
        self.texts = []

    def write_data(self, fname):
        with open(fname, 'a') as fp:
            for line in self.__dict__.items():
                if str(line[0]) == 'texts':
                    sentences = ''
                    for sentence in line[1]:
                        sentences = sentences + sentence + TAB
                    sentences.rstrip(TAB)
                    fp.write(sentences)
                else:
                    fp.write(str(line[1]))
                    fp.write(TAB)
            fp.write(SEP)

    def __str__(self):
        for line in self.__dict__.items():
            print(str(line))
        return ''

def main():
    args = parser() 
    api = Tweets.Twitter_api()
    api.connect_twitter_api(args.keys)
    api.set_count(args.count)
    api.get_user_names(args.count)
    all_user_data = []
    for user_name in api.user_names:
        # user_data = []
        user = User()
        user.name = user_name
        user_datum = api.api.user_timeline(user.name, count=1, page=1)
        user_datum = user_datum[RESULT]
        user.id = user_datum.id
        user.screen_name = user_datum.user.screen_name
        user.description = text2sentence(user_datum.user.description)
        user.followers_count = user_datum.user.followers_count
        user.friends_count = user_datum.user.friends_count
        # TODO datetime format になってるので文字列に変更
        user.created_at = datetime2date(str(user_datum.user.created_at))
        user.favourites_count = user_datum.user.favourites_count
        user.location = is_location(user_datum.user.location)
        user.url = is_url(user_datum.user.entities)
        for page in range(1, args.page_num+1):
            user_datum = api.api.user_timeline(user.name, count=args.count, page=page)
            try:
                user_datum = user_datum[RESULT]
                text = text2sentence(user_datum.text)
            except:
                text ='None'
            #user_data.append(user_datum)
            user.texts.append(text)
        print(SEP)
        print(user)
        user.write_data(args.output_file)
        all_user_data.append(user)
    # write_data(args.output_file, all_user_data)


if __name__ == '__main__':
    main()
