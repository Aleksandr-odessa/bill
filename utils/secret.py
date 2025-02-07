import hashlib
import os
from datetime import datetime, timedelta

import bcrypt
import jwt
from dotenv import load_dotenv

load_dotenv()
admin_email = os.getenv('EMAIL_ADMIN')
admin_password = os.getenv('PASSWORD_ADMIN')
admin_name = os.getenv('NAME_ADMIN')
def_email = os.getenv('EMAIL_USER')
def_name = os.getenv('NAME_USER')
def_password = os.getenv('PASSWORD_USER')
secret_key_jwt = os.getenv('SECRET_KEY_JWT')
secret_key_webhook = os.getenv('SECRET_KEY_WEBHOOK')

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed_password.encode())

def create_token(user_id: int) -> str:
    payload = {"user_id": user_id, "exp": datetime.now() + timedelta(hours=1)}
    return jwt.encode(payload, secret_key_jwt, algorithm="HS256")

def decode_token(token: str):
    token_encode = token.encode('utf-8')
    try:
        return jwt.decode(token_encode, secret_key_jwt, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return None

def verify_signature(data):
    sorted_keys = sorted(data.keys())
    concatenated_values = "".join(str(data[key]) for key in sorted_keys if key != "signature")
    concatenated_values += secret_key_webhook
    expected_signature = hashlib.sha256(concatenated_values.encode()).hexdigest()
    return data.get("signature") == expected_signature