import secrets
import uuid
secret_key = secrets.token_hex(16)
print(secret_key)

# Генерация UUID
transaction_id = str(uuid.uuid4())
print(transaction_id)

