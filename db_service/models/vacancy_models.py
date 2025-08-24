from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from .config import Base

class Employer(Base):
    __tablename__ = "employers"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    vacancies = relationship("Vacancy", back_populates="employer")

class Category(Base):
    __tablename__ = "category"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    subcategories = relationship("Subcategory", back_populates="category")

class Subcategory(Base):
    __tablename__ = "subcategory"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    category_id = Column(Integer, ForeignKey("category.id"))
    category = relationship("Category", back_populates="subcategories")    
    vacancies = relationship("Vacancy", back_populates="subcategory")

class Vacancy(Base):
    __tablename__ = "vacancies"
    id = Column(Integer, primary_key=True)
    url = Column(String, unique=True)
    name = Column(String, nullable=False)
    employer_id = Column(Integer, ForeignKey("employers.id"))
    employer = relationship("Employer", back_populates="vacancies")
    subcategory_id = Column(Integer, ForeignKey("subcategory.id"))
    subcategory = relationship("Subcategory", back_populates="vacancies")
    salary = Column(String, nullable=True)

    workplaces = Column(JSONB)     
    contract_types = Column(JSONB) 
    work_schedules = Column(JSONB) 
    position_levels = Column(JSONB)
    work_models = Column(JSONB)    
    
    optional_cv = Column(Boolean, default=False, nullable=True)
