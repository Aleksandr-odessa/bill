from pydantic import ValidationError
from sanic import Sanic, response
from sanic.exceptions import InvalidUsage
from sqlalchemy.future import select

from database.db import get_db
from database.models import Account, Payment
from utils.secret import verify_signature


class WebhookController:
    __slots__ = ('schema_create')

    def __init__(self, schema_create):
        self.schema_create = schema_create

    async def handle_webhook(self,request):
        try:
            data = self.schema_create(**request.json).dict()
            if not verify_signature(data):
                return response.json({"error": "Invalid signature"}, status=400)
            transaction_id = data["transaction_id"]
            account_id = data["account_id"]
            user_id = data["user_id"]
            amount = data["amount"]
            async for db in get_db():
                account = await self.get_or_create_account(db, user_id, account_id)
                await self.save_transaction(db, transaction_id, account_id, amount)
                await self.update_account_balance(db, account, amount)
                return response.json({"message": "Payment processed successfully"})
        except Exception as e:
            print(e)
            return response.json({"error": str(e)}, status=400)

    @staticmethod
    async def get_or_create_account(db, user_id, account_id):
        account = await db.execute(select(Account).where(Account.id == account_id, Account.user_id == user_id))
        account = account.scalar()
        if not account:
            account = Account(id=account_id, user_id=user_id, balance=0.0)
            db.add(account)
            await db.commit()
        return account

    @staticmethod
    async def save_transaction(db, transaction_id, account_id, amount):
        try:
            existing_transaction = await db.execute(select(Payment).where(Payment.transaction_id == transaction_id))
            existing_transaction = existing_transaction.scalar()
            if existing_transaction:
                raise ValueError("Transaction already exists")
            transaction = Payment(
                transaction_id=transaction_id,
                account_id=account_id,
                amount=amount
            )
            db.add(transaction)
            await db.commit()
        except Exception as e:
            await db.rollback()

    @staticmethod
    async def update_account_balance(db, account, amount):
        account.balance += amount
        await db.commit()




