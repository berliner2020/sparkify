import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *


def process_song_file(cur, filepath):
    # open song file
    df = pd.read_json(path_or_buf=filepath, typ='series')
    df.head(5)

    # insert song record
    song_id = df.values[6]
    title = df.values[7]
    artist_id = df.values[1]
    year = df.values[9]
    duration = df.values[8]

    song_data = (song_id, title, artist_id, year, duration)
    print(song_data[0])
    print('inserting song data into tables')
    print()

    cur.execute(song_table_insert, song_data)
    
    # insert artist record
    artist_id = df.values[1]
    name = df.values[5]
    location = df.values[4]
    latitude = df.values[3]
    longitude = df.values[2]

    artist_data = (artist_id, name, location, latitude, longitude)
    print(artist_data[0])
    print('inserting artist data into tables')
    print()
    cur.execute(artist_table_insert, artist_data)


def process_log_file(cur, filepath):
    # open log file
    df = pd.read_json(path_or_buf=filepath, typ='frame', lines=True)

    # filter by NextSong action
    df.loc[df['page'] == 'NextSong']

    # convert timestamp column to datetime and other transformations
    df['ts'] = pd.to_datetime(df['ts'], unit='ms')
    df['userAgent'] = df['userAgent'].str.strip(to_strip='"')
    df['userAgent'] = df['userAgent'].str.slice(0, 7)
    #df['location'] = df['location'].str.split(pat=',', )[0][0]

    # insert time data records
    df['t_stamp'] = df['ts'].dt.date
    df['t_hour'] = df['ts'].dt.hour
    df['t_day'] = df['ts'].dt.day
    df['t_week_of_year'] = df['ts'].dt.isocalendar().week
    df['t_month'] = df['ts'].dt.month
    df['t_year'] = df['ts'].dt.year
    df['t_weekday'] = df['ts'].dt.dayofweek

    time_df = df.filter(items=['t_stamp', 't_hour', 't_day', 't_week_of_year', 't_month', 't_year', 't_weekday'])

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    print('inserting data into time records')

    # load user table
    user_df = df.filter(items=['userId', 'firstName', 'lastName', 'gender', 'level'])

    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    print('inserting data into user records')

    # insert songplay records
    for index, row in df.iterrows():
        artist = row[0]
        song = row[13]
        level = row[7]
        session_id = row[12]
        start_time = row[15]
        user_agent = row[16]
        location = row[8]

        # # get songid and artistid from song and artist tables
        # cur.execute(song_select, (row.song, row.artist, row.length))
        # results = cur.fetchone()
        #
        # if results:
        #     songid, artistid = results
        # else:
        #     songid, artistid = None, None

        # insert songplay record
        print('inserting data into songplay records')
        songplay_data = (start_time, level, session_id, user_agent, location, artist, song)
        cur.execute(songplay_table_insert, songplay_data)

        # update the songplays table by pulling in the song_id and artist_id from the songs table
        cur.execute(song_select)


def process_data(cur, conn, filepath, func):
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    # connection string
    host = 'localhost'
    dbname = 'sparkifydb'
    user = 'postgres'
    password = 'mysecretpassword'

    # connect to default database
    conn = psycopg2.connect(host=host, dbname=dbname, user=user, password=password)
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()