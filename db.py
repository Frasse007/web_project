import os
from datetime import datetime, timezone
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.orm import DeclarativeBase, Session

load_dotenv()

# DB connection with .env variables
DATABASE_URL = (
    f"postgresql+psycopg2://{os.getenv('DB_USERNAME')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)

engine = create_engine(DATABASE_URL, echo=False)

# Base class to build on
class Base(DeclarativeBase):
    pass

# Model for DB table
class Observation(Base):
    __tablename__ = "observations"

    id          = Column(Integer, primary_key=True, autoincrement=True)
    city        = Column(String,  nullable=False)
    country     = Column(String,  nullable=False)
    latitude    = Column(Float,   nullable=False)
    longitude   = Column(Float,   nullable=False)
    elevation   = Column(Float)
    temperature = Column(Float)
    windspeed   = Column(Float)
    created_at  = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            "id":          self.id,
            "city":        self.city,
            "country":     self.country,
            "latitude":    self.latitude,
            "longitude":   self.longitude,
            "elevation":   self.elevation,
            "temperature": self.temperature,
            "windspeed":   self.windspeed,
            "created_at":  self.created_at.isoformat() if self.created_at else None,
        }

# Creates table if it doesn't already exist
Base.metadata.create_all(engine)

# Creates a new observation entry from instance of WeatherReport
def insert_observation(weather_report) -> Observation:
    obs = Observation(
        city=weather_report.city,
        country=weather_report.country,
        latitude=weather_report.latitude,
        longitude=weather_report.longitude,
        elevation=weather_report.elevation,
        temperature=weather_report.temperature,
        windspeed=weather_report.windspeed,
    )
    with Session(engine) as session:
        session.add(obs)
        session.commit()
        session.refresh(obs)   # populates id + created_at
        return obs

# Returns all observations for a specific city
def get_observations_by_city(city: str) -> list[Observation]:
    with Session(engine) as session:
        return (
            session.query(Observation)
            .filter(Observation.city.ilike(city))
            .all()
        )

# Updates the fields that allow updating on an existing entry
def update_observation(observation_id: int, updates: dict) -> Observation | None:
    allowed = {"temperature", "windspeed", "elevation"}
    with Session(engine) as session:
        obs = session.get(Observation, observation_id)
        if obs is None:
            return None
        for key, value in updates.items():
            if key in allowed:
                setattr(obs, key, value)
        session.commit()
        session.refresh(obs)
        return obs

# Deletes an observation by its ID
def delete_observation(observation_id: int) -> bool:
    with Session(engine) as session:
        obs = session.get(Observation, observation_id)
        if obs is None:
            return False
        session.delete(obs)
        session.commit()
        return True