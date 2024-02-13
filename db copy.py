import code
from flask_sqlalchemy import SQLAlchemy

import base64
import boto3
import datetime
import io
from io import BytesIO
from mimetypes import guess_extension, guess_type
import os
from PIL import Image
import random
import re
import string

import hashlib

from sqlalchemy import ForeignKey
import bcrypt

db = SQLAlchemy()

# create tables 
class User(db.Model):
    """
    User model 

    Many-to-one relationship with Plant table. Multiple Users can be associated with One Plant
    Delete associated Users if Plant is deleted.
    """

class Plant(db.Model):
    """
    Plant model 

    One-to-many relationship with User table. One Plant can be associated with Multiple Users.
    """

class Configuration(db.Model):
    """
    Configuration Model 

    One-to-one relationship with Plant table. 
    Multiple Users can change these values and we use just use the most updated values.
    
    """


# create models/dbs