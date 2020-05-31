from Class import Tweets
import argparse

TAB = '\t'

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

def main():
    args = parser() 
    api = Tweets.Twitter_api()
    api.connect_twitter_api(args.keys)
    api.set_count(args.count)
    api.get_user_names(args.count)
    print(api.user_names)
    all_user_data = []
    for user_name in api.user_names:
        user_data = []
        for page in range(1, args.page_num+1):
            user_datum = api.api.user_timeline(user_name, count=args.count, page=page)
            #user_datum = api.api.user_timeline('tyariRAD', count=args.count, page=page)
            user_data.append(user_datum)
        all_user_data.append(user_data)
    write_data(args.output_file, all_user_data)
    print(user_data[0])



if __name__ == '__main__':
    main()
