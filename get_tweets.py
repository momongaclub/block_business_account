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

def text2sentnece(text):
    text = text.split(SEP)
    # print('RT', text[0], 'bool', str(text[0]) == 'RT')
    sentence = ''.join(text)
    return sentence


class User():

    def __init__(self):
        self.name = ''
        self.id = ''
        self.location = ''
        self.url = ''
        self.description = ''
        self.created_at = ''
        self.followers_count = 0
        self.friends_count = 0
        self.favorites_count = 0

def main():
    args = parser() 
    api = Tweets.Twitter_api()
    api.connect_twitter_api(args.keys)
    api.set_count(args.count)
    api.get_user_names(args.count)
    all_user_data = []
    for user_name in api.user_names:
        user_data = []
        user = User()
        user.name = user_name
        user_datum = api.api.user_timeline(user_name, count=1, page=1)
        user_datum = user_datum[RESULT]
        print('user_id:', user_datum.user.screen_name)
        if user_datum.user.location == '':
            user_datum.user.location = 'None'
        user.location = user_datum.user.location
        print('location:', user_datum.user.location)
        print('description:', user_datum.user.description)
        if user_datum.user.entities.get('url') == None:
            print('url:', 'None')
        else:
            print('url:', user_datum.user.entities['url']['urls'][0]['display_url'])
        print('followers_count:', user_datum.user.followers_count)
        print('friends_count:', user_datum.user.friends_count)
        print('created_at:', user_datum.user.created_at)
        print('favorites_count:', user_datum.user.favourites_count)
        for page in range(1, args.page_num+1):
            user_datum = api.api.user_timeline(user_name, count=args.count, page=page)
            # user_datum = api.api.user_timeline('kagamiu055', count=args.count, page=page)
            # user_datum = api.api.user_timeline('tyariRAD', count=args.count, page=page)
            try:
                user_datum = user_datum[RESULT]
                print('text:', text2sentnece(user_datum.text))
            except:
                print('warning:', '0')
            user_data.append(user_datum)
        print(SEP)
        print(user.name, user.location)
        all_user_data.append(user_data)
    # write_data(args.output_file, all_user_data)


if __name__ == '__main__':
    main()
