from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from database.models import Base, User, WeightHistory, Equipment, Workout
from config import DATABASE_URL
from datetime import datetime
from sqlalchemy.exc import IntegrityError

engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

def get_session():
    """Create a new session and return it."""
    return Session()

def close_session(session):
    """Close the given session."""
    session.close()

def get_user(user_id):
    session = get_session()
    user = session.query(User).filter_by(user_id=user_id).first()
    close_session(session)
    return user

def create_or_update_user(user_id, gender=None, height=None, weight=None):
    session = get_session()
    user = session.query(User).filter_by(user_id=user_id).first()
    if user:
        if gender is not None:
            user.gender = gender
        if height is not None:
            user.height = height
        if weight is not None:
            new_weight_entry = WeightHistory(user_id=user_id, weight=weight)
            session.add(new_weight_entry)
    else:
        user = User(user_id=user_id, gender=gender, height=height)
        session.add(user)
        if weight is not None:
            new_weight_entry = WeightHistory(user_id=user_id, weight=weight)
            session.add(new_weight_entry)
    session.commit()
    close_session(session)

def get_latest_weight(user_id):
    session = get_session()
    latest_weight = session.query(WeightHistory).filter_by(user_id=user_id).order_by(WeightHistory.date.desc()).first()
    close_session(session)
    return latest_weight.weight if latest_weight else None

def get_weight_history(user_id):
    session = get_session()
    weight_history = session.query(WeightHistory).filter_by(user_id=user_id).order_by(desc(WeightHistory.date)).all()
    close_session(session)
    return weight_history

def add_workout(user_id, muscle_group, equipment, sets, reps):
    session = get_session()
    workout = Workout(user_id=user_id, muscle_group=muscle_group, equipment=equipment, sets=sets, reps=reps)
    session.add(workout)
    session.commit()
    close_session(session)

def get_equipment_by_muscle_group(muscle_group):
    session = get_session()
    equipment_list = session.query(Equipment).filter_by(muscle_group=muscle_group).all()
    close_session(session)
    return equipment_list

def get_equipment_description(equipment_name):
    session = get_session()
    equipment = session.query(Equipment).filter_by(name=equipment_name).first()
    close_session(session)
    return equipment.description if equipment else None

def add_custom_equipment(name, muscle_group, description):
    session = get_session()
    try:
        equipment = session.query(Equipment).filter_by(name=name).first()
        if equipment:
            equipment.muscle_group = muscle_group
            equipment.description = description
        else:
            equipment = Equipment(name=name, muscle_group=muscle_group, description=description)
            session.add(equipment)
        session.commit()
    except IntegrityError:
        session.rollback()
        print(f"Equipment '{name}' already exists. Updating instead.")
        equipment = session.query(Equipment).filter_by(name=name).first()
        equipment.muscle_group = muscle_group
        equipment.description = description
        session.commit()
    finally:
        close_session(session)
