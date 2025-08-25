from sqlalchemy import Column, Integer, String, ForeignKey, JSON, Boolean, Table
from sqlalchemy.orm import relationship
from .config import Base, engine


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    username = Column(String)
    is_consuming = Column(Boolean, default=False, nullable=False)


class Location(Base):
    __tablename__ = "location"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)


class ContractType(Base):
    __tablename__ = "contract_type"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)


class PositionLevel(Base):
    __tablename__ = "position_level"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)


class WorkSchedule(Base):
    __tablename__ = "work_schedule"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)


class WorkModel(Base):
    __tablename__ = "work_model"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)


user_location_association = Table(
    "users_location_association",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("user.id")),
    Column("location_id", Integer, ForeignKey("location.id")),
)
user_contract_type_association = Table(
    "users_contract_types_association",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("user.id")),
    Column("contract_type_id", Integer, ForeignKey("contract_type.id")),
)
user_position_level_association = Table(
    "users_position_level_association",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("user.id")),
    Column("position_level_id", Integer, ForeignKey("position_level.id")),
)
user_work_schedule_association = Table(
    "users_work_schedule_association",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("user.id")),
    Column("work_schedule_id", Integer, ForeignKey("work_schedule.id")),
)
user_work_model_association = Table(
    "users_work_model_association",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("user.id")),
    Column("work_model_id", Integer, ForeignKey("work_model.id")),
)
user_subcategory_association = Table(
    "users_subcategory_association",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("user.id")),
    Column("subcategory_id", Integer, ForeignKey("subcategory.id")),
)
user_category_association = Table(
    "users_category_association",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("user.id")),
    Column("category_id", Integer, ForeignKey("category.id")),
)

Base.metadata.create_all(engine)