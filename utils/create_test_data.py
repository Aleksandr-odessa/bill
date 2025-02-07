from sqlalchemy import func, select

from database.db import get_db
from database.models import Account, User
from utils.secret import (admin_email, admin_name, admin_password, def_email,
                          def_name, def_password, hash_password)


async def create_test_data()->None:
    async for db in get_db():
        result = await db.execute(select(func.count(User.id)))
        if not result.scalar():
            admin = User(email=admin_email, is_admin=1, full_name = admin_name,
                                 password_hash=hash_password(admin_password))
            user = User(email=def_email, full_name = def_name,
                                 password_hash=hash_password(def_password))

            db.add_all([user, admin])
            await db.commit()

            # ✅ Получаем ID пользователей
            await db.refresh(admin)
            await db.refresh(user)

            # ✅ Создаём счета для пользователей
            user_account1 = Account(user_id=user.id, balance=50)
            db.add(user_account1)
            await db.commit()