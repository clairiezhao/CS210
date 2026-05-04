from mysql.connector import connect, Error
from typing import Tuple, List, Set

def clear_database(mydb):
    """
    Deletes all the rows from all the tables of the database.
    If a table has a foreign key to a parent table, it is deleted before 
    deleting the parent table, otherwise the database system will throw an error. 

    Args:
        mydb: database connection
    """
    cursor = mydb.cursor()
    tables = ["song_genre", "album_genre", "genre", "rating", "user", "song", "album", "artist"]
    cursor.execute("set foreign_key_checks = 0")
    mydb.commit()
    for table in tables:
        cursor.execute(f"truncate table {table}")
    cursor.execute("set foreign_key_checks = 1") 
    mydb.commit()
    
def load_single_songs(mydb, single_songs: List[Tuple[str,Tuple[str, ...],str,str]]) -> Set[Tuple[str,str]]:
    """
    Add single songs to the database. 

    Args:
        mydb: database connection
        
        single_songs: List of single songs to add. Each single song is a tuple of the form:
              (song title, genre names, artist name, release date)
        Genre names is a tuple since a song could belong to multiple genres
        Release date is of the form yyyy-dd-mm
        Example 1 single song: ('S1',('Pop',),'A1','2008-10-01') => here song is of genre Pop
        Example 2 single song: ('S2',('Rock', 'Pop),'A2','2000-02-15') => here song is of genre Rock and Pop

    Returns:
        Set[Tuple[str,str]]: set of (song,artist) for combinations that already exist 
        in the database and were not added (rejected). 
        Set is empty if there are no rejects.
    """
    cursor = mydb.cursor()
    not_added = set()
    add_artist = "insert into artist (name) values (%s)"
    add_song = "insert into song (title, release_date, artist_id) values (%s, %s, %s)"
    add_song_genre = "insert into song_genre values (%s, %s)"
    add_genre = "insert into genre (name) values (%s)"

    song_exists = '''
    select count(*) from song, artist
    where song.title = (%s)
    and artist.name = (%s)
    and song.artist_id = artist.id
    '''
    get_artist_id = "select id from artist where name = (%s)"
    get_genre_id = "select id from genre where name = (%s)"

    for song in single_songs:
        title = song[0]
        genres = song[1]
        artist = song[2]
        date = song[3]
        # Check if the combination (song, artist) exists in song table
        cursor.execute(song_exists, (title, artist))
        if cursor.fetchone()[0] == 0:
            artist_id = 0
            genre_id = 0
            # Check if artist exists
            cursor.execute(get_artist_id, (artist,))
            res = cursor.fetchone()
            if not res:
                # Add artist
                cursor.execute(add_artist, (artist,))
                artist_id = cursor.lastrowid
            else:
                artist_id = res[0]
            # Add song
            cursor.execute(add_song, (title, date, artist_id))
            song_id = cursor.lastrowid
            # Add to song_genre
            for genre in genres:
                # Check if genre exists
                cursor.execute(get_genre_id, (genre,))
                res = cursor.fetchone()
                if not res:
                    # Add genre
                    cursor.execute(add_genre, (genre,))
                    genre_id = cursor.lastrowid
                else:
                    genre_id = res[0]
                cursor.execute(add_song_genre, (song_id, genre_id))
            mydb.commit()
        else:
            not_added.add((title, artist))

    return not_added

def get_most_prolific_individual_artists(mydb, n: int, year_range: Tuple[int,int]) -> List[Tuple[str,int]]:   
    """
    Get the top n most prolific individual artists by number of singles released in a year range. 
    Break ties by alphabetical order of artist name.

    Args:
        mydb: database connection
        n: how many to get
        year_range: tuple, e.g. (2015,2020)

    Returns:
        List[Tuple[str,int]]: list of (artist name, number of songs) tuples.
        If there are fewer than n artists, all of them are returned.
        If there are no artists, an empty list is returned.
    """
    cursor = mydb.cursor()
    top_artists = set()
    query = '''select name, count(*) as songs from artist, song
    where song.album_id is null
    where year(release_date) between (%s) and (%s)
    and song.artist_id = artist.id
    group by artist.id
    order by artist.id desc
    limit (%s)'''
    cursor.execute(query, (year_range[0], year_range[1], n))
    res = cursor.fetchall()
    for row in res:
        top_artists.add(row)
        print(row)
    return top_artists


def get_artists_last_single_in_year(mydb, year: int) -> Set[str]:
    """
    Get all artists who released their last single in the given year.
    
    Args:
        mydb: database connection
        year: year of last release
        
    Returns:
        Set[str]: set of artist names
        If there is no artist with a single released in the given year, an empty set is returned.
    """
    cursor = mydb.cursor()
    top_artists = set()
    query = '''select name, count(*) as songs from artist, song
    where song.album_id is null
    and year(release_date) = (%s)
    and song.artist_id = artist.id
    group by artist.id
    order by artist.id desc'''
    cursor.execute(query, (year,))
    res = cursor.fetchall()
    for row in res:
        top_artists.add(row[0])
    return top_artists
    
def load_albums(mydb, albums: List[Tuple[str,str,str,str,List[str]]]) -> Set[Tuple[str,str]]:
    """
    Add albums to the database. 
    
    Args:
        mydb: database connection
        
        albums: List of albums to add. Each album is a tuple of the form:
              (album title, genre, artist name, release date, list of song titles) 
        Release date is of the form yyyy-dd-mm
        Example album: ('Album1','Jazz','A1','2008-10-01',['s1','s2','s3','s4','s5','s6'])

    Returns:
        Set[Tuple[str,str]: set of (album, artist) combinations that were not added (rejected) 
        because the artist already has an album of the same title.
        Set is empty if there are no rejects.
    """
    pass

def get_top_song_genres(mydb, n: int) -> List[Tuple[str,int]]:
    """
    Get n genres that are most represented in terms of number of songs in that genre.
    Songs include singles as well as songs in albums. 
    
    Args:
        mydb: database connection
        n: number of genres

    Returns:
        List[Tuple[str,int]]: list of tuples (genre,number_of_songs), from most represented to
        least represented genre. If number of genres is less than n, returns all.
        Ties broken by alphabetical order of genre names.
    """

def get_album_and_single_artists(mydb) -> Set[str]:
    """
    Get artists who have released albums as well as singles.

    Args:
        mydb; database connection

    Returns:
        Set[str]: set of artist names
    """
    cursor = mydb.cursor()
    query = """
        SELECT DISTINCT a.name
        FROM artist AS a
        JOIN album AS al
            ON al.artist_id = a.id
        JOIN song AS s
            ON s.artist_id = a.id
        WHERE s.album_id IS NULL
    """
    cursor.execute(query)
    return {row[0] for row in cursor.fetchall()}
    
def load_users(mydb, users: List[str]) -> Set[str]:
    """
    Add users to the database. 

    Args:
        mydb: database connection
        users: list of usernames

    Returns:
        Set[str]: set of all usernames that were not added (rejected) because 
        they are duplicates of existing users.
        Set is empty if there are no rejects.
    """
    pass

def load_song_ratings(mydb, song_ratings: List[Tuple[str,Tuple[str,str],int, str]]) -> Set[Tuple[str,str,str]]:
    """
    Load ratings for songs, which are either singles or songs in albums. 

    Args:
        mydb: database connection
        song_ratings: list of rating tuples of the form:
            (rater, (artist, song), rating, date)
        
        The rater is a username, the (artist,song) tuple refers to the uniquely identifiable song to be rated.
        e.g. ('u1',('a1','song1'),4,'2021-11-18') => u1 is giving a rating of 4 to the (a1,song1) song.

    Returns:
        Set[Tuple[str,str,str]]: set of (username,artist,song) tuples that are rejected, for any of the following
        reasongs:
        (a) username (rater) is not in the database, or
        (b) username is in database but (artist,song) combination is not in the database, or
        (c) username has already rated (artist,song) combination, or
        (d) everything else is legit, but rating is not in range 1..5
        
        An empty set is returned if there are no rejects.  
    """
    pass

def get_most_rated_songs(mydb, year_range: Tuple[int,int], n: int) -> List[Tuple[str,str,int]]:
    """
    Get the top n most rated songs in the given year range (both inclusive), 
    ranked from most rated to least rated. 
    "Most rated" refers to number of ratings, not actual rating scores. 
    Ties are broken in alphabetical order of song title. If the number of rated songs is less
    than n, all rates songs are returned.
    
    Args:
        mydb: database connection
        year_range: range of years, e.g. (2018-2021), during which ratings were given
        n: number of most rated songs

    Returns:
        List[Tuple[str,str,int]: list of (song title, artist name, number of ratings for song)   
    """
    cursor = mydb.cursor()
    query = """
        SELECT s.title, a.name, COUNT(*) AS num_ratings
        FROM rating AS r
        JOIN song AS s
            ON r.song_id = s.id
        JOIN artist AS a
            ON s.artist_id = a.id
        WHERE YEAR(r.date) BETWEEN %s AND %s
        GROUP BY s.id, s.title, a.name
        ORDER BY num_ratings DESC, s.title ASC
        LIMIT %s
    """
    cursor.execute(query, (year_range[0], year_range[1], n))
    return cursor.fetchall()

def get_most_engaged_users(mydb, year_range: Tuple[int,int], n: int) -> List[Tuple[str,int]]:
    """
    Get the top n most engaged users, in terms of number of songs they have rated.
    Break ties by alphabetical order of usernames.

    Args:
        mydb: database connection
        year_range: range of years, e.g. (2018-2021), during which ratings were given
        n: number of users

    Returns:
        List[Tuple[str, int]]: list of (username,number_of_songs_rated) tuples
    """
    cursor = mydb.cursor()
    query = """
        SELECT u.name, COUNT(*) AS num_songs_rated
        FROM rating AS r
        JOIN `user` AS u
            ON r.user_id = u.id
        WHERE YEAR(r.date) BETWEEN %s AND %s
        GROUP BY u.id, u.name
        ORDER BY num_songs_rated DESC, u.name ASC
        LIMIT %s
    """
    cursor.execute(query, (year_range[0], year_range[1], n))
    return cursor.fetchall()

def main():
    try:
        mydb = connect(unix_socket='/run/mysqld/mysqld.sock', database='cxz7_music_db')
        singles = [
        ("Old Town Road", ("Country Rap", "Trap"), "Lil Nas X", "2018-12-03"),
        ("Sunflower", ("Hip Hop", "Pop Rap"), "Post Malone", "2018-10-18"),
        ("Sucker", ("Pop Rock", "Pop"), "Jonas Brothers", "2019-03-01"),
        ("Thank U, Next", ("Pop", "R&B"), "Ariana Grande", "2018-11-03"),
        ("Bad Guy", ("Pop", "Electropop"), "Billie Eilish", "2019-03-29"),
        ("Uptown Funk", ("Funk", "Pop"), "Mark Ronson", "2014-11-10"),
        ("Shallow", ("Pop", "Soundtrack"), "Lady Gaga", "2018-09-27"),
        ("This Is America", ("Hip Hop", "Gospel"), "Childish Gambino", "2018-05-05"),
        ("Happy", ("Pop", "Soul"), "Pharrell Williams", "2013-11-21"),
        ("We Are Never Ever Getting Back Together", ("Pop", "Country Pop"), "Taylor Swift", "2012-08-13"),
        ("Royals", ("Indie Pop", "Electropop"), "Lorde", "2013-03-08"),
        ("Counting Stars", ("Pop Rock", "Folk Pop"), "OneRepublic", "2013-06-14"),
        ("Despacito", ("Reggaeton", "Latin Pop"), "Luis Fonsi", "2017-01-13"),
        ("Blinding Lights", ("Synthwave", "Pop"), "The Weeknd", "2019-11-29"),
        ("Drivers License", ("Pop", "Indie Pop"), "Olivia Rodrigo", "2021-01-08")
        ]
        not_added = load_single_songs(mydb, singles)
        print(not_added)
        artists = get_most_prolific_individual_artists(mydb, (2018, 2020))
        print(artists)
        artists = get_artists_last_single_in_year(mydb, 2018)
        print(artists)
        
    except Error as e:
        print(e)
    

if __name__ == "__main__":
    main()