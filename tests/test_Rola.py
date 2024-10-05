from src.Rola import *
from src.Minero import *

def test_case():
    builder = RolaBuilder()
    rola = (builder
            .set_id_performer(1)
            .set_id_performer_type(0)  # 0 for person
            .set_id_album(5)
            .set_path("/music/album/track1.mp3")
            .set_title("Awesome Song")
            .set_track(1)
            .set_year(2023)
            .set_genre("Rock")
            .build())

    print(rola)
