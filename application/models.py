from sqlalchemy import Column, DateTime, Integer, String, Boolean, ForeignKey, DECIMAL
from sqlalchemy.types import Enum as SQLAlchemyEnum
from datetime import datetime 
from . import db

# For enum values
from enum import Enum

class ChemicalType(Enum):
    PAC = "PAC"
    AL2SO43 = "AL2SO43"

    def toJSON(self):
        return self.value

class TankLabel(Enum):
    A1 = "A1"
    A2 = "A2"
    B1 = "B1"
    B2 = "B2"

# create tables 
class User(db.Model):
    """
    User model 

    Many-to-one relationship with Plant table. Multiple Users can be associated with One Plant
    Delete associated Users if Plant is deleted.
    """
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255),unique=True, nullable=False)
    phone_number = Column(String(15), unique=True, nullable=False)

    # Users/Operators must be associated with only one AguaClara plant 
    plant_id = Column(Integer, ForeignKey("plants.id"), nullable=False)

    def _init_(self, **kwargs):
        """
        Initialize User object/entry
        """
        self.name = kwargs.get("name")
        self.email = kwargs.get("email")
        self.phone_number = kwargs.get("phone_number")
        self.plant_id = kwargs.get("plant_id")
    
    def serialize(self):
        """
        Serializes User object
        """
        plant = Plant.query.filter_by(id=self.plant_id).first()
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "phone_number": self.phone_number, 
            "plant_id": plant.simple_serialize()
        }


class Plant(db.Model):
    """
    Plant model 

    One-to-many relationship with User table. One Plant can be associated with Multiple Users.
    """

    __tablename__ = "plants"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), unique=True, nullable=False)
    phone_number = Column(String(15), unique=True, nullable=False)

    config_id = Column(Integer, ForeignKey("configurations.id"), nullable=False)

    def _init_(self, **kwargs):
        """
        Initialize Plant object/entry
        """
        self.name = kwargs.get("name")
        self.phone_number = kwargs.get("phone_number")
        self.config_id = kwargs.get("config_id")
    
    def serialize(self):
        """
        Serializes Plant object
        """
        config = Configuration.query.filter_by(id=self.config_id).first()
        return {
            "id": self.id,
            "name": self.name,
            "phone_number": self.phone_number, 
            "config_id": config.simple_serialize()
        }

    def simple_serialize(self):
        """
        Simple serializes Plant Object 
        """
        return {
            "id": self.id,
            "name": self.name,
            "phone_number": self.phone_number
        }


class Configuration(db.Model):
    """
    Configuration Model 

    One-to-one relationship with Plant table. 
    Multiple Users can change these values and we use just use the most updated values.
    """

    __tablename__ = "configurations"
    id = Column(Integer, primary_key=True, autoincrement=True)
    chemical_type = Column(SQLAlchemyEnum(ChemicalType), nullable=False)
    chemical_concentration = Column(DECIMAL, nullable=False)
    num_filters = Column(Integer, nullable=False)
    num_clarifiers = Column(Integer, nullable=False)

    # plant_id = Column(Integer, ForeignKey('plants.id'), nullable=False)

    def _init_(self, **kwargs):
        """
        Initialize Configuration object/entry
        """
        self.chemical_type = kwargs.get("chemical_type")
        self.chemical_concentration = kwargs.get("chemical_concentration")
        self.num_filters = kwargs.get("num_filters")
        self.num_clarifiers = kwargs.get("num_clarifiers")
        # self.plant_id = kwargs.get("plant_id")

    def simple_serialize(self):
        """
        Simple serializes Configuration object
        """
        return {
            "id": self.id,
            "chemical_type": self.chemical_type.toJSON(),
            "chemical_concentration": str(self.chemical_concentration),
            "num_filters": self.num_filters,
            "num_clarifiers": self.num_clarifiers,
        }

class DosageEntry(db.Model):
    """
    Dosage Entry Model 

    Many-to-one relationship with User model. Many Dosage Entries can be associated with one User. 
    Do not delete associated Dosage Entries if User is deleted. 

    Other optional relations: CalibrationSection, ChangeDoseSection
    """

    __tablename__ = "dosage_entries"
    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, default=datetime.now())
    is_deleted = Column(Boolean, default=False)
    # SKIPPED FOR MVP: tank volumes

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    # calibration is required if changing dose 
    calibration_id = Column(Integer, ForeignKey("calibrations.id"), nullable=True)
    change_dose_id = Column(Integer, ForeignKey("change_doses.id"), nullable=True)

    def _init_(self, **kwargs):
        """
        Initialize Dosage Entry object/entry 
        """
        self.user_id = kwargs.get("user_id")
        self.calibration_id = kwargs.get("calibration_id")
        self.change_dose_id = kwargs.get("change_dose_id")


class CalibrationSection(db.Model): 
    """
    Calibration Section Model 

    One-to-One relationship with DosageEntry model. 
    """

    __tablename__ = "calibrations"
    id = Column(Integer, primary_key=True, autoincrement=True)
    slider_position = Column(DECIMAL, nullable=False)
    inflow_rate = Column(Integer, nullable=False)
    starting_volume = Column(Integer, nullable=False)
    ending_volume = Column(Integer, nullable=False)
    elapsed_seconds = Column(Integer, nullable=False)
    calculated_flow_rate = Column(DECIMAL, nullable=False)
    calculated_chemical_dose = Column(DECIMAL, nullable=False)
    slider_pos_chem_dose_ratio = Column(DECIMAL, nullable=False)

    dosage_entry_id = Column(Integer, ForeignKey("dosage_entries.id"), nullable=False)

    def _init_(self, **kwargs):
        """
        Initialize Calibration Section object/entry 
        """

        self.slider_position = kwargs.get("slider_position")
        self.inflow_rate = kwargs.get("inflow_rate")
        self.starting_volume = kwargs.get("starting_volume")
        self.ending_volume = kwargs.get("ending_volume")
        self.elapsed_seconds = kwargs.get("elaspsed_seconds")
        self.calculated_flow_rate = kwargs.get("calculated_flow_rate")
        self.calculated_chemical_dose = kwargs.get("calculated_chemical_dose")
        self.slider_pos_chem_dose_ratio = kwargs.get("slider_pos_chem_dose_ratio")
        self.dosage_entry_id = kwargs.get("dosage_entry_id")


class ChangeDoseSection(db.Model):
    """
    Change Dose Section Model 

    One-to-One relationship with DosageEntry model. 
    One-to-One relationship with CalibrationSection model. 
    """

    __tablename__ = "change_doses"
    id = Column(Integer, primary_key=True, autoincrement=True)
    target_coagulant_dose = Column(DECIMAL, nullable=False)
    new_slider_position = Column(DECIMAL, nullable=False)

    dosage_entry_id = Column(Integer, ForeignKey("dosage_entries.id"), nullable=False)
    related_calibration_id = Column(Integer, ForeignKey("calibrations.id"), nullable=True)

    def _init_(self, **kwargs):
        self.target_coagulant_dose = kwargs.get("target_coagulant_dose")
        self.new_slider_position = kwargs.get("new_slider_position")
        self.dosage_entry_id = kwargs.get("dosage_entry_id")
        self.related_calibration_id = kwargs.get("related_calibration_id")


class RawWaterEntry(db.Model):
    """
    Raw Water Entry Model 

    Many-to-one relationship with User model. Many Raw Water Entries can be associated with one User. 
    Do not delete associated Raw Water Entries if User is deleted. 
    """
    __tablename__ = "raw_water_entries"
    id = Column(Integer, primary_key=True, autoincrement=True)
    utn = Column(Integer, nullable=False)
    turbidity_method = Column(String, nullable=True)

    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    def _init_(self, **kwargs):
        """
        Initialize Raw Water Entry object/entry
        """
        self.utn = kwargs.get("utn")
        self.turbidity_method = kwargs.get("turbidity_method")
        self.user_id = kwargs.get("user_id")


# --------MODELS NOT USED FOR MVP--------
# class TankVolumeSection(db.Model):
#     """
#     Tank Volume Section Model

#     Many-to-One relationship with DosageEntry model. 
#     """

# class ClarifiedEntry(db.Model):
#     """
#     Clarified Entry Model

#     Many-to-One relationship with Plant model.
#     Many-to-One relationship withe User model. 
#     """

#     __tablename__ = "clarified_entries"
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     aggregated_clarified_turb = Column(Integer, nullable=True)
#     clarifier_section = Column()

# class ClarifierSection(db.Model):
#     """
#     Clarifier Section Model

#     Many-to-One relationship with ClarifiedEntry model. 
#     """

# class FiltersEntry(db.Model):
#     """
#     Filters Entry Model

#     Many-to-One relationship with Plant model.
#     Many-to-One relationship with User model. 
#     """

# class FilterSection(db.Model):
#     """
#     Filter Section Model 

#     Many-to-One relationship with FiltersEntry model. 
#     """

# class PostTreatmentEntry(db.Model):
#     """
#     Post Treatment Entry Model

#     Many-to-One relationship with User model. 
#     """

# class FeedbackEntry(db.Model):
#     """
#     Feedback Entry Model

#     Many-to-One relationship with User model. 
#     """
