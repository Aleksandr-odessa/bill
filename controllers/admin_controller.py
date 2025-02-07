from pydantic import ValidationError
from sanic import response
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload

from controllers.auth_controller import AuthController
from database.db import get_db
from database.models import User
from schemas import (AccountResponse, UserCreate, UserResponseAdmin,
                     UserUpdateRequest)
from utils.protected import protected
from utils.secret import hash_password


class AdminController(AuthController):
    def __init__(self, model):
        super().__init__(model)

    @protected
    async def get_me(self, request):
        """Получение данных администратора"""
        user_data = request.ctx.user
        async for db in get_db():
            user = await db.execute(select(self.model).where(self.model.id == user_data["user_id"]))
            user = user.scalar()
            if not user or not user.is_admin:
                return response.json({"error": "Access denied"}, status=403)
        return response.json(
            {"id": user.id, "email": user.email, "full_name": user.full_name, "is_admin": user.is_admin})

    @protected
    async def create_user(self, request):
        """Создание нового пользователя"""
        try:
            data = UserCreate(**request.json)
        except ValidationError as e:
            return response.json({"error": "Invalid data", "details": e.errors()}, status=400)
        new_user = User(email=data.email,
            password_hash=hash_password(data.password),
            full_name=data.full_name)
        async for db in get_db():
            request_user = await db.execute(select(self.model).where(self.model.email == new_user.email))
            if request_user.scalar():
                return response.json({"error": "User with this email already exists"}, status=400)
            db.add(new_user)
            await db.commit()
        return response.json({"message": "User registered successfully"})

    @protected
    async def delete_user(self, request, user_id):
        """Удаление пользователя"""
        async for db in get_db():
            user_delete = await db.execute(select(self.model).where(self.model.id == user_id))
            user_to_delete = user_delete.scalar()
            if not user_to_delete:
                return response.json({"error": "User not found"}, status=404)

            await db.delete(user_to_delete)
            await db.commit()
        return response.json({"message": "User deleted successfully"}, status=204)

    @protected
    async def get_all_users(self, request):
        """Получение всех пользователей"""
        async for db in get_db():
            result = await db.execute(select(User))
            users = result.scalars().all()
            return response.json([{"id": user.id, "email": user.email} for user in users])


    async def check_email(self, db, data):
        request_user = await db.execute(select(self.model).where(self.model.email == data["email"]))
        if request_user.scalar():
            return response.json({"error": "User with this email already exists"}, status=400)

    def validate_input(self, request):
        try:
            data = UserUpdateRequest(**request.json)
            return data.old, data.new
        except ValidationError as e:
            raise ValueError({"error": "Invalid data", "details": e.errors()})

    @staticmethod
    def check_required_fields(data_old, data_new):
        if not data_old.get("email"):
            raise ValueError({"error": "Email is required in 'old' data"})

        if not any(key in data_new for key in ["email", "full_name", "password"]):
            raise ValueError({"error": "No valid fields to update in 'new' data"})

    @staticmethod
    async def find_user(db, email, model):
        request_user = await db.execute(select(model).where(model.email == email))
        user = request_user.scalar()
        if not user:
            raise ValueError({"error": "User not found"})
        return user

    @staticmethod
    async def update_user_data(db, user, data_new, check_email_func, hash_password_func):
        if "email" in data_new and not await check_email_func(db, data_new):
            user.email = data_new["email"]
        if "full_name" in data_new:
            user.full_name = data_new["full_name"]
        if "password" in data_new:
            user.password_hash = hash_password_func(data_new["password"])
        return user

    @staticmethod
    async def save_changes(db, user):
        try:
            db.add(user)
            await db.commit()
            await db.refresh(user)
        except SQLAlchemyError as e:
            await db.rollback()
            raise ValueError({"error": "Database error", "details": str(e)})

    @staticmethod
    def build_success_response(user):
        return {
            "message": "User updated successfully",
            "user": {
                "id": user.id,
                "email": user.email,
                "full_name": user.full_name
            }
        }

    @protected
    async def patch(self, request):
        try:
            data_old, data_new = self.validate_input(request)
            self.check_required_fields(data_old, data_new)
            async for db in get_db():
                user = await self.find_user(db, data_old["email"], self.model)
                user = await self.update_user_data(db, user, data_new, self.check_email, hash_password)
                await self.save_changes(db, user)
                return response.json(self.build_success_response(user))

        except ValueError as e:
            return response.json(e.args[0], status=400)
        except Exception as e:
            return response.json({"error": "Internal server error", "details": str(e)}, status=500)


    @protected
    async def get_users_with_accounts(self, request):
        async for db in get_db():
            result = await db.execute(select(self.model)
                .options(joinedload(self.model.accounts))
                                      )
            users = result.scalars().unique().all()
            users_with_accounts = [
                UserResponseAdmin(
                    id=user.id,
                    email=user.email,
                    full_name=user.full_name,
                    is_admin=user.is_admin,
                    accounts=[
                        AccountResponse(
                            id=account.id,
                            balance=account.balance
                        )
                        for account in user.accounts
                    ]
                )
                for user in users
            ]

            return response.json([user.model_dump() for user in users_with_accounts])