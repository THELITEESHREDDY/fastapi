from fastapi import APIRouter,HTTPException,status,Depends,Request
from sqlalchemy.orm import Session
from src.utils.db import get_db
from src.user.dtos import UserSchema
from src.user import controller
from src.user.dtos import UserResponseSchema
from src.user.dtos import LoginSchema
user_routes = APIRouter(prefix="/user")


@user_routes.post("/register",response_model=UserResponseSchema,status_code=status.HTTP_201_CREATED )
def register(user:UserSchema,db:Session=Depends(get_db)):
    return controller.register(user,db)


@user_routes.post("/login", status_code=status.HTTP_200_OK)
def longin(user:LoginSchema,db:Session=Depends(get_db)):
    print(user)
    return controller.login_user(user,db)

@user_routes.get("/is_auth",response_model=UserResponseSchema)
def is_auth(request :Request,db:Session=Depends(get_db)):
    return controller.is_authenticated(request,db) 