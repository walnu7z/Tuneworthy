class Rola:
    def __init__(self, id_performer, id_performer_type, id_album, path, title, track, year, genre):
        self.id_performer = id_performer
        self.id_performer_type = id_performer_type
        self.id_album = id_album
        self.path = path
        self.title = title
        self.track = track
        self.year = year
        self.genre = genre

    def __str__(self):
        return  f"title:\t\t{self.title}\n"\
                f"performer_id:\t{self.id_performer}\n"\
                f"performer_type:\t{self.id_performer_type}\n"\
                f"album_id:\t{self.id_album}\n"\
                f"path:\t\t{self.path}\n"\
                f"track:\t\t{self.track}\n"\
                f"year:\t\t{self.year}\n"\
                f"genre:\t\t{self.genre}"

class RolaBuilder:
    def __init__(self):
        self._id_performer = None
        self._id_performer_type = None
        self._id_album = None
        self._path = None
        self._title = None
        self._track = None
        self._year = None
        self._genre = None

    def set_id_performer(self, id_performer):
        self._id_performer = id_performer
        return self

    def set_id_performer_type(self, id_performer_type):
        if id_performer_type not in [0, 1, 2]:
            raise ValueError("id_performer_type must be 0 (person), 1 (group), or 2 (unknown)")
        self._id_performer_type = id_performer_type
        return self

    def set_id_album(self, id_album):
        self._id_album = id_album
        return self

    def set_path(self, path):
        self._path = path
        return self

    def set_title(self, title):
        self._title = title
        return self

    def set_track(self, track):
        self._track = track
        return self

    def set_year(self, year):
        self._year = year
        return self

    def set_genre(self, genre):
        self._genre = genre
        return self

    def build(self):
        return Rola(
            id_performer=self._id_performer,
            id_performer_type=self._id_performer_type,
            id_album=self._id_album,
            path=self._path,
            title=self._title,
            track=self._track,
            year=self._year,
            genre=self._genre
        )