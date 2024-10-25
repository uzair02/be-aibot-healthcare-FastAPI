"""
This module defines the base user model and specific user types (Patient, Doctor, Admin)
for a FastAPI application using SQLAlchemy ORM. Each user type extends the base user model
and includes additional fields relevant to their roles.

Imports:
    - uuid: Used to generate unique identifiers for users.
    - sqlalchemy:
        - Boolean, Column, Date, String, text: Core types for defining database columns and constraints.
    - sqlalchemy.dialects.postgresql:
        - TIMESTAMP, UUID: Specific data types for PostgreSQL.
    - src.repository.database:
        - Base: Base class for SQLAlchemy models, enabling the declarative model pattern.

Classes:
    - BaseUser:
        Abstract base class for all user types (Patient, Doctor, Admin) with common attributes.
    - Patient:
        Model representing a patient user, extending the BaseUser class with additional attributes.
    - Doctor:
        Model representing a doctor user, extending the BaseUser class with additional attributes.
    - Admin:
        Model representing an admin user, extending the BaseUser class with additional attributes.
"""

import uuid

from sqlalchemy import Boolean, Column, Date, String, Integer, text
from sqlalchemy.dialects.postgresql import TIMESTAMP, UUID
from sqlalchemy.orm import relationship
from src.repository.database import Base





class BaseUser(Base):
    """
    Abstract base model for users in the application. Contains common attributes
    that all user types (Patient, Doctor, Admin) will inherit.

    Attributes:
        user_id (UUID): Unique identifier for the user, automatically generated.
        username (str): Unique username for the user.
        hashed_password (str): Hashed password for user authentication.
        is_active (bool): Indicates whether the user's account is active. Defaults to True.
        timestamp (datetime): Timestamp for when the user record was created, defaults to the current time.
        email (str): The email address of the user, must be unique.
        city (str): The city where the user resides.
    """

    __abstract__ = True

    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    timestamp = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), nullable=False)
    email = Column(String, unique=True, nullable=False)
    city = Column(String, nullable=True)


class Patient(BaseUser):
    """
    Model representing a patient user in the application. Inherits from BaseUser
    and adds attributes specific to patients.

    Attributes:
        first_name (str): The first name of the patient.
        last_name (str): The last name of the patient.
        phone_number (str): The patient's phone number, must be unique.
        dob (date): The date of birth of the patient.
        gender (GenderEnum): Gender of the patient.
        blood_group (BloodGroupEnum): Blood group of the patient.
        emergency_contact (str): Emergency contact number, optional.
        appointments: relation between appointment and patient.
        prescriptions: relation between prescription and patient.
    """

    __tablename__ = "patients"

    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    phone_number = Column(String(11), nullable=False, unique=True)
    dob = Column(Date, nullable=False)
    gender = Column(String(6), nullable=False)
    blood_group = Column(String(6), nullable=True)
    emergency_contact = Column(String(11), nullable=True)
    appointments = relationship("Appointment", back_populates="patient", cascade="all, delete-orphan")
    prescriptions = relationship("Prescription", back_populates="patient", cascade="all, delete-orphan")


class Doctor(BaseUser):
    """
    Model representing a doctor user in the application. Inherits from BaseUser
    and adds attributes specific to doctors.

    Attributes:
        first_name (str): The first name of the doctor.
        last_name (str): The last name of the doctor.
        specialization (str): The medical specialization of the doctor.
        phone_number (str): The doctor's phone number, must be unique.
        gender (GenderEnum): Gender of the doctor.
        years_of_experience (int): Number of years the doctor has been practicing.
        consultation_fee (float): The consultation fee charged by the doctor.
        time_slots: relation between doctor and timeslot.
        appointments: relation between appointment and doctor.
        prescriptions: relation between prescription and doctor.
    """

    __tablename__ = "doctors"

    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    specialization = Column(String, nullable=False)
    phone_number = Column(String(11), nullable=False, unique=True)
    gender = Column(String(6), nullable=False)
    years_of_experience = Column(Integer, nullable=False)
    consultation_fee = Column(Integer, nullable=False)
    time_slots = relationship("TimeSlot", back_populates="doctor", cascade="all, delete-orphan")
    appointments = relationship("Appointment", back_populates="doctor", cascade="all, delete-orphan")
    prescriptions = relationship("Prescription", back_populates="doctor", cascade="all, delete-orphan")


class Admin(BaseUser):
    """
    Model representing an admin user in the application. Inherits from BaseUser
    and adds attributes specific to admins.
    """

    __tablename__ = "admins"

