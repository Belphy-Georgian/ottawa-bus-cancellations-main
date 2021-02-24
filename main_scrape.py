import utils
import pandas as pd
import numpy as np
import datetime

def main():
    choice = ''

    while choice != '0':
        print('\n\nSelect action:\n')
        print('1: download and import GTFS')
        print('2: download and import tweets from @OCTranspoLive')
        print('3: show database stats')
        print('4: correlate and export CSV files')
        print('0: exit\n')
        choice = input('Enter the number of action: ')

        if choice == '1':
            download_gtfs()
        if choice == '2':
            download_tweets()
        if choice == '3':
            show_database()
        if choice == '4':
            export_csv()


def download_gtfs():
    print(f'\ntrying to download GTFS from OC Transpo...')
    print(utils.download_gtfs())


def download_tweets():
    print('\n----------------------------------------')
    print('Enter the year and month that you want to download')
    year = datetime.datetime.now().year
    month = datetime.datetime.now().month
    tweets = utils.scrape_tweets(year=year, month=month)
    ### temp for debug
    tweet_ids = []
    tweet_texts = []
    tweet_isodates = []
    for tweet in tweets:
        tweet_ids.append(tweet.id)
        tweet_texts.append(tweet.content)
        tweet_isodates.append(tweet.date.isoformat())
    tweets_dict = {
        'id': tweet_ids,
        'text': tweet_texts,
        'isodate': tweet_isodates
    }
    df_tweets = pd.DataFrame(tweets_dict)
    df_tweets.set_index('id', inplace=True)
    df_tweets.to_csv('./csv/tweets_raw.csv')
    df_tweets_x = pd.read_csv('./csv/tweets_raw.csv')
    utils.process_tweets_x(df_tweets_x)
    # utils.process_tweets(tweets)


def show_database():
    row_counters = utils.show_db_counter()

    print('\n----------------------------------------')
    for (key, value) in row_counters.items():
        print(f'{key}: {value}')


def export_csv():
    utils.calculate_cancellation_rate()


# Standard boilerplate to call the main() function to begin
# the program.
if __name__ == '__main__':
    main()
