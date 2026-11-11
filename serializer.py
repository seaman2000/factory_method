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
        return _serialize_to_json
    elif data_format == "XML":
        return _serialize_to_xml
    else:
        raise ValueError(data_format)

# Products
def _serialize_to_json(song):
    song_info = {'id': song.song_id, 'title': song.title, 'artist': song.artist}
    return json.dumps(song_info)

def _serialize_to_xml(song):
    song_info = et.Element('song', attrib={'id': song.song_id})
    title = et.SubElement(song_info, 'title')
    title.text = song.title
    artist = et.SubElement(song_info, 'artist')
    artist.text = song.artist
    return et.tostring(song_info, encoding='unicode')