# DROP TABLES

songplay_table_drop = "DROP TABLE IF EXISTS songplays;"
user_table_drop = "DROP TABLE IF EXISTS users;"
song_table_drop = "DROP TABLE IF EXISTS songs;"
artist_table_drop = "DROP TABLE IF EXISTS artists;"
time_table_drop = "DROP TABLE IF EXISTS time"

# CREATE TABLES

# Fact Table

songplay_table_create = ("""CREATE TABLE IF NOT EXISTS songplays (
    id SERIAL PRIMARY KEY, 
    start_time timestamp, 
    user_level varchar(50),
    song_id varchar(18), 
    song_name varchar(200),
    artist_name varchar(200),
    artist_id varchar(18), 
    session_id varchar(100), 
    location varchar(300), 
    user_agent varchar(100)
)
""")

# Dimensions Tables
user_table_create = ("""
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    user_id varchar(18), 
    first_name varchar(100), 
    last_name varchar(100), 
    gender varchar(2), 
    user_level varchar(100)
)
""")

song_table_create = ("""
CREATE TABLE IF NOT EXISTS songs (
    id SERIAL PRIMARY KEY,
    song_id varchar(20), 
    title varchar(200), 
    artist_id varchar(18), 
    album_year integer, 
    duration numeric(10,5)
)
""")

artist_table_create = ("""
CREATE TABLE IF NOT EXISTS artists (
    id SERIAL PRIMARY KEY,
    artist_id varchar(18), 
    artist_name varchar(200), 
    location varchar(300), 
    latitude numeric(10,5), 
    longitude numeric(10,5)
)
""")

time_table_create = ("""
CREATE TABLE IF NOT EXISTS time (
    id SERIAL PRIMARY KEY,
    start_time date, 
    play_hour integer, 
    play_day integer, 
    play_week integer, 
    play_month integer, 
    play_year integer, 
    weekday integer
)
""")

# INSERT RECORDS

songplay_table_insert = ("""INSERT INTO songplays (start_time, user_level, session_id, user_agent, location,
    artist_name, song_name)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
""")

user_table_insert = ("""INSERT INTO users (user_id, first_name, last_name, gender, user_level)
    VALUES (%s, %s, %s, %s, %s)
""")

song_table_insert = ("""INSERT INTO songs (song_id, title, artist_id, album_year, duration)
    VALUES (%s, %s, %s, %s, %s)
""")

artist_table_insert = ("""INSERT INTO artists (artist_id, artist_name, location, latitude, longitude)
    VALUES (%s, %s, %s, %s, %s)
""")

time_table_insert = ("""INSERT INTO time (start_time, play_hour, play_day, play_week, play_month, play_year, weekday)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
""")

# FIND SONGS

song_select = ("""UPDATE songplays
SET (song_id, artist_id) = (songs.song_id, songs.artist_id)
FROM songs
WHERE songs.title = songplays.song_name;
""")

# QUERY LISTS
create_table_queries = [songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]