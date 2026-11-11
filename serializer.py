import json
import xml.etree.ElementTree as et
from dataclasses import dataclass, asdict

@dataclass
class Song:
    song_id: str
    title: str
    artist: str


def serialize(song, data_format):
    serializer_product = _get_serializer(data_format)
    return str(serializer_product(song))

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
    def __init__(self):
        self._current_object = None

    def start_object(self, object_name, object_id):
        self._current_object = {'id': object_id}

    def add_property(self, name, value):
        self._current_object[name] = value

    def __str__(self):
        return json.dumps(self._current_object)

class _XMLSerializer:
    def __init__(self):
        self._element = None

    def start_object(self, object_name, object_id):
        self._element = et.Element(object_name, attrib={'id': object_id})

    def add_property(self, name, value):
        prop = et.SubElement(self._element, name)
        prop.text = value

    def __str__(self):
        return et.tostring(self._element, encoding='unicode')