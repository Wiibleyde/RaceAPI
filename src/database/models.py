from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, create_engine, ForeignKey, Boolean
from sqlalchemy.orm import Session

Base = declarative_base()
engine = create_engine('sqlite:///database.db', echo=True)
session = Session(engine)

class Stable(Base):
    __tablename__ = 'stable'
    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __repr__(self):
        return f"<Stable(name={self.name})>"

class Pilot(Base):
    __tablename__ = 'pilot'
    id = Column(Integer, primary_key=True)
    firstname = Column(String, nullable=False)
    lastname = Column(String, nullable=False)
    stable_id = Column(Integer, ForeignKey('stable.id'))
    nationality = Column(String)

    def __repr__(self):
        return f"<Pilot(firstname={self.firstname}, lastname={self.lastname})>"

class Race(Base):
    __tablename__ = 'race'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    laps = Column(Integer)

class RaceLeaderboard(Base):
    __tablename__ = 'race_leaderboard'
    id = Column(Integer, primary_key=True)
    race_id = Column(Integer, ForeignKey('race.id'))
    pilot_id = Column(Integer, ForeignKey('pilot.id'))
    position = Column(Integer)
    achievedLaps = Column(Integer)
    pitstops = Column(Boolean)

class RaceEvent(Base):
    __tablename__ = 'race_event'
    race_id = Column(Integer, ForeignKey('race.id'), primary_key=True)
    type = Column(Integer)
    sector = Column(Integer)


def init_db():
    Base.metadata.create_all(engine)