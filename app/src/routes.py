from .route_functions import *
from fastapi import status, APIRouter
from config import schemas
from typing import List

school_router = APIRouter(tags=['School'])
class_router = APIRouter(tags=['Class'])


###########School APIs
#createSchool
@school_router.post('/school',
                    status_code=status.HTTP_201_CREATED,
                    tags=['School'])
def postSchool(request: schemas.School):
    return createSchool(request)


#deleteSchool
@school_router.delete('/school/{id}',
                      status_code=status.HTTP_204_NO_CONTENT,
                      tags=['School'])
def destroySchool(id: int):
    return deleteSchool(id)


#updateSchool
@school_router.put('/school',
                   status_code=status.HTTP_202_ACCEPTED,
                   tags=['School'])
def putSchool(request: schemas.School):
    return updateSchool(request)


########## Class APIs


#createClass
@class_router.post('/class',
                   status_code=status.HTTP_201_CREATED,
                   tags=['Class'])
def postClass(request: schemas.Class):
    return createClass(request)


#addStudent
@class_router.put('/class/{id}',
                  status_code=status.HTTP_202_ACCEPTED,
                  tags=['Class'])
def putStudent(id: int, request: List[int]):
    return addStudent(id, request)


#deleteClass
@class_router.delete('/class',
                     status_code=status.HTTP_204_NO_CONTENT,
                     tags=['Class'])
def destroyClass(id: int):
    return deleteClass(id)


@class_router.get('/class/availability', tags=['Class'])
def fetchAvailability(classId: int):
    return getAvailability(classId)
