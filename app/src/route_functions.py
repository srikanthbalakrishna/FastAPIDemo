import json
from unittest import result
from fastapi.responses import JSONResponse
from fastapi import status
from config import models, schemas
from config.app_config import DESIGNATIONS, MAX_CLASS_CAPACITY
from config.dbconfig import SessionLocal
from .utils import *
from typing import List
from datetime import datetime


def createSchool(request: schemas.School):
    db = SessionLocal()
    payloadValidity = payloadCheckAddschool(request)
    if payloadValidity.status_code != status.HTTP_200_OK:
        return result

    new_school = models.School(id=request.id,
                               name=request.name,
                               designation=request.designation,
                               phone=request.phone)
    try:
        db.add(new_school)
        db.commit()
        db.refresh(new_school)
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content=jsonresponse(f"{e}", 'fail'))

    return JSONResponse(content=jsonresponse('', 'pass', new_school))


def deleteSchool(id: int):
    db = SessionLocal()
    db.query(models.School).filter(models.School.id == id).delete(
        synchronize_session=False)
    db.commit()

    return JSONResponse(content=jsonresponse('', 'pass', "deleted"))


def updateSchool(request: schemas.School):
    db = SessionLocal()
    payloadValidity = payloadCheckAddschool(request)
    if payloadValidity.status_code != status.HTTP_200_OK:
        return payloadValidity
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
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content=jsonresponse(f"{e}", 'fail'))
    return JSONResponse(content=jsonresponse('', 'pass', "updated"))


def createClass(request: schemas.Class):
    db = SessionLocal()
    payloadValidity = payloadCheckAddClass(request)
    if payloadValidity.status_code != status.HTTP_200_OK:
        return payloadValidity
    newClass = models.Class(id=request.id,
                            students=str(request.students),
                            teacherId=request.teacherId,
                            dateAdded=str(datetime.now())[:19])

    try:
        db.add(newClass)
        db.commit()
        db.refresh(newClass)
    except Exception as e:
        return JSONResponse(status_code=200,
                            content=jsonresponse(f"{e}", 'fail'))

    return JSONResponse(content=jsonresponse('', 'pass', newClass))


def addStudent(id: int, request: List[int]):
    db = SessionLocal()
    classToUpdate = db.query(models.Class).filter(models.Class.id == id)
    updatedList = json.loads(classToUpdate.first().students)
    updatedList.extend(request)
    updatedList = str(updatedList)
    classToUpdate.update({"students": updatedList})

    db.commit()

    return JSONResponse(content=jsonresponse('', 'pass', "updated"))


def deleteClass(id: int):
    db = SessionLocal()
    db.query(models.Class).filter(models.Class.id == id).delete(
        synchronize_session=False)
    db.commit()

    return JSONResponse(content=jsonresponse('', 'pass', "deleted"))


def getAvailability(classId: int):
    db = SessionLocal()
    requiredClass = db.query(models.Class).filter_by(id=classId)
    return JSONResponse(content=jsonresponse(
        '', 'pass',
        "Available" if len(json.loads(requiredClass.first().students)
                           ) < MAX_CLASS_CAPACITY else "Full"))
