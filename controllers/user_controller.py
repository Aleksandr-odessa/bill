from sanic import response
from sqlalchemy import func
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload

from database.db import get_db
from database.models import Account, User
from utils.protected import protected
from utils.secret import (admin_email, admin_name, admin_password, def_email,
                          def_name, def_password, hash_password)

from .auth_controller import AuthController


class UserController(AuthController):
    def __init__(self, model):
        super().__init__(model)

    @protected
    async def get_me(self, request):
        """Получение информации о пользователе"""
        user_data = request.ctx.user
        async for db in get_db():
            result = await db.execute(select(self.model).where(self.model.id == user_data["user_id"]))
            user = result.scalar()
        return response.json({"id": user.id, "email": user.email, "full_name": user.full_name})

    @protected
    async def get_user_accounts(self, request):
        """Получение счетов пользователя"""
        user_id = request.ctx.user["user_id"]
        async for db in get_db():
            accounts = await db.execute(select(Account).where(Account.user_id == user_id))
            accounts = accounts.scalars().all()
            accounts_data = [{"id": acc.id, "balance": acc.balance} for acc in accounts]
            return response.json(accounts_data)


    @protected
    async def get_user_payments(self, request):
        user_id = request.ctx.user["user_id"]
        async for db in get_db():
            result = await db.execute(select(self.model).
                                      options(joinedload(self.model.accounts).joinedload(Account.payments)).
                                      where(self.model.id == user_id)
                                      )
            user = result.scalars().first()
            payments = []
            for account in user.accounts:
                for payment in account.payments:
                    payments.append({
                        "transaction_id": payment.transaction_id,
                        "account_id": payment.account_id,
                        "amount": payment.amount
                    })
            return response.json(payments)