from pydantic import BaseModel, EmailStr
from uuid import uuid4, UUID


class UserCreate(BaseModel):
    email:EmailStr
    password: str
    full_name: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class ResponseWebhook(BaseModel):
    transaction_id: str
    user_id: int
    account_id: int
    amount:int
    signature: str

class UserUpdateRequest(BaseModel):
    old: dict
    new: dict

class AccountResponse(BaseModel):
    id: int
    balance: float

class UserResponseAdmin(BaseModel):
    id: int
    email: str
    full_name: str
    is_admin: int
    accounts: list[AccountResponse]