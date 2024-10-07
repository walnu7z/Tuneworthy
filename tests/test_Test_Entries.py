import pytest
from src.Minero import * 


class TestEntries:
    @pytest.fixture
    def minero(self):
        """Fixture to set up the Minero object before each test."""
        miner = Minero()
        yield miner
        miner.close_DB()

    @pytest.fixture
    def song_info(self):
        """Fixture to store song information in an object."""
        class Song:
            def __init__(self, path, performer, title, album, year, genre, track):
                self.PATH = path
                self.TPE1 = performer
                self.TIT2 = title
                self.TALB = album
                self.TDRC = year
                self.TCON = genre
                self.TRCK = track

        # Example songs
        return [
            Song(
                path="path/to/strokes/album",
                performer="The Strokes",
                title="Last Nite",
                album="Is This It",
                year=2001,
                genre="Garage Rock",
                track=2
            ),
            Song(
                path="path/to/julian-casablancas/album",
                performer="Julian Casablancas",
                title="11th Dimension",
                album="Phrazes for the Young",
                year=2009,
                genre="Alternative/Indie",
                track=1
            )
        ]

    def test_add_performer_entry(self, minero: Minero):
        """Test adding a performer entry."""
        performer_name = "The Strokes"
        performer_type = 2  

        # Add performer to the database
        minero.db.insert_performer_if_not_exists(performer_type, performer_name)

        # Verify the performer was added
        minero.db.cursor.execute("SELECT * FROM performers WHERE name = ?", (performer_name,))
        performer = minero.db.cursor.fetchone()
        assert performer is not None
        assert performer[1] == performer_type  # Check id_type


    def test_add_album_entry(self, minero : Minero):
        """Test adding an album entry."""
        album_name = "Is This It"
        album_path = "path/to/strokes/album"
        album_year = 2001

        # Add album to the database
        minero.db.insert_album_if_not_exists(album_path, album_name, album_year)

        # Verify the album was added
        minero.db.cursor.execute("SELECT * FROM albums WHERE name = ?", (album_name,))
        album = minero.db.cursor.fetchone()
        assert album is not None
        assert album[1] == album_path  # Check path
        assert album[3] == album_year  # Check year

    def test_add_rola_entry(self, minero : Minero, song_info):
        """Test adding a rola entry."""
        # Add entries for both songs
        for song in song_info:
            # get id for performer and album before adding the song
            performer_id = minero.db.insert_performer_if_not_exists(2, song.TPE1)  # Assuming type ID is 1 for simplicity
            album_id = minero.db.insert_album_if_not_exists(song.PATH, song.TALB, song.TDRC)

            # Prepare the Mena object for the song
            rola_song = Mena(
                PATH=song.PATH,
                TPE1=song.TPE1,
                TIT2=song.TIT2,
                TALB=song.TALB,
                TDRC=song.TDRC,
                TCON=song.TCON,
                TRCK=song.TRCK
            )

            # Add Rola to the database using the Mena Class
            minero.add_song_from_mena(rola_song)

            # Verify the Rola was added
            minero.db.cursor.execute("SELECT * FROM rolas WHERE title = ?", (song.TIT2,))
            rola = minero.db.cursor.fetchone()
            assert rola is not None
            assert rola[1] == performer_id  # Check id_performer based on the performer ID
            assert rola[2] == album_id  # Check id_album based on the album ID
            assert rola[3] == song.PATH  # Check path
            assert rola[4] == song.TIT2  # Check title
            assert rola[5] == song.TRCK  # Check track
            assert rola[6] == song.TDRC  # Check year
            assert rola[7] == song.TCON  # Check genre
        