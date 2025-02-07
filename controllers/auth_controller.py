from pydantic import ValidationError
from sanic import response
from sqlalchemy.future import select

from database.db import get_db
from schemas import UserLogin
from utils.secret import create_token, verify_password


class AuthController:
    def __init__(self, model):
        self.model = model

    async def login(self, request):
        """Метод для аутентификации пользователей и админов"""
        try:
            user_data = UserLogin(**request.json)
        except ValidationError as e:
            return response.json({"error": "Invalid data", "details": e.errors()}, status=400)

        email, password = user_data.email, user_data.password

        async for db in get_db():
            result = await db.execute(select(self.model).where(self.model.email == email))
            user = result.scalar()
            if not user or not verify_password(password, user.password_hash):
                return response.json({"error": "Invalid credentials"}, status=401)

            token = create_token(user.id)
            return response.json({"token": token})

