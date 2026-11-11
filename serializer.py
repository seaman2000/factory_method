import json
import xml.etree.ElementTree as et


class Song:
    def __init__(self, song_id, title, artist):
        self.song_id = song_id
        self.title = title
        self.artist = artist


def serialize(song, data_format):
    serializer_product = _get_serializer(data_format)
    return serializer_product(song)

# Creator
def _get_serializer(data_format):
    if data_format == "JSON":
        return _JSONSerializer
    elif data_format == "XML":
        return _XMLSerializer
    else:
        raise ValueError(data_format)

# Products
class _JSONSerializer:
    def __init__(self, song):
        self.song = song

    def __str__(self):
        return json.dumps({'id': self.song.song_id,
                           'title': self.song.title,
                           'artist': self.song.artist})

class _XMLSerializer:
    def __init__(self, song):
        self.song_info = et.Element('song', attrib={'id': song.song_id})
        self.title = et.SubElement(self.song_info, 'title')
        self.title.text = song.title
        self.artist = et.SubElement(self.song_info, 'artist')
        self.artist.text = song.artist
    def __str__(self):
        return et.tostring(self.song_info, encoding='unicode')