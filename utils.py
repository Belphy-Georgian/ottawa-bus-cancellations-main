import os
import subprocess
import re
import sqlite3
import datetime
import requests
import pandas as pd
import numpy as np
#import GetOldTweets3 as got
import snscrape as sntwitter


def download_gtfs():
    output = ''
    time_now = datetime.datetime.now()
    filepath = time_now.strftime('./archives/octranspo_gtfs_%Y%m%d.zip')
    ### mkdir
    print(f'create directory for archives')
    try:
        os.mkdir('./archives/')
    except FileExistsError:
        print('directory exists')
    output += f'filepath: {filepath}\n'

    ### download zip archive from OC Transpo
    print(f'downloading...')
    gtfs_url = 'https://www.octranspo.com/files/google_transit.zip'
    response = requests.get(gtfs_url)
    with open(filepath, 'wb') as f:
        f.write(response.content)

    print(f'importing... (5 - 10 mins)')
    task = subprocess.run(["C:/Users/guill/OneDrive/Documents/Documentos/Georgian College/Big Data/Second Semester/MRP/WebScraping/WebScraping/gtfsdb-master/gtfsdb-master/bin/gtfsdb-load", '--database', 'sqlite:///gtfs.db', filepath], stdout=subprocess.PIPE)
    output += task.stdout.decode('utf-8')

    return output


def show_db_counter():
    title = 'GTFS Database'
    ########## sqlite
    ### connect to sqlite database or create it if it doesn't exist
    conn = sqlite3.connect('gtfs.db', isolation_level=None)
    # conn = sqlite3.connect(':memory:', isolation_level=None)
    cur = conn.cursor()
    row_counters = {
        'agency': 0,
        'calendar': 0,
        'calendar_dates': 0,
        'routes': 0,
        'shapes': 0,
        'stop_times': 0,
        'stops': 0,
        'trips': 0
    }

    ### agency
    cur.execute(f'SELECT COUNT(*) FROM agency')
    row = cur.fetchone()
    row_counters['agency'] = row[0]
    ### calendar
    cur.execute(f'SELECT COUNT(*) FROM calendar')
    row = cur.fetchone()
    row_counters['calendar'] = row[0]
    ### calendar_dates
    cur.execute(f'SELECT COUNT(*) FROM calendar_dates')
    row = cur.fetchone()
    row_counters['calendar_dates'] = row[0]
    ### routes
    cur.execute(f'SELECT COUNT(*) FROM routes')
    row = cur.fetchone()
    row_counters['routes'] = row[0]
    ### shapes
    cur.execute(f'SELECT COUNT(*) FROM shapes')
    row = cur.fetchone()
    row_counters['shapes'] = row[0]
    ### stop_times
    cur.execute(f'SELECT COUNT(*) FROM stop_times')
    row = cur.fetchone()
    row_counters['stop_times'] = row[0]
    ### stops
    cur.execute(f'SELECT COUNT(*) FROM stops')
    row = cur.fetchone()
    row_counters['stops'] = row[0]
    ### trips
    cur.execute(f'SELECT COUNT(*) FROM trips')
    row = cur.fetchone()
    row_counters['trips'] = row[0]
    ### bus_cancellations
    cur.execute(f'SELECT COUNT(*) FROM bus_cancellations')
    row = cur.fetchone()
    row_counters['bus_cancellations'] = row[0]
    
    ### close database connection
    cur.close()
    conn.close()

    return row_counters


def calculate_bus_trips():
    results = []
    ########## sqlite
    ### connect to sqlite database or create it if it doesn't exist
    conn = sqlite3.connect('gtfs.db', isolation_level=None)
    # conn = sqlite3.connect(':memory:', isolation_level=None)
    cur = conn.cursor()

    start_date = datetime.date(2020, 1, 1)
    end_date = datetime.date(2020, 2, 1)
    # print(f'start_date: {start_date}\t\tend_date: {end_date}')
    print(f'calculating bus trips...')
    date_delta = end_date - start_date

    number_of_weekdays = {
        'mon': 0,
        'tue': 0,
        'wed': 0,
        'thu': 0,
        'fri': 0,
        'sat': 0,
        'sun': 0
    }
    for i in range(date_delta.days):
        target_day = start_date + datetime.timedelta(days=i)
        weekday = target_day.weekday()
        if weekday == 0:
            number_of_weekdays['mon'] += 1
        elif weekday == 1:
            number_of_weekdays['tue'] += 1
        elif weekday == 2:
            number_of_weekdays['wed'] += 1
        elif weekday == 3:
            number_of_weekdays['thu'] += 1
        elif weekday == 4:
            number_of_weekdays['fri'] += 1
        elif weekday == 5:
            number_of_weekdays['sat'] += 1
        elif weekday == 6:
            number_of_weekdays['sun'] += 1

    ### get all route_id
    route_ids = []
    cur.execute(f'SELECT route_id FROM routes')
    rows = cur.fetchall()
    for row in rows:
        route_ids.append(row[0])

    for route_id in route_ids:
        number_of_buses = 0
        nob_mon = 0
        nob_tue = 0
        nob_wed = 0
        nob_thu = 0
        nob_fri = 0
        nob_sat = 0
        nob_sun = 0
        ### get unique service_id for each route_id
        cur.execute(f'''SELECT trips.route_id, COUNT(trips.trip_id) AS counter, trips.trip_id, calendar.* FROM trips
            INNER JOIN calendar ON trips.service_id = calendar.service_id
            WHERE trips.route_id = "{route_id}"
            GROUP BY calendar.service_id 
            ''')
        rows = cur.fetchall()
        for row in rows:
            # row[1] is counter
            counter = row[1]
            # row[4] is mon
            ### number_of_buses is total number of buses in a month
            ### nob_xxx is the total number of buese in a week
            if row[4] == 1:
                number_of_buses += counter * number_of_weekdays['mon']
                nob_mon += counter
            if row[5] == 1:
                number_of_buses += counter * number_of_weekdays['tue']
                nob_tue += counter
            if row[5] == 1:
                number_of_buses += counter * number_of_weekdays['wed']
                nob_wed += counter
            if row[6] == 1:
                number_of_buses += counter * number_of_weekdays['thu']
                nob_thu += counter
            if row[7] == 1:
                number_of_buses += counter * number_of_weekdays['fri']
                nob_fri += counter
            if row[8] == 1:
                number_of_buses += counter * number_of_weekdays['sat']
                nob_sat += counter
            if row[9] == 1:
                number_of_buses += counter * number_of_weekdays['sun']
                nob_sun += counter
        result = {
            'route_id': route_id,
            'number_of_buses': number_of_buses,
        }
        for i in range(date_delta.days):
            target_day = start_date + datetime.timedelta(days=i)
            weekday = target_day.weekday()
            day_of_month = target_day.strftime('%d')
            if weekday == 0:
                result[day_of_month] = nob_mon
            elif weekday == 1:
                result[day_of_month] = nob_tue
            elif weekday == 2:
                result[day_of_month] = nob_wed
            elif weekday == 3:
                result[day_of_month] = nob_thu
            elif weekday == 4:
                result[day_of_month] = nob_fri
            elif weekday == 5:
                result[day_of_month] = nob_sat
            elif weekday == 6:
                result[day_of_month] = nob_sun
        results.append(result)
        print(f'.', end='')
    
    ### close database connection
    cur.close()
    conn.close()

    return results


def calculate_cancellation_rate():
    ### structure of trip_counters
    # [{
    #     'route_id': route_id,
    #     'number_of_buses': number_of_buses
    # }]
    #trip_counters = calculate_bus_trips()
    ### structure of cancellations
    # [{
    #     'tweet_id': row[0],
    #     'affected_route': row[1],
    #     'conditions': row[2],
    #     'create_time': row[3],
    #     'destination': row[4],
    #     'destination_time': row[5],
    #     'message': row[6],
    #     'next_trip': row[7],
    #     'route_short_name': row[8],
    #     'source': row[9],
    #     'source_time': row[10],
    #     'temperature': row[11],
    #     'title': row[12]
    #     'diff', 'route_id', 'trip_id', 'service_id', 
    #     'cancellation_date', 'start_date', 'julian_start_date', 'end_date', 'julian_end_date', 
    #     'src_arrival_time', 'src_departure_time', 'src_stop_sequence', 'src_stop_id', 'src_stop_name', 'src_stop_lat', 'src_stop_lon', 
    #     'dst_arrival_time', 'dst_departure_time', 'dst_stop_sequence', 'dst_stop_id', 'dst_stop_name', 'dst_stop_lat', 'dst_stop_lon'
    # }]
    cancellations = read_cancellations()
    ### search for intermediate stops
    stop_list = get_stop_list(cancellations)
    # print('stop list')
    # for stop in stop_list:
    #     print(stop)

    #for trip_counter in trip_counters:
        # trip_counter['cancellations'] = list(filter(lambda e: e['route_id'] == trip_counter['route_id'], cancellations))
    #    trip_counter['number_of_cancellations'] = len(list(filter(lambda e: e['route_id'] == trip_counter['route_id'], cancellations)))
    #    if trip_counter['number_of_buses'] == 0:
    #        trip_counter['cancellation_rate'] = 0.0
    #    else:
    #        trip_counter['cancellation_rate'] = trip_counter['number_of_cancellations'] / trip_counter['number_of_buses']
    
    # print(trip_counters)

    ### mkdir for csv
    try:
        os.mkdir('./csv/')
    except FileExistsError:
        print('directory exists')

    df_cancellations = pd.DataFrame(cancellations)
    df_cancellations.set_index('tweet_id', inplace=True)
    print(df_cancellations)
    df_cancellations.to_csv('./csv/cancellations_raw.csv')
    print(f'exported cancellations_raw.csv')

    #df_cancellation_rate = pd.DataFrame(trip_counters)
    #df_cancellation_rate.set_index('route_id', inplace=True)
    #print(df_cancellation_rate)
    #df_cancellation_rate.to_csv('./csv/cancellation_rate.csv')
    #print(f'exported cancellation_rate.csv')

    #df_cancellation_rate_details = []
    #for trip_counter in trip_counters:
    #    route_id = trip_counter['route_id']
        ### exclude columns 'route_id', 'number_of_buses', 'number_of_cancellations' and 'cancellation_rate'
    #    x_labels = ['route_id'] + list(trip_counter.keys())[2:-2]
    #    y_labels = ['00:00', '01:00', '02:00', '03:00', '04:00', '05:00', '06:00', '07:00', '08:00', '09:00', '10:00', '11:00',
    #        '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00', '21:00', '22:00', '23:00']
    #    temp_df_cancellation_rate_details = pd.DataFrame(np.zeros((len(y_labels), len(x_labels))), index=y_labels, columns=x_labels)
    #    temp_df_cancellation_rate_details.loc[:, 'route_id'] = route_id
        ### filter cancellations by route_id
    #    filtered_cancellations = list(filter(lambda e: e['route_id'] == route_id, cancellations))
        ### add the number of cancellation based on the time
    #    for filtered_cancellation in filtered_cancellations:
            ### covert ISO string to datetime object and get only the day value
    #        cancellation_day = datetime.datetime.fromisoformat(filtered_cancellation['create_time']).strftime('%d')
            ### substr the first 2 characters as hour
    #        cancellation_hour = filtered_cancellation['source_time'][0:2] + ':00'
            # print(f'row: {cancellation_hour} col: {cancellation_day}')
            ### skip if the srouce_time format is not correct
    #        try:
                ### add 1 to the specific time slot
    #            temp_df_cancellation_rate_details.at[cancellation_hour, cancellation_day] += 1
    #        except KeyError as err:
    #            print(err)
    #    print(route_id)
    #    print(temp_df_cancellation_rate_details)
    #    df_cancellation_rate_details.append(temp_df_cancellation_rate_details)
    #df_cancellation_rate_details_all = pd.concat(df_cancellation_rate_details)
    #df_cancellation_rate_details_all.to_csv(f'./csv/cancellation_rate_details.csv')
    #print(f'exported cancellation_rate_details.csv')

    df_stop_list = pd.DataFrame(stop_list)
    df_stop_list.set_index('tweet_id', inplace=True)
    print(df_stop_list)
    df_stop_list.to_csv('./csv/cancellations_stop_list.csv')
    print(f'exported cancellations_stop_list.csv')

    #return trip_counters


def scrape_tweets(year, month):
    start_year = int(year)
    start_month = int(month)
    start_date = datetime.date(start_year, start_month, 1)

    end_year = start_year
    end_month = start_month + 1
    if end_month == 13:
        end_year += 1
        end_month = 1
    end_date = datetime.date(end_year, end_month, 1) - datetime.timedelta(days=1)
    since = start_date.strftime('%Y-%m-%d')
    until = end_date.strftime('%Y-%m-%d')
    print(f'Downloading {since} - {until}')
    tweetString = 'from:@OCTranspoLive + since:' + since + ' until:' + until + ' -filter:links -filter:replies'
    print(tweetString)
    tweets = []
    for i, tweet in enumerate(sntwitter.modules.twitter.TwitterSearchScraper(tweetString).get_items()):
        print(tweet)
        print(tweet.date.strftime("%d/%m/%Y") + ' ' + tweet.content)
        print(tweet.id)
        tweets.append(tweet)
        if i > 100:
            break
    tweets
    return tweets
    ### GetOldTweets3

    # tweetCriteria = got.manager.TweetCriteria().setUsername("OCTranspoLive")\
    #                                        .setSince(since)\
    #                                        .setUntil(until)\
    #                                        .setEmoji("unicode")
    #                                        # .setMaxTweets(101)\
    # tweets = got.manager.TweetManager.getTweets(tweetCriteria)
    # tweet = got.manager.TweetManager.getTweets(tweetCriteria)[0]

    # print(type(tweets))


def process_tweets(tweets):
    cancellations = []
    for tweet in tweets:
        cancellation = process_tweet(tweet.text)
        ### check if cancellation is empty
        if cancellation:
            cancellation['tweet_id'] = tweet.id
            cancellation['create_time'] = tweet.date.isoformat()
            # print(tweet.date)
            # print(tweet.formatted_date )
            cancellations.append(cancellation)
        # print(cancellation)
    # print(cancellations)

    ### GetOldTweets3

    store_tweets(cancellations)

    print(f'Downloaded tweets:\t{len(tweets)}')
    print(f'Vaild tweets:\t\t{len(cancellations)}')

def process_tweets_x(df_tweets_x):
    cancellations = []
    for index, row in df_tweets_x.iterrows():
        cancellation = process_tweet(row['text'])
        ### check if cancellation is empty
        if cancellation:
            cancellation['tweet_id'] = row['id']
            cancellation['create_time'] = row['isodate']
            # print(tweet.date)
            # print(tweet.formatted_date )
            cancellations.append(cancellation)
        # print(cancellation)
    # print(cancellations)

    ### GetOldTweets3

    store_tweets(cancellations)

    print(f'Downloaded tweets:\t{df_tweets_x.shape}')
    print(f'Vaild tweets:\t\t{len(cancellations)}')

def process_tweet(message):
    data_cleaned = False
    ### convert message to lower case and copy to another variable for easy matching
    message_lower = message.lower()
    # time_posted_str = '2020-02-18 13:30:26'
    # tweet = '85 Bayshore: the trip is cancelled from Terrasses de la Chaudière at 13:04 to Preston/Somerset at 13:10.  The next trip is 15 minutes later.'
    # tweet = '39 Blair: Trip is cancelled between Trim Station at 8:25 and Blair Station at 8:43. Next trip is 9 minutes later.'
    # print(message)
    
    ### convert string to datetime object
    # time_posted = datetime.datetime.strptime(time_posted_str, '%Y-%m-%d %H:%M:%S')
    ### determine to use "from-to" or "between-and"
    print(message)
    route_short_name = ''
    route_name = ''
    source = ''
    source_time = ''
    destination = ''
    destination_time = ''
    next_trip_minutes = ''
    if ('from' in message_lower or 'between' in message_lower) and 'cancelled' in message_lower:
        ### route_short_name
        re_route_short_name = re.search('(\d)+', message_lower)
        if re_route_short_name != None:
            route_short_name = re_route_short_name.group()
        ### route_name
        re_first_colon = re.search(':', message_lower)
        if re_first_colon != None:
            route_name = message[re_route_short_name.end():re_first_colon.start()].strip()
        ### from || between
        re_from = re.search(' from ', message_lower)
        if re_from == None:
            re_from = re.search(' from', message_lower)
        if re_from == None:
            re_from = re.search(' between ', message_lower)
        ### to || and
        re_to = re.search(' t[o0] ', message_lower)
        if re_to == None:
            re_to = re.search(' to', message_lower)
        if re_to == None:
            re_to = re.search(' and ', message_lower)
        if re_to == None:
            re_to = re.search('and ', message_lower)
        if re_to == None:
            re_to = re.search(' et ', message_lower)
        if re_to == None:
            re_to = re.search(' (\d+)(\s?):(\s?)(\d+) ', message_lower)
        ### src and dst
        offset = re_to.end()
        re_trip = re.search(' trip[s]? ', message_lower[offset:])
        if re_trip != None:
            re_trip_index = re_trip.start()
            ### minutes
            re_minutes = re.search('(\d+)', message_lower[re_trip_index+offset:])
            if re_minutes != None:
                next_trip_minutes = re_minutes.group()
        else:
            re_trip_index = len(message_lower)
        re_times = re.finditer('(\d+)(\s?):(\s?)(\d+)', message_lower)
        time_matches = list(re_times)
        if len(time_matches) == 2:
            re_from_time = time_matches[0]
            re_to_time = time_matches[1]
            source_time = process_src_dst_time(re_from_time.group())
            destination_time = process_src_dst_time(re_to_time.group())
            source = process_stop_name(message[re_from.end():re_from_time.start()])
            destination = process_stop_name(message[re_to.end():re_to_time.start()])
        if len(time_matches) == 1:
            print(time_matches[0])
            re_from_time = time_matches[0]
            source_time = process_src_dst_time(re_from_time.group())
            source = process_stop_name(message[re_from.end():re_to.start()])
            ### time is placed after destination stop name
            if re_from_time.start() > re_to.end():
                destination = process_stop_name(message[re_to.end():re_from_time.start()])
            else:
                ### ignore '. ' before 'next trip'
                destination = process_stop_name(message[re_to.end():re_trip_index-2])
        if len(time_matches) == 0:
            source = process_stop_name(message[re_from.end():re_to.start()])
            destination = process_stop_name(message[re_to.end():re_trip_index])

        # print(f'{route_short_name}, {route_name}, {source}, {source_time}, {destination}, {destination_time}, {next_trip_minutes}')

        data_cleaned = True
    
    # if 'between' in message_lower and 'and' in message_lower and 'cancelled' in message_lower:
        # first_space_index = message_lower.find(' ')
        # colon_index = message_lower.find(':')
        # between_index = message_lower.find(' between ')
        # second_colon_index = message_lower[between_index:].find(':') + between_index
        # and_index = message_lower[between_index:].find(' and ') + between_index
        # third_colon_index = message_lower[and_index:].find(':') + and_index
        # next_trip_index = message_lower[third_colon_index:].find('next trip') + third_colon_index
        # minutes_index = message_lower[third_colon_index:].find(' min') + third_colon_index
    
        # route_short_name = message[:first_space_index].strip()
        # route_name = message[first_space_index:colon_index].strip()
        # source = process_stop_name(message[between_index + 9:second_colon_index-2])
        # source_time = process_src_dst_time(message[second_colon_index-2:second_colon_index+3].strip())
        # destination = process_stop_name(message[and_index + 5:third_colon_index-2])
        # destination_time = process_src_dst_time(message[third_colon_index-2:third_colon_index+3].strip())
        # next_trip_minutes = process_next_trip(message[next_trip_index + 9:minutes_index])
        # data_cleaned = True

    cancellation = {}
    if data_cleaned:
        cancellation = {
            'route_short_name': route_short_name,
            'affected_route': f'{route_short_name} {route_name}',
            'destination': destination,
            'destination_time': destination_time,
            'message': message,
            'next_trip': next_trip_minutes,
            'source': source,
            'source_time': source_time,
            'title': f'{route_short_name} {route_name}: Cancelled trip',
            'conditions': '',
            'temperature': ''
        }
        # print('')
        # print(time_posted)
        # print(route_number)
        # print(route_name)
        # print(source)
        # print(source_time)
        # print(destination)
        # print(destination_time)

    return cancellation


def process_stop_name(stop_name):
    ### convert the stop name to lower case for easy matching
    stop_name = stop_name.lower()

    ### remove extra words
    if stop_name.find('–') >= 0:
        stop_name = stop_name.replace('–', '-')
    if stop_name.find(' - ') >= 0:
        stop_name = stop_name.replace(' - ', '-')
    if stop_name.find(' at') >= 0:
        stop_name = stop_name.replace(' at', '')
    if stop_name.find(' station') >= 0:
        stop_name = stop_name.replace(' station', '')
    if stop_name.find(' stn') >= 0:
        stop_name = stop_name.replace(' stn', '')
    if stop_name.find(' center') >= 0:
        stop_name = stop_name.replace(' center', '')
    if stop_name.find(' centre') >= 0:
        stop_name = stop_name.replace(' centre', '')
    if stop_name.find(' ctr') >= 0:
        stop_name = stop_name.replace(' ctr', '')
    if stop_name.find(' termianl') >= 0:
        stop_name = stop_name.replace(' termianl', '')
    if stop_name.find(' park') >= 0:
        stop_name = stop_name.replace(' park', '')
    if stop_name.find(' chaudières') >= 0:
        stop_name = stop_name.replace(' chaudière', '')
    if stop_name.find(' collégiale') >= 0:
        stop_name = stop_name.replace(' collégiale', '')
    if stop_name.find(' terminal') >= 0:
        stop_name = stop_name.replace(' terminal', '')
    if stop_name.find(' recreation') >= 0:
        stop_name = stop_name.replace(' recreation', '')
    if stop_name.find(' park') >= 0:
        stop_name = stop_name.replace(' park', '')
    if stop_name.find(' and') >= 0:
        stop_name = stop_name.replace(' and', '')
    if stop_name.find(' &') >= 0:
        stop_name = stop_name.replace(' &', '')
    if stop_name.find(' ride') >= 0:
        stop_name = stop_name.replace(' ride', '')
    if stop_name.find(' road') >= 0:
        stop_name = stop_name.replace(' road', '')
        
    if stop_name.find('the ') == 0:
        stop_name = stop_name.replace('the ', '')
    if stop_name.find('la ') == 0:
        stop_name = stop_name.replace('la ', '')
    if stop_name.find('ottawa airport') == 0:
        stop_name = stop_name.replace('ottawa airport', 'airport')
    if stop_name.find('carleton university') >= 0:
        stop_name = stop_name.replace('carleton university', 'carleton u')
    if stop_name.find('millenium') >= 0:
        stop_name = stop_name.replace('millenium', ' millennium')
    if stop_name.find('st. laurent') >= 0:
        stop_name = stop_name.replace('st. laurent', 'st-laurent')
    if stop_name.find('st. laurents') >= 0:
        stop_name = stop_name.replace('st. laurent', 'st-laurent')
    if stop_name.find('terrassess') >= 0:
        stop_name = stop_name.replace('terrassess', 'terrasses')
    if stop_name.find('cardelred-goulbourn') >= 0:
        stop_name = stop_name.replace('cardelred-goulbourn', 'cardelrec-goulbourn')
    if stop_name.find('cardelred-goulbrourn') >= 0:
        stop_name = stop_name.replace('cardelred-goulbrourn', 'cardelrec-goulbourn')
    if stop_name.find('place du portage') >= 0:
        stop_name = stop_name.replace("place du portage", "place d'accueil")
    if stop_name.find('lyon 1') >= 0:
        stop_name = stop_name.replace('lyon 1', 'lyon')

    ### trim white space on both side
    stop_name = stop_name.strip()

    return stop_name.upper()


def process_next_trip(next_trip_minutes):
    ### convert the text to lower case for easy matching
    next_trip_minutes = next_trip_minutes.lower()
    ### check if text contain 'is'
    if next_trip_minutes.find('is') >= 0:
        next_trip_minutes = next_trip_minutes.replace('is', '')
    ### trim white space on both side
    next_trip_minutes = next_trip_minutes.strip()

    return next_trip_minutes


def process_src_dst_time(src_dst_time):
    ### insert a leading 0
    src_dst_time = f'0{src_dst_time}'
    colon_index = src_dst_time.find(':')
    hour = src_dst_time[:colon_index].strip()
    hour = hour[-2:]
    minute = src_dst_time[colon_index+1:].strip()
    src_dst_time = f'{hour}:{minute}'

    return src_dst_time


def store_tweets(cancellations):
    ########## sqlite
    ### connect to sqlite database or create it if it doesn't exist
    conn = sqlite3.connect('gtfs.db', isolation_level=None)
    cur = conn.cursor()
    
    # check if table exists
    cur.execute('''CREATE TABLE IF NOT EXISTS bus_cancellations (
        tweet_id TEXT, 
        affected_route TEXT, 
        conditions TEXT, 
        create_time TEXT, 
        destination TEXT,
        destination_time TEXT,
        message TEXT,
        next_trip TEXT,
        route_short_name TEXT,
        source TEXT,
        source_time TEXT,
        temperature TEXT,
        title TEXT
        )''')
    
    for cancellation in cancellations:
        try:
            cur.execute(f"""SELECT COUNT(*) FROM bus_cancellations WHERE tweet_id = '{cancellation['tweet_id']}'""")
            row = cur.fetchone()
            counter = row[0]
            if counter == 0:
                # insert new record if tweet_id is not found
                sql = f'''INSERT INTO bus_cancellations VALUES (
                    "{cancellation['tweet_id']}",
                    "{cancellation['affected_route']}",
                    "{cancellation['conditions']}",
                    "{cancellation['create_time']}",
                    "{cancellation['destination']}",
                    "{cancellation['destination_time']}",
                    "{cancellation['message']}",
                    "{cancellation['next_trip']}",
                    "{cancellation['route_short_name']}",
                    "{cancellation['source']}",
                    "{cancellation['source_time']}",
                    "{cancellation['temperature']}",
                    "{cancellation['title']}"
                    )'''
                cur.execute(sql)
        except sqlite3.Error:
            pass

    ### close database connection
    cur.close()
    conn.close()


def read_tweets():
    ########## sqlite
    ### connect to sqlite database or create it if it doesn't exist
    conn = sqlite3.connect('gtfs.db', isolation_level=None)
    cur = conn.cursor()

    cur.execute(f"""SELECT * FROM bus_cancellations 
        ORDER BY create_time DESC 
        """)
    rows = cur.fetchall()

    cancellations = []
    for row in rows:
        cancellation = {
            'tweet_id': row[0],
            'affected_route': row[1],
            'conditions': row[2],
            'create_time': row[3],
            'destination': row[4],
            'destination_time': row[5],
            'message': row[6],
            'next_trip': row[7],
            'route_short_name': row[8],
            'source': row[9],
            'source_time': row[10],
            'temperature': row[11],
            'title': row[12]
        }
        cancellations.append(cancellation)
    
    ### close database connection
    cur.close()
    conn.close()
    
    return cancellations


def read_cancellations():
    ########## sqlite
    ### connect to sqlite database or create it if it doesn't exist
    conn = sqlite3.connect('gtfs.db', isolation_level=None)
    cur = conn.cursor()

    cur.execute(f"""SELECT * FROM bus_cancellations 
        ORDER BY create_time DESC 
        """)
    rows = cur.fetchall()

    cancellations = []
    for row in rows:
        cancellation = {
            'tweet_id': row[0],
            'affected_route': row[1],
            'conditions': row[2],
            'create_time': (datetime.datetime.fromisoformat(row[3]) - datetime.timedelta(hours=5)).isoformat(),
            'destination': row[4],
            'destination_time': row[5],
            'message': row[6],
            'next_trip': row[7],
            'route_short_name': row[8],
            'source': row[9],
            'source_time': row[10],
            'temperature': row[11],
            'title': row[12]
        }
        cancellations.append(cancellation)

    print(f'correlating tweet data to GTFS data...', end='')
    for cancellation in cancellations:
        ########################################
        ### search for source stop
        src_stop_name = cancellation['source']
        ### find ’ character: codepoint 8217
        ### 2019;RIGHT SINGLE QUOTATION MARK;Pf;0;ON;;;;;N;SINGLE COMMA QUOTATION MARK;;;;
        if src_stop_name.find(chr(8217)) >= 0:
            src_stop_name = src_stop_name.replace(chr(8217), '%')
        ### find ' character: codepoint 39
        ### 0027;APOSTROPHE;Po;0;ON;;;;;N;APOSTROPHE-QUOTE;;;;
        if src_stop_name.find(chr(39)) >= 0:
            src_stop_name = src_stop_name.replace(chr(39), '%')
        ### find / character:
        if src_stop_name.find('/') < 0:
            src_stop_name = src_stop_name.strip().replace(' ', '%')
            sql_src_stop_name = f'stops.stop_name LIKE "%{src_stop_name}%" '
        else:
            m = re.search('/', src_stop_name)
            first_part = src_stop_name[:m.start()].strip().replace(' ', '%')
            second_part = src_stop_name[m.end():].strip().replace(' ', '%')
            sql_src_stop_name = f'(stops.stop_name LIKE "%{first_part}%" OR stops.stop_name LIKE "%{second_part}%") '

        create_time = datetime.datetime.fromisoformat(cancellation['create_time'])
        weekday = create_time.strftime('%A').lower()
        # date = time_posted.strftime('%Y-%m-%d')
        sql = f'''SELECT min(abs(julianday(stop_times.arrival_time) - julianday("{cancellation['source_time']}"))), 
            routes.route_id, trips.trip_id, trips.service_id, 
            julianday("{cancellation['create_time']}") as julianday_cancellation_date, 
            calendar.start_date, julianday(calendar.start_date) as julian_start_date, 
            calendar.end_date, julianday(calendar.end_date) as julian_end_date, 
            stop_times.arrival_time, stop_times.departure_time, stop_times.stop_sequence, stop_times.stop_id, 
            stops.stop_name, stops.stop_lat, stops.stop_lon 
            FROM trips 
            INNER JOIN calendar ON trips.service_id = calendar.service_id 
            INNER JOIN routes ON trips.route_id = routes.route_id
            INNER JOIN stop_times ON trips.trip_id = stop_times.trip_id
            INNER JOIN stops ON stop_times.stop_id = stops.stop_id 
            WHERE calendar.{weekday} = 1 
            AND routes.route_short_name = "{cancellation['route_short_name']}" 
            AND julianday_cancellation_date >= julian_start_date 
            AND julianday_cancellation_date <= julian_end_date 
			AND stop_times.stop_id IN (
				SELECT stop_id 
				FROM stops 
				WHERE {sql_src_stop_name})
            '''
            # '''
            # AND stop_times.stop_sequence = (SELECT min(stop_times.stop_sequence) 
            #                                 FROM trips 
            #                                 INNER JOIN calendar ON trips.service_id = calendar.service_id 
            #                                 INNER JOIN routes ON trips.route_id = routes.route_id
            #                                 INNER JOIN stop_times ON trips.trip_id = stop_times.trip_id
            #                                 INNER JOIN stops ON stop_times.stop_id = stops.stop_id 
            #                                 WHERE calendar.{weekday} = 1 
            #                                 AND routes.route_short_name = "{cancellation['route_short_name']}" 
            #                                 AND {sql_src_stop_name}) 
            # '''
        # print(sql)
        cur.execute(sql)
        rows = cur.fetchall()
        if len(rows) > 1:
            print(f'*** more than 1 matches {len(rows)}')
            print(sql)
        elif len(rows) == 1:
            row = rows[0]
            if row[0] is None:
                print('*** no match ***')
                print(sql)
            cancellation['diff'] = row[0]
            cancellation['route_id'] = row[1]
            cancellation['trip_id'] = row[2]
            cancellation['service_id'] = row[3]
            cancellation['cancellation_date'] = row[4]
            cancellation['start_date'] = row[5]
            cancellation['julian_start_date'] = row[6]
            cancellation['end_date'] = row[7]
            cancellation['julian_end_date'] = row[8]
            cancellation['src_arrival_time'] = row[9]
            cancellation['src_departure_time'] = row[10]
            cancellation['src_stop_sequence'] = row[11]
            cancellation['src_stop_id'] = row[12]
            cancellation['src_stop_name'] = row[13]
            cancellation['src_stop_lat'] = row[14]
            cancellation['src_stop_lon'] = row[15]
            
        ########################################
        ### search for destination stop
        dst_stop_name = cancellation['destination']
        ### find ’ character: codepoint 8217
        ### 2019;RIGHT SINGLE QUOTATION MARK;Pf;0;ON;;;;;N;SINGLE COMMA QUOTATION MARK;;;;
        if dst_stop_name.find(chr(8217)) >= 0:
            dst_stop_name = dst_stop_name.replace(chr(8217), '%')
        ### find ' character: codepoint 39
        ### 0027;APOSTROPHE;Po;0;ON;;;;;N;APOSTROPHE-QUOTE;;;;
        if dst_stop_name.find(chr(39)) >= 0:
            dst_stop_name = dst_stop_name.replace(chr(39), '%')
        ### find / character:
        if dst_stop_name.find('/') < 0:
            dst_stop_name = dst_stop_name.strip().replace(' ', '%')
            sql_dst_stop_name = f'stops.stop_name LIKE "%{dst_stop_name}%" '
        else:
            m = re.search('/', dst_stop_name)
            #first_part = dst_stop_name[:m.start()].strip().replace(' ', '%')
            second_part = dst_stop_name[m.end():].strip().replace(' ', '%')
            #sql_dst_stop_name = f'(stops.stop_name LIKE "%{first_part}%" OR stops.stop_name LIKE "%{second_part}%") '
            sql_dst_stop_name = f'(stops.stop_name LIKE "%{second_part}%") '
        create_time = datetime.datetime.fromisoformat(cancellation['create_time'])
        weekday = create_time.strftime('%A').lower()
        # date = time_posted.strftime('%Y-%m-%d')
        sql = f'''SELECT min(abs(julianday(stop_times.arrival_time) - julianday("{cancellation['destination_time']}"))), 
            routes.route_id, trips.trip_id, trips.service_id, 
            julianday("{cancellation['create_time']}") as julianday_cancellation_date, 
            calendar.start_date, julianday(calendar.start_date) as julian_start_date, 
            calendar.end_date, julianday(calendar.end_date) as julian_end_date, 
            stop_times.arrival_time, stop_times.departure_time, stop_times.stop_sequence, stop_times.stop_id, 
            stops.stop_name, stops.stop_lat, stops.stop_lon 
            FROM trips 
            INNER JOIN calendar ON trips.service_id = calendar.service_id 
            INNER JOIN routes ON trips.route_id = routes.route_id
            INNER JOIN stop_times ON trips.trip_id = stop_times.trip_id
            INNER JOIN stops ON stop_times.stop_id = stops.stop_id 
            WHERE calendar.{weekday} = 1 
            AND routes.route_short_name = "{cancellation['route_short_name']}" 
            AND julianday_cancellation_date >= julian_start_date 
            AND julianday_cancellation_date <= julian_end_date 
			AND stop_times.stop_id IN (
				SELECT stop_id 
				FROM stops 
				WHERE {sql_src_stop_name})
            '''
            # '''
            # AND stop_times.stop_sequence = (SELECT max(stop_times.stop_sequence) 
            #                                 FROM trips 
            #                                 INNER JOIN calendar ON trips.service_id = calendar.service_id 
            #                                 INNER JOIN routes ON trips.route_id = routes.route_id
            #                                 INNER JOIN stop_times ON trips.trip_id = stop_times.trip_id
            #                                 INNER JOIN stops ON stop_times.stop_id = stops.stop_id 
            #                                 WHERE calendar.{weekday} = 1 
            #                                 AND routes.route_short_name = "{cancellation['route_short_name']}" 
            #                                 AND {sql_dst_stop_name}) 
            # '''
        # print(sql)
        cur.execute(sql)
        rows = cur.fetchall()
        if len(rows) > 1:
            print(f'*** more than 1 matches {len(rows)}')
            print(sql)
        elif len(rows) == 1:
            row = rows[0]
            if row[0] is None:
                print('*** no match ***')
                print(sql)
            cancellation['dst_arrival_time'] = row[9]
            cancellation['dst_departure_time'] = row[10]
            cancellation['dst_stop_sequence'] = row[11]
            cancellation['dst_stop_id'] = row[12]
            cancellation['dst_stop_name'] = row[13]
            cancellation['dst_stop_lat'] = row[14]
            cancellation['dst_stop_lon'] = row[15]
        print('.', end='')
            
    
    ### close database connection
    cur.close()
    conn.close()
    
    return cancellations


def get_stop_list(cancellations):
    stop_list = []
    ########## sqlite
    ### connect to sqlite database or create it if it doesn't exist
    conn = sqlite3.connect('gtfs.db', isolation_level=None)
    cur = conn.cursor()

    ### structure of cancellations
    # [{
    #     'tweet_id': row[0],
    #     'affected_route': row[1],
    #     'conditions': row[2],
    #     'create_time': row[3],
    #     'destination': row[4],
    #     'destination_time': row[5],
    #     'message': row[6],
    #     'next_trip': row[7],
    #     'route_short_name': row[8],
    #     'source': row[9],
    #     'source_time': row[10],
    #     'temperature': row[11],
    #     'title': row[12]
    #     'diff', 'route_id', 'trip_id', 'service_id', 
    #     'cancellation_date', 'start_date', 'julian_start_date', 'end_date', 'julian_end_date', 
    #     'src_arrival_time', 'src_departure_time', 'src_stop_sequence', 'src_stop_id', 'src_stop_name', 'src_stop_lat', 'src_stop_lon', 
    #     'dst_arrival_time', 'dst_departure_time', 'dst_stop_sequence', 'dst_stop_id', 'dst_stop_name', 'dst_stop_lat', 'dst_stop_lon'
    # }]
    for cencellation in cancellations:
        src_seq = cencellation['src_stop_sequence']
        dst_seq = cencellation['dst_stop_sequence']
        trip_id = cencellation['trip_id']

        ### search for intermediate stops if src_seq and dst_seq are not None
        if src_seq != None and dst_seq != None:
            sql = f'''SELECT stop_times.trip_id, stop_times.stop_sequence, stops.stop_name, stops.stop_lat, stops.stop_lon 
                FROM stop_times 
                INNER JOIN stops ON stop_times.stop_id = stops.stop_id 
                WHERE stop_times.trip_id = "{trip_id}" 
                AND (stop_times.stop_sequence >= {src_seq} AND stop_times.stop_sequence <= {dst_seq}) 
                '''
            print(sql)
            cur.execute(sql)
            rows = cur.fetchall()  
            for row in rows:
                stop = {
                    'tweet_id': cencellation['tweet_id'],
                    'trip_id': row[0],
                    'stop_sequence': row[1],
                    'stop_name': row[2],
                    'stop_lat': row[3],
                    'stop_lon': row[4]
                }
                stop_list.append(stop)
    
    ### close database connection
    cur.close()
    conn.close()
    
    return stop_list
