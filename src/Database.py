import sqlite3
import os
from src.Rola import *

class MusicLibraryDB:
    def __init__(self, db_name='biblioteca.db'):
        self.conn = sqlite3.connect(db_name)
        self.conn.execute('PRAGMA foreign_keys = ON')
        self.cursor = self.conn.cursor()
        self.deploy()

    def add_performer(self, id_type, name):
        self.cursor.execute('''
            INSERT INTO performers (id_type, name)
            VALUES (?, ?)
        ''', (id_type, name))
        self.conn.commit()

    def add_album(self, path, name, year):
        self.cursor.execute('''
            INSERT INTO albums (path, name, year)
            VALUES (?, ?, ?)
        ''', (path, name, year))
        self.conn.commit()

    def add_rola(self, id_performer, id_album, path, title, track, year, genre):
        self.cursor.execute('''
            INSERT INTO rolas (id_performer, id_album, path, title, track, year, genre)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (id_performer, id_album, path, title, track, year, genre))
        self.conn.commit()

    def add_person(self, stage_name, real_name, birth_date, death_date=None):
        self.cursor.execute('''
            INSERT INTO persons (stage_name, real_name, birth_date, death_date)
            VALUES (?, ?, ?, ?)
        ''', (stage_name, real_name, birth_date, death_date))
        self.conn.commit()

    def add_group(self, name, start_date, end_date=None):
        self.cursor.execute('''
            INSERT INTO groups (name, start_date, end_date)
            VALUES (?, ?, ?)
        ''', (name, start_date, end_date))
        self.conn.commit()

    def add_in_group(self, id_person, id_group):
        self.cursor.execute('''
            INSERT INTO in_group (id_person, id_group)
            VALUES (?, ?)
        ''', (id_person, id_group))
        self.conn.commit()

    def close(self):
        self.conn.close()

    def add_song(self, performer, album, path, title, track, year, genre):
        conn = self.conn
        cursor = self.cursor

        id_performer = self.insert_performer_if_not_exists(2, performer)
        id_album = self.insert_album_if_not_exists(path, album, year) 

        cursor.execute('INSERT INTO rolas (id_performer, id_album, path, title, track, year, genre) '
                    'VALUES (?, ?, ?, ?, ?, ?, ?)', 
                    (id_performer, id_album, path, title, track, year, genre))

        conn.commit()
        
        RB = RolaBuilder()
        RB.set_album(album)
        RB.set_genre(genre)
        RB.set_id_album(id_album)
        RB.set_id_performer(id_performer)
        RB.set_path(path)
        RB.set_performer(performer)
        RB.set_title(title)
        RB.set_track(track)
        RB.set_year(year)
        return RB.build()


    # Function to insert into performers table only if the performer doesn't exist, return id_performer
    def insert_performer_if_not_exists(self, performer_type, performer_name):
        # Check if performer already exists
        cursor = self.cursor
        cursor.execute('SELECT id_performer FROM performers WHERE name = ?', (performer_name,))
        result = cursor.fetchone()

        if result:
            return result[0]  # Return existing id_performer

        # Insert performer if not exists
        cursor.execute('INSERT INTO performers (id_type, name) VALUES (?, ?)', (performer_type, performer_name))
        return cursor.lastrowid  # Return new id_performer

    # Function to insert into albums table only if the album doesn't exist, return id_album
    def insert_album_if_not_exists(self, filepath, album_name, album_year):
        # Check if album already exists
        album_path = os.path.dirname(filepath)
        cursor = self.cursor
        cursor.execute('SELECT id_album FROM albums WHERE path = ? AND name = ? AND year = ?', 
                    (album_path, album_name, album_year))
        result = cursor.fetchone()

        if result:
            return result[0]  # Return existing id_album

        # Insert album if not exists
        cursor.execute('INSERT INTO albums (path, name, year) VALUES (?, ?, ?)', 
                    (album_path, album_name, album_year))
        return cursor.lastrowid  # Return new id_album

    def deploy(self):
        """
        Check if the database is defined correctly.
        If not, deploy the schema.
        
        :param conn: sqlite3.Connection object
        """
        try:
            cursor = self.cursor
            cursor.execute("SELECT * FROM sqlite_master WHERE type='table' AND name='types';")
            table_exists = cursor.fetchone()

            if table_exists is None:
                print("Table does not exist. Deploying schema...")
                self.deploy_schema()
            else:
                print("Database already deployed")
        
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")


    # Function to deploy the schema
    def deploy_schema(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS types (
                id_type       INTEGER PRIMARY KEY,
                description   TEXT
            )
        ''')

        self.cursor.executemany('''
        INSERT OR IGNORE INTO types (id_type, description)
        VALUES (?, ?)
        ''', [
            (0, 'Person'),
            (1, 'Group'),
            (2, 'Unknown')
        ])

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS performers (
                id_performer  INTEGER PRIMARY KEY,
                id_type       INTEGER,
                name          TEXT,
                FOREIGN KEY   (id_type) REFERENCES types(id_type)
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS persons (
                id_person     INTEGER PRIMARY KEY,
                stage_name    TEXT,
                real_name     TEXT,
                birth_date    TEXT,
                death_date    TEXT
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS groups (
                id_group      INTEGER PRIMARY KEY,
                name          TEXT,
                start_date    TEXT,
                end_date      TEXT
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS in_group (
                id_person     INTEGER,
                id_group      INTEGER,
                PRIMARY KEY   (id_person, id_group),
                FOREIGN KEY   (id_person) REFERENCES persons(id_person),
                FOREIGN KEY   (id_group) REFERENCES groups(id_group)
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS albums (
                id_album      INTEGER PRIMARY KEY,
                path          TEXT,
                name          TEXT,
                year          INTEGER
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS rolas (
                id_rola       INTEGER PRIMARY KEY,
                id_performer  INTEGER,
                id_album      INTEGER,
                path          TEXT,
                title         TEXT,
                track         INTEGER,
                year          INTEGER,
                genre         TEXT,
                FOREIGN KEY   (id_performer) REFERENCES performers(id_performer),
                FOREIGN KEY   (id_album) REFERENCES albums(id_album)
            )
        ''')

        self.conn.commit()