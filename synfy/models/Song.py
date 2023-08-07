import eyed3


class Song:
    def __init__(self, song_path):
        self.song_path = song_path
        self.artist, self.title, self.genre, self.key, self.bpm = self.read_song_tags()

    def read_song_tags(self):
        eyed3.log.setLevel("ERROR")
        audiofile = eyed3.load(self.song_path)
        key = None
        if audiofile.tag is None:
            print("Le fichier n'a pas de tag MP3.")
            return None, None, None, None, None
        else:
            try:
                for frame in audiofile.tag.frameiter(["TKEY"]):
                    key = frame.text
                    if key is not None:
                        break
            except:
                print("Failed reading TKEY")
            return audiofile.tag.artist, audiofile.tag.title, audiofile.tag.genre, key, audiofile.tag.bpm
