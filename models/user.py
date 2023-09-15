"""
This module is responsible for the user models.
"""

from pydantic import BaseModel


class UserBase(BaseModel):
    """
    All common fields between UserCreate and UserUpdate
    """
    id: str
    name: str
    phone_number: str
    email: str
    profile_pic: dict = None
    password: str
    role: str # like client, admin
    pan_number: str = None
    pan_card_pic: dict = None
    aadhar_number: str = None
    aadhar_card_pic: dict = None
    # Add more fields as per your user requirements


class UserCreate(BaseModel):
    """
    This class is responsible for the data received for creating the user.

    The fields are:
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
    name: str
    phone_number: str
    email: str
    profile_pic: dict # will contain filename and file_data
    password: str
    pan_number: str = None
    pan_card_pic: dict = None
    aadhar_number: str = None
    aadhar_card_pic: dict = None
    # role: str | None = "client"


class UserCreateResponse(BaseModel):
    """
    This class is responsible for the data sending after the user is created.

    The fields are:
    - `id`
    """
    id: str


class TokenSchema(BaseModel):
    """
    This class is responsible for the token schema.

    The fields are:
    - `access_token`
    - `refresh_token`
    - `role`
    """
    access_token: str
    refresh_token: str
    role: str


class TokenData(BaseModel):
    """
    This class is responsible for the token data.
    """
    username: str = None


class AmountUserId(BaseModel):
    """
    This class is responsible for the amount and user_id.

    The fields are: 
    - `amount`
    - `user_id`
    """
    amount: int
    user_id: str

