from sqlalchemy import create_engine, Column, String, DateTime, Integer, func
from sqlalchemy.orm import declarative_base, sessionmaker, scoped_session
from sqlalchemy.exc import SQLAlchemyError
import requests
from config import Config

DATABASE_URI = Config.DATABASE_URI
CONFIG_API_URL = Config.CONFIG_API_URL

config_response = requests.get(CONFIG_API_URL + "/get_em")
config_data = config_response.json()
workers, tokens, __, __ = config_data

Base = declarative_base()


class CheckinData(Base):
    __tablename__ = "checkin"

    worker_id = Column(String, primary_key=True)
    worker_name = Column(String, nullable=False)
    checkin_time = Column(String, primary_key=True)


class HighscoreData(Base):
    __tablename__ = "highscore"

    worker_name = Column(String, primary_key=True)
    work_done = Column(Integer, default=0, nullable=False)


def get_engine():
    return create_engine(DATABASE_URI)


def get_session():
    engine = get_engine()
    Session = sessionmaker(bind=engine)
    session = scoped_session(Session)
    return session


def create_tables():
    engine = get_engine()
    Base.metadata.create_all(engine)


def create_highscore():
    session = get_session()
    try:
        for name in workers:
            if not session.query(HighscoreData).filter_by(worker_name=name).first():
                new_worker = HighscoreData(worker_name=name)
                session.add(new_worker)
        session.commit()
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Error creating highscore data: {e}")
    finally:
        session.close()


def save_checkin(token, check_timestamp):
    session = get_session()
    if token not in tokens:
        return False
    try:
        data = CheckinData(
            worker_id=token,
            worker_name=tokens[token],
            checkin_time=check_timestamp
        )
        session.add(data)
        session.commit()
        return True
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Error saving check-in: {e}")
        return False
    finally:
        session.close()


def update_work_done():
    session = get_session()
    try:
        # Count check-ins per worker
        work_counts = session.query(
            CheckinData.worker_name,
            func.count(func.distinct(CheckinData.worker_id)).label('count')
        ).group_by(CheckinData.worker_name).all()

        for worker_name, count in work_counts:
            session.query(HighscoreData).filter_by(worker_name=worker_name).update(
                {'work_done': HighscoreData.work_done + count}
            )
        session.commit()
        return True
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Error updating work done: {e}")
        return False
    finally:
        session.close()


def clear_highscores():
    session = get_session()
    try:
        session.query(HighscoreData).delete()
        session.commit()
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Error clearing highscores: {e}")
    finally:
        session.close()


def clear_checkin():
    session = get_session()
    try:
        session.query(CheckinData).delete()
        session.commit()
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Error clearing checkin: {e}")
    finally:
        session.close()

def get_highscore():
    session = get_session()
    try:
        highscores = session.query(HighscoreData).order_by(HighscoreData.work_done.desc()).all()
        return True, highscores
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Error getting Highscores: {e}")
        return False, None
    finally:
        session.close()



if __name__ == '__main__':
    import datetime

    update_work_done()









