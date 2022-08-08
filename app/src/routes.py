import json
from fastapi import Depends, HTTPException, status, Response, APIRouter
from config import models, schemas
from config.app_config import DESIGNATIONS, MAX_CLASS_CAPACITY
from sqlalchemy.orm import Session
from config.dbconfig import get_db
from typing import List
from datetime import datetime

school_router = APIRouter(tags=['School'])
class_router = APIRouter(tags=['Class'])


###########School APIs
@school_router.post('/school',
                    status_code=status.HTTP_201_CREATED,
                    tags=['School'])
def createSchool(request: schemas.School, db: Session = Depends(get_db)):
    if request.designation not in DESIGNATIONS:  #Alt: Can modify sql-model to make designation an ENUM
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Designations must one of: {DESIGNATIONS}")

    new_school = models.School(id=request.id,
                               name=request.name,
                               designation=request.designation,
                               phone=request.phone)
    try:
        db.add(new_school)
        db.commit()
        db.refresh(new_school)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"{e}")

    return new_school


@school_router.delete('/school/{id}',
                      status_code=status.HTTP_204_NO_CONTENT,
                      tags=['School'])
def deleteSchool(id: int, db: Session = Depends(get_db)):
    db.query(models.School).filter(models.School.id == id).delete(
        synchronize_session=False)
    db.commit()

    return "deleted"


@school_router.put('/school',
                   status_code=status.HTTP_202_ACCEPTED,
                   tags=['School'])
def updateSchool(request: schemas.School, db: Session = Depends(get_db)):
    if request.designation not in DESIGNATIONS:  #Alt: Can modify sql-model to make designation an ENUM
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Designations must one of: {DESIGNATIONS}")
    try:
        db.query(models.School).filter(models.School.id == request.id).update({
            "designation":
            request.designation,
            "name":
            request.name,
            "phone":
            request.phone
        })
        db.commit()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"{e}")
    return "updated"


########## Class APIs


@class_router.post('/class',
                   status_code=status.HTTP_201_CREATED,
                   tags=['Class'])
def createClass(request: schemas.Class, db: Session = Depends(get_db)):

    try:
        if not isinstance(request.students, list):
            raise Exception("'students' must be List of Integer(StudentIds)")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"{e}")

    newClass = models.Class(id=request.id,
                            students=str(request.students),
                            teacherId=request.teacherId,
                            dateAdded=str(datetime.now())[:19])

    try:
        db.add(newClass)
        db.commit()
        db.refresh(newClass)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"{e}")

    return newClass


@class_router.put('/class/{id}',
                  status_code=status.HTTP_202_ACCEPTED,
                  tags=['Class'])
def addStudent(id: int, request: List[int], db: Session = Depends(get_db)):
    classToUpdate = db.query(models.Class).filter(models.Class.id == id)
    updatedList = json.loads(classToUpdate.first().students)
    updatedList.extend(request)
    updatedList = str(updatedList)
    classToUpdate.update({"students": updatedList})

    db.commit()

    return "updated"


@class_router.delete('/class',
                     status_code=status.HTTP_204_NO_CONTENT,
                     tags=['Class'])
def deleteClass(id: int, db: Session = Depends(get_db)):
    db.query(models.Class).filter(models.Class.id == id).delete(
        synchronize_session=False)
    db.commit()

    return "deleted"


@class_router.get('/class/availability', tags=['Class'])
def getAvailability(classId: int, db: Session = Depends(get_db)):
    requiredClass = db.query(models.Class).filter_by(id=classId)
    return "Available" if len(json.loads(
        requiredClass.first().students)) < MAX_CLASS_CAPACITY else "Full"
