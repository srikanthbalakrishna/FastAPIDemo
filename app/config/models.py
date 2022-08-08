from sqlalchemy import Column, ForeignKey, Integer, String, ARRAY
from sqlalchemy.orm import relationship
from config.dbconfig import Base


class School(Base):
    __tablename__ = "school"
    id = Column(Integer, primary_key=True)
    designation = Column(String)  #Alt:ENUM to enforce designations
    name = Column(String)
    phone = Column(String)
    classes = relationship("Class")


class Class(Base):
    __tablename__ = "class"
    id = Column(Integer, primary_key=True)
    teacherId = Column(Integer, ForeignKey("school.id"))
    #students serialised list -> manually enforce FK: check if student exists
    students = Column(String)
    dateAdded = Column(String)
