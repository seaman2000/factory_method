import json
import yaml
import xml.etree.ElementTree as et
from dataclasses import dataclass, asdict
from abc import ABC, abstractmethod


class ClientObjectBlueprint(ABC):

    @abstractmethod
    def use_product(self, product):
        pass

@dataclass
class Song(ClientObjectBlueprint):
    song_id: str
    title: str
    artist: str

    def use_product(self, product):
        product.start_object('song', self.song_id)
        product.add_property('title', self.title)
        product.add_property('artist', self.artist)

@dataclass
class Book(ClientObjectBlueprint):
    book_id: str
    title: str
    author: str
    publisher: str

    def use_product(self, product):
        product.start_object('book', self.book_id)
        product.add_property('title', self.title)
        product.add_property('author', self.author)
        product.add_property('publisher', self.publisher)

def serialize(object_to_serialize, data_format):
    my_product = creator.factory_method(data_format)
    object_to_serialize.use_product(my_product)
    print(creator)
    return str(my_product)

# Creator
class CreatorBlueprint(ABC):

    @abstractmethod
    def factory_method(self, data_format):
        pass

    def register_format(self, data_format, product):
        pass

class SerializerCreator(CreatorBlueprint):
    def __init__(self):
        self.data_format = None
        self._products = dict()

    def register_format(self, data_format, product):
        self._products[data_format] = product

    def factory_method(self, data_format):
        self.data_format = data_format
        product = self._products.get(data_format)
        if not product:
            raise ValueError
        return product()

    def __repr__(self):
        return "Your creator today: Serializer Creator"

    def __str__(self):
        return f"""
        Dear Client,
        
        Thank you for your purchase of:
        Serializer: {self.data_format}
        
        {self.__repr__()}
        
        Your product is below:
        """

# Products
class SerializationProductBlueprint(ABC):

    @abstractmethod
    def start_object(self, object_name, object_id):
        pass

    @abstractmethod
    def add_property(self, name, value):
        pass

class _JSONSerializer(SerializationProductBlueprint):
    def __init__(self):
        self._current_object = None

    def start_object(self, object_name, object_id):
        self._current_object = {'id': object_id}

    def add_property(self, name, value):
        self._current_object[name] = value

    def __str__(self):
        return json.dumps(self._current_object)

class _XMLSerializer(SerializationProductBlueprint):
    def __init__(self):
        self._element = None

    def start_object(self, object_name, object_id):
        self._element = et.Element(object_name, attrib={'id': object_id})

    def add_property(self, name, value):
        prop = et.SubElement(self._element, name)
        prop.text = value

    def __str__(self):
        return et.tostring(self._element, encoding='unicode')

class _YAMLSerializer(_JSONSerializer):
    def __str__(self):
        return yaml.dump(self._current_object)

# Register
creator = SerializerCreator()
creator.register_format("JSON", _JSONSerializer)
creator.register_format("XML", _XMLSerializer)
creator.register_format("YAML", _YAMLSerializer)
