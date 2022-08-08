from fastapi import Depends, HTTPException, status, Response, APIRouter

school_router = APIRouter(tags=['School'])
class_router = APIRouter(tags=['Class'])