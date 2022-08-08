from config import schemas
from config.app_config import DESIGNATIONS
from fastapi.responses import JSONResponse
from fastapi import status


def jsonresponse(reasonText='', status='pass', responseObject=None):
    json = {
        "status": status,
        "reasonText": reasonText,
        "responseObject": responseObject
    }
    return json


def payloadCheckAddschool(request: schemas.School):
    if request.designation not in DESIGNATIONS:  #Alt: Can modify sql-model to make designation an ENUM
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content=jsonresponse(
                                f"Designations must one of: {DESIGNATIONS}",
                                'fail'))


def payloadCheckAddClass(request: schemas.School):
    if not isinstance(request.students, list):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=jsonresponse(
                "'students' must be List of Integer(StudentIds)", 'fail'))
