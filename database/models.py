from sqlalchemy import Column, Integer, String, Date, ForeignKey, Float, DateTime
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
    date = Column(Date)
    exercise_name = Column(String)

    user = relationship("User", back_populates="workouts")
    sets = relationship("WorkoutSet", back_populates="workout")

class WorkoutSet(Base):
    __tablename__ = 'workout_sets'

    id = Column(Integer, primary_key=True)
    workout_id = Column(Integer, ForeignKey('workouts.id'))
    reps = Column(Integer)

    workout = relationship("Workout", back_populates="sets")
