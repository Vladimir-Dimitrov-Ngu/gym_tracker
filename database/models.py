from sqlalchemy import Column, Integer, String, Date, ForeignKey, Float, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timezone

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True)
    gender = Column(String)
    height = Column(Integer)
    
    weight_history = relationship("WeightHistory", back_populates="user", order_by="WeightHistory.date.desc()")
    workouts = relationship("Workout", back_populates="user")

class WeightHistory(Base):
    __tablename__ = 'weight_history'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    weight = Column(Float)
    date = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    user = relationship("User", back_populates="weight_history")

class Workout(Base):
    __tablename__ = 'workouts'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    date = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    muscle_group = Column(String)
    equipment = Column(String)
    sets = Column(Integer)
    reps = Column(Integer)

    user = relationship("User", back_populates="workouts")

class Equipment(Base):
    __tablename__ = 'equipment'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    muscle_group = Column(String)
    description = Column(Text)
