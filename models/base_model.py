#!/usr/bin/python3
"""
base_model.py
Module that defines the BaseModel class.
"""
import uuid
from datetime import datetime
from models import storage  # Import the storage instance

class BaseModel:
    """
    Defines all common attributes/methods for other classes.
    """

    def __init__(self, *args, **kwargs):
        """
        Initializes a new instance of BaseModel.
        If kwargs is not empty, initializes attributes with kwargs;
        otherwise, creates id and created_at as a new instance.
        """
        if kwargs:
            for key, value in kwargs.items():
                if key == '__class__':
                    continue
                elif key in ['created_at', 'updated_at']:
                    # Convert string datetime to datetime object
                    setattr(self, key, datetime.fromisoformat(value))
                else:
                    setattr(self, key, value)
        else:
            self.id = str(uuid.uuid4())  # Generate a new UUID
            self.created_at = self.updated_at = datetime.now()
            storage.new(self)  # Add the new instance to storage

    def __str__(self):
        """
        Returns a string representation of the BaseModel instance.
        """
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"

    def save(self):
        """
        Updates 'updated_at' with the current datetime and saves the instance to storage.
        """
        self.updated_at = datetime.now()
        storage.new(self)  # Ensure the instance is in the storage's object dictionary
        storage.save()  # Serialize the storage's object dictionary to the JSON file

    def to_dict(self):
        """
        Returns a dictionary containing all keys/values of the instance,
        including the key '__class__' with the class name of the object.
        """
        dict_copy = self.__dict__.copy()
        dict_copy['__class__'] = self.__class__.__name__
        # Convert datetime objects to strings
        dict_copy['created_at'] = self.created_at.isoformat()
        dict_copy['updated_at'] = self.updated_at.isoformat()
        return dict_copy
