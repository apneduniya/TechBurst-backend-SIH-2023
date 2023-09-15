"""
This file contains the functions and classes related to the user.
"""

# from uuid import uuid4
from fastapi import APIRouter, HTTPException, Depends
from starlette import status
from fastapi.security import OAuth2PasswordRequestForm
from typing import Tuple
from models.user import UserCreateResponse, UserCreate, TokenSchema, UserBase, AmountUserId
from database.user import UserDB
from bson import ObjectId
import datetime
import base64
from utils.user import (
    get_hashed_password,
    create_access_token,
    create_refresh_token,
    verify_password,
    get_current_active_user,
    is_admin
)

router = APIRouter()
user_db = UserDB()


@router.post('/create', summary="Create new user", response_model=UserCreateResponse, 
             description="""
Create new user with the given data:
- `name`
- `phone_number`
- `email`
- `password`
- `profile_pic` { filename, file_data }
- `pan_number` (optional)
- `pan_card_pic` (optional)
- `aadhar_number` (optional)
- `aadhar_card_pic` (optional)
"""
)
async def create_user(data: UserCreate):
    # querying database to check if user already exist
    user = user_db.get_user_email(data.email)
    if user is not None:
            raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exist"
        )
    print(data)
    external_data :dict = {**data.dict()}
    external_data["role"] = "user"
    external_data.pop("password") # Doesn't saving raw password (orginal password)
    external_data["role"] = external_data["role"].lower()
    external_data["created_at"] = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    external_data["balance"] = 0

    # profile_pic_file_id = ObjectId()
    # profile_pic_file_name = f"{str(profile_pic_file_id)}_{external_data['profile_pic']['filename']}"
    # profile_pic_file_data = external_data["profile_pic"]["file_data"].split(",")[1]
    # with open(r"{UPLOAD_DIR}/{profile_pic_file_name}".format(UPLOAD_DIR=UPLOAD_DIR, profile_pic_file_name=profile_pic_file_name), "wb") as f:
    #      f.write(base64.b64decode(profile_pic_file_data))
    # external_data["profile_pic_file_id"] = profile_pic_file_name
    external_data.pop("profile_pic")

    # pan_card_pic_file_id = ObjectId()
    # pan_card_pic_file_name = f"{str(pan_card_pic_file_id)}_{external_data['pan_card_pic']['filename']}"
    # pan_card_pic_file_data = external_data["pan_card_pic"]["file_data"].split(",")[1]
    # with open(r"{UPLOAD_DIR}/{pan_card_pic_file_name}".format(UPLOAD_DIR=UPLOAD_DIR, pan_card_pic_file_name=pan_card_pic_file_name), "wb") as f:
    #     f.write(base64.b64decode(pan_card_pic_file_data))
    # external_data["pan_card_pic_file_id"] = pan_card_pic_file_name
    external_data.pop("pan_card_pic")

    # aadhar_card_pic_file_id = ObjectId()
    # aadhar_card_pic_file_name = f"{str(aadhar_card_pic_file_id)}_{external_data['aadhar_card_pic']['filename']}"
    # aadhar_card_pic_file_data = external_data["aadhar_card_pic"]["file_data"].split(",")[1]
    # with open(r"{UPLOAD_DIR}/{aadhar_card_pic_file_name}".format(UPLOAD_DIR=UPLOAD_DIR, aadhar_card_pic_file_name=aadhar_card_pic_file_name), "wb") as f:
    #     f.write(base64.b64decode(aadhar_card_pic_file_data))
    # external_data["aadhar_card_pic_file_id"] = aadhar_card_pic_file_name
    external_data.pop("aadhar_card_pic")

    user_data = {
        'password': get_hashed_password(data.password), # Saving hashed password (for later verification)
        # 'id': str(uuid4()),
        **external_data
    }
    user_id = user_db.create_user(user_data)    # saving user to database
    return {"id": user_id, **data.dict()}
    

@router.post('/login', summary="Create access token for user", response_model=TokenSchema, 
             description="""
Create access token for user with the given data:
- `username` (email)
- `password`
"""
)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = user_db.get_user_email(form_data.username) # form_data.username is the email id of the user
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )

    hashed_pass = user['password']
    if not verify_password(form_data.password, hashed_pass):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )
    
    return {
        "access_token": create_access_token(user['email']),
        "refresh_token": create_refresh_token(user['email']),
        "role": user['role'],
    }


@router.get("/me", response_model=UserBase, summary="Get current user", 
            description="""
Get current user with the given data:
- `id`
- `name`
- `phone_number`
- `email`
- `profile_pic` { filename, file_data }
- `role`
- `created_at`
- `pan_number` (optional)
- `pan_card_pic` (optional)
- `aadhar_number` (optional)
- `aadhar_card_pic` (optional)
"""
)
async def read_users_me(
    current_user: UserBase = Depends(get_current_active_user)
):
    del current_user["password"]
    current_user["id"] = str(current_user["_id"])
    # print(current_user)
    return current_user

@router.get("/data/{limit}/{id}", response_model=UserBase, summary="Get the list of current user",
            description="""
Get the list of current user with each user consisting of the given data:
- `id`
- `name`
- `phone_number`
- `email`
- `profile_pic` { filename, file_data }
- `pan_number` (optional)
- `pan_card_pic` (optional)
- `aadhar_number` (optional)
- `aadhar_card_pic` (optional)
- `role`
- `created_at`
"""
)
async def read_users_me(
    current_user: UserBase = Depends(is_admin),
    limit: int = 10,
    id: str = None
):
    print(id)
    users_list = user_db.get_all_user(id=id, limit=limit)
    if not users_list:
        raise HTTPException(status_code=404, detail="Users not found")
    # print(users_list)
    return users_list

    