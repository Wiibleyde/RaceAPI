from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, create_engine, ForeignKey, Boolean, Enum as SQLAlchemyEnum
from sqlalchemy.orm import Session

from src.race.events import RaceEvents

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
    type = Column(SQLAlchemyEnum(RaceEvents))
    sector = Column(Integer)


def init_db():
    Base.metadata.create_all(engine)

def init_test_data():
    if not session.query(Stable).filter_by(name="Ferrari").first():
        stable1 = Stable(name="Ferrari")
        session.add(stable1)
    if not session.query(Stable).filter_by(name="McLaren").first():
        stable2 = Stable(name="McLaren")
        session.add(stable2)
    session.commit()

    if not session.query(Pilot).filter_by(firstname="Charles", lastname="Leclerc").first():
        pilot1 = Pilot(firstname="Charles", lastname="Leclerc", stable_id=session.query(Stable).filter_by(name="Ferrari").first().id, nationality="Monaco")
        session.add(pilot1)
    if not session.query(Pilot).filter_by(firstname="Lewis", lastname="Hamilton").first():
        pilot2 = Pilot(firstname="Lewis", lastname="Hamilton", stable_id=session.query(Stable).filter_by(name="Ferrari").first().id, nationality="United Kingdom")
        session.add(pilot2)
    if not session.query(Pilot).filter_by(firstname="Lando", lastname="Norris").first():
        pilot3 = Pilot(firstname="Lando", lastname="Norris", stable_id=session.query(Stable).filter_by(name="McLaren").first().id, nationality="United Kingdom")
        session.add(pilot3)
    if not session.query(Pilot).filter_by(firstname="Oscar", lastname="Piastri").first():
        pilot4 = Pilot(firstname="Oscar", lastname="Piastri", stable_id=session.query(Stable).filter_by(name="McLaren").first().id, nationality="Australia")
        session.add(pilot4)
    session.commit()

    if not session.query(Race).filter_by(name="Monaco").first():
        race = Race(name="Monaco", laps=78)
        session.add(race)
    session.commit()

    race_id = session.query(Race).filter_by(name="Monaco").first().id
    if not session.query(RaceLeaderboard).filter_by(race_id=race_id, pilot_id=session.query(Pilot).filter_by(firstname="Charles").first().id).first():
        race_leaderboard1 = RaceLeaderboard(race_id=race_id, pilot_id=session.query(Pilot).filter_by(firstname="Charles").first().id, position=1, achievedLaps=0, pitstops=False)
        session.add(race_leaderboard1)
    if not session.query(RaceLeaderboard).filter_by(race_id=race_id, pilot_id=session.query(Pilot).filter_by(firstname="Lewis").first().id).first():
        race_leaderboard2 = RaceLeaderboard(race_id=race_id, pilot_id=session.query(Pilot).filter_by(firstname="Lewis").first().id, position=2, achievedLaps=0, pitstops=False)
        session.add(race_leaderboard2)
    if not session.query(RaceLeaderboard).filter_by(race_id=race_id, pilot_id=session.query(Pilot).filter_by(firstname="Lando").first().id).first():
        race_leaderboard3 = RaceLeaderboard(race_id=race_id, pilot_id=session.query(Pilot).filter_by(firstname="Lando").first().id, position=3, achievedLaps=0, pitstops=False)
        session.add(race_leaderboard3)
    session.commit()

    if not session.query(RaceEvent).filter_by(race_id=race_id, type=RaceEvents.GREEN_FLAG, sector=1).first():
        race_event = RaceEvent(race_id=race_id, type=RaceEvents.GREEN_FLAG, sector=1)
        session.add(race_event)
    session.commit()
