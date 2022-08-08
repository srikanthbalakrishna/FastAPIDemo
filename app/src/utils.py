import re
from fastapi.responses import JSONResponse
from fastapi import status

from config import models


def jsonresponse(reasonCode, status, reasonText, responseObject, totalRecords,
                 responseListObject):
    json = {
        "reasonCode": reasonCode,
        "status": status,
        "reasonText": reasonText,
        "responseObject": responseObject,
        "totalRecords": totalRecords,
        "responseListObject": responseListObject
    }
    return json