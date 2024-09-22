from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from database.models import Base, User, WeightHistory
from config import DATABASE_URL
from datetime import datetime

engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

def get_user(user_id):
    session = Session()
    user = session.query(User).filter_by(user_id=user_id).first()
    session.close()
    return user

def create_or_update_user(user_id, gender=None, height=None, weight=None):
    session = Session()
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
    session.close()

def get_latest_weight(user_id):
    session = Session()
    latest_weight = session.query(WeightHistory).filter_by(user_id=user_id).order_by(WeightHistory.date.desc()).first()
    session.close()
    return latest_weight.weight if latest_weight else None

def get_weight_history(user_id):
    session = Session()
    weight_history = session.query(WeightHistory).filter_by(user_id=user_id).order_by(desc(WeightHistory.date)).all()
    session.close()
    return weight_history
