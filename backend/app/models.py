"""
FILE: models.py
PRIMARY SOURCE: docs/04-data-model.md
SECONDARY SOURCE: docs/11-backend-implementation-logic.md

WARNING: This is the 'Single Source of Truth' for the database schema.
Changes here require a Database Migration (Alembic) and updates to all Routers.
"""

from sqlalchemy import Column, Integer, String, Boolean, Date, DateTime, ForeignKey, Time
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=False)
    birth_date = Column(Date, nullable=True)
    role = Column(String, default="VOLUNTEER")
    service_start_date = Column(Date, nullable=True)
    last_recognized_milestone = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    attended_101 = Column(Boolean, default=False) 
    is_verified = Column(Boolean, default=False) 
    is_trainee = Column(Boolean, default=True)
    registrations = relationship("Registration", back_populates="user")

class ServiceSlot(Base):
    __tablename__ = "service_slots"
    id = Column(Integer, primary_key=True, index=True)
    slot_name = Column(String, nullable=False)
    start_time = Column(Time, nullable=False)
    capacity_limit = Column(Integer, default=15)

class Registration(Base):
    __tablename__ = "registrations"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    slot_id = Column(Integer, ForeignKey("service_slots.id"))
    service_date = Column(Date, nullable=False)
    state = Column(String, default="PENDING")
    arrival_time = Column(DateTime, nullable=True)
    user = relationship("User", back_populates="registrations")

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    actor_id = Column(Integer, ForeignKey("users.id")) # Person who made the change
    
    # Generic targets to allow reverting ANYTHING
    target_id = Column(Integer)  # ID of the User, Slot, or Registration being changed
    target_type = Column(String) # "USER", "REGISTRATION", "SERVICE_SLOT"
    
    # JSON snapshots for the Time Machine
    previous_state = Column(String, nullable=True) # JSON string of data BEFORE change
    new_state = Column(String, nullable=True)      # JSON string of data AFTER change
    
    action_type = Column(String) # e.g., "UPDATE", "REVERT", "STATUS_CHANGE"
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

class SystemSetting(Base):
    __tablename__ = "system_settings"
    id = Column(Integer, primary_key=True, index=True)
    key = Column(String, unique=True, index=True)
    value = Column(String)
    description = Column(String, nullable=True)
