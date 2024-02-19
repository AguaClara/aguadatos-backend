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

class RawWaterEntry(db.Model):
    """
    Raw Water Entry Model 

    Many-to-one relationship with User model. Many Raw Water Entries can be associated with one User. 
    Do not delete associated Raw Water Entries if User is deleted. 
    """

class DosageEntry(db.Model):
    """
    Dosage Entry Model 

    Many-to-one relationship with User model. Many Dosage Entries can be associated with one User. 
    Do not delete associated Dosage Entries if User is deleted. 

    Other optional relations: CalibrationSection, ChangeDoseSection
    """

class CalibrationSection(db.Model): 
    """
    Calibration Section Model 

    One-to-One relationship with DosageEntry model. 
    """

class ChangeDoseSection(db.Model):
    """
    Change Dose Section Model 

    One-to-One relationship with DosageEntry model. 
    One-to-One relationship with CalibrationSection model. 
    """

class TankVolumeSection(db.Model):
    """
    Tank Volume Section Model

    Many-to-One relationship with DosageEntry model. 
    """

class ClarifiedEntry(db.Model):
    """
    Clarified Entry Model

    Many-to-One relationship with Plant model.
    Many-to-One relationship withe User model. 
    """

class ClarifierSection(db.Model):
    """
    Clarifier Section Model

    Many-to-One relationship with ClarifiedEntry model. 
    """

class FiltersEntry(db.Model):
    """
    Filters Entry Model

    Many-to-One relationship with Plant model.
    Many-to-One relationship with User model. 
    """

class FilterSection(db.Model):
    """
    Filter Section Model 

    Many-to-One relationship with FiltersEntry model. 
    """

class PostTreatmentEntry(db.Model):
    """
    Post Treatment Entry Model

    Many-to-One relationship with User model. 
    """

class FeedbackEntry(db.Model):
    """
    Feedback Entry Model

    Many-to-One relationship with User model. 
    """