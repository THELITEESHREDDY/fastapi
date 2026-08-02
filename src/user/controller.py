from fastapi import HTTPException,status,Request
from datetime import datetime, timedelta,timezone
from src.user.dtos import UserSchema
from src.user.dtos import LoginSchema
from sqlalchemy.orm import Session
from src.user.models import UserModel
from pwdlib import PasswordHash
import jwt
from jwt.exceptions import InvalidTokenError
from src.utils.settings import settings


password_hash = PasswordHash.recommended()

def get_password_hash(password):
    return password_hash.hash(password)

def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password,hashed_password)


def register(user_data:UserSchema, db:Session):
    ## user name validatioin
    ##  email validation

    is_user = db.query(UserModel).filter(UserModel.username == user_data.username).first()

    if is_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Username already exists.."
        )

    is_user = db.query(UserModel).filter(UserModel.email == user_data.email).first()

    if is_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists"
        )

    hash_password = get_password_hash(user_data.password)

    new_user = UserModel(
        name = user_data.name,
        username = user_data.username,
        email = user_data.email,
        hashed_password = hash_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user



def login_user(user_data:LoginSchema ,db:Session):
    
    is_user = db.query(UserModel).filter(UserModel.username == user_data.username).first()
    
    if not is_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Username/ password wrong"
        )

    if not verify_password(user_data.password, is_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED ,
            detail="Username/password wrong"
        )

    exp_time = datetime.now(timezone.utc) + timedelta(minutes=settings.EXP_TIME)
    token = jwt.encode({"id":is_user.id,"exp":exp_time},settings.SECRET_KEY,settings.ALGORITHM)
    
    return {"token" : token}


def is_authenticated(request:Request,db:Session):
    try:
        token = request.headers.get("authorization")

        if not token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="Unauthorized"
            )
        
        token = token.split(" ")[-1]

        data = jwt.decode(token,settings.SECRET_KEY, settings.ALGORITHM)

        user_id = data.get("id")
        

        is_user = db.query(UserModel).filter(UserModel.id==user_id).first()

        if not is_user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="you are unauthorized"
            )
        return is_user
    except InvalidTokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="you are unauthorized"
            )
