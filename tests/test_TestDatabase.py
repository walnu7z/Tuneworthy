import pytest
from src.Database import MusicLibraryDB

class TestDatabase:
    @pytest.fixture
    def db(self):
        """Fixture to set up the MusicLibraryDB object before each test."""
        db_instance = MusicLibraryDB()  
        yield db_instance
        db_instance.conn.close()  

    def test_types_table(self, db):
        """Test the existence and structure of the types table."""
        db.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='types'")
        assert db.cursor.fetchone() is not None  # Check if the table exists

        db.cursor.execute("PRAGMA table_info(types)")
        columns = [column[1] for column in db.cursor.fetchall()]
        expected_columns = ['id_type', 'description']
        assert sorted(columns) == sorted(expected_columns)

    def test_performers_table(self, db):
        """Test the existence and structure of the performers table."""
        db.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='performers'")
        assert db.cursor.fetchone() is not None  # Check if the table exists

        db.cursor.execute("PRAGMA table_info(performers)")
        columns = [column[1] for column in db.cursor.fetchall()]
        expected_columns = ['id_performer', 'id_type', 'name']
        assert sorted(columns) == sorted(expected_columns)

    def test_persons_table(self, db):
        """Test the existence and structure of the persons table."""
        db.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='persons'")
        assert db.cursor.fetchone() is not None  # Check if the table exists

        db.cursor.execute("PRAGMA table_info(persons)")
        columns = [column[1] for column in db.cursor.fetchall()]
        expected_columns = ['id_person', 'stage_name', 'real_name', 'birth_date', 'death_date']
        assert sorted(columns) == sorted(expected_columns)

    def test_groups_table(self, db):
        """Test the existence and structure of the groups table."""
        db.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='groups'")
        assert db.cursor.fetchone() is not None  # Check if the table exists

        db.cursor.execute("PRAGMA table_info(groups)")
        columns = [column[1] for column in db.cursor.fetchall()]
        expected_columns = ['id_group', 'name', 'start_date', 'end_date']
        assert sorted(columns) == sorted(expected_columns)

    def test_in_group_table(self, db):
        """Test the existence and structure of the in_group table."""
        db.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='in_group'")
        assert db.cursor.fetchone() is not None  # Check if the table exists

        db.cursor.execute("PRAGMA table_info(in_group)")
        columns = [column[1] for column in db.cursor.fetchall()]
        expected_columns = ['id_person', 'id_group']
        assert sorted(columns) == sorted(expected_columns)

    def test_albums_table(self, db):
        """Test the existence and structure of the albums table."""
        db.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='albums'")
        assert db.cursor.fetchone() is not None  # Check if the table exists

        db.cursor.execute("PRAGMA table_info(albums)")
        columns = [column[1] for column in db.cursor.fetchall()]
        expected_columns = ['id_album', 'path', 'name', 'year']
        assert sorted(columns) == sorted(expected_columns)

    def test_rolas_table(self, db):
        """Test the existence and structure of the rolas table."""
        db.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='rolas'")
        assert db.cursor.fetchone() is not None  # Check if the table exists

        db.cursor.execute("PRAGMA table_info(rolas)")
        columns = [column[1] for column in db.cursor.fetchall()]
        expected_columns = ['id_rola', 'id_performer', 'id_album', 'path', 'title', 'track', 'year', 'genre']
        assert sorted(columns) == sorted(expected_columns)
