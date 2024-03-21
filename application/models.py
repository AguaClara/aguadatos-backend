from sqlalchemy import Column, DateTime, Integer, String, Boolean, ForeignKey, Float
from datetime import datetime 
from . import db

ChemicalTypes = {'PAC', 'AL2SO43'}
TankLabels = {'A1', 'A2', 'B1', 'B2'}

# create tables 
class User(db.Model):
    """
    User model 
    
    Many-to-one relationship with Plants table. Multiple Users can be associated with One Plant
    Delete associated Users if Plant is deleted.
    """
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255),unique=True, nullable=False)
    phone_number = Column(String(15), unique=True, nullable=False)

    # Users/Operators must be associated with only one AguaClara plant 
    plant_id = Column(Integer, ForeignKey("plants.id"), nullable=False)


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


class Configuration(db.Model):
    """
    Configuration Model 

    One-to-one relationship with Plants table. 
    Multiple Users can change these values and we use just use the most updated values.
    """
    __tablename__ = "configurations"
    id = Column(Integer, primary_key=True, autoincrement=True)
    chemical_type = Column(String, nullable=False)
    chemical_concentration = Column(Float, nullable=False)
    num_filters = Column(Integer, nullable=False)
    num_clarifiers = Column(Integer, nullable=False)


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


class CalibrationSection(db.Model): 
    """
    Calibration Section Model 

    One-to-One relationship with DosageEntry model. 
    """
    __tablename__ = "calibrations"
    id = Column(Integer, primary_key=True, autoincrement=True)
    slider_position = Column(Float, nullable=False)
    inflow_rate = Column(Integer, nullable=False)
    starting_volume = Column(Integer, nullable=False)
    ending_volume = Column(Integer, nullable=False)
    elapsed_seconds = Column(Integer, nullable=False)
    calculated_flow_rate = Column(Float, nullable=False)
    calculated_chemical_dose = Column(Float, nullable=False)
    slider_pos_chem_dose_ratio = Column(Float, nullable=False)
    
    dosage_entry_id = Column(Integer, ForeignKey("dosage_entries.id"), nullable=False)


class ChangeDoseSection(db.Model):
    """
    Change Dose Section Model 

    One-to-One relationship with DosageEntry model. 
    One-to-One relationship with CalibrationSection model. 
    """
    __tablename__ = "change_doses"
    id = Column(Integer, primary_key=True, autoincrement=True)
    target_coagulant_dose = Column(Float, nullable=False)
    new_slider_position = Column(Float, nullable=False)

    dosage_entry_id = Column(Integer, ForeignKey("dosage_entries.id"), nullable=False)
    related_calibration_id = Column(Integer, ForeignKey("calibrations.id"), nullable=True)


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
