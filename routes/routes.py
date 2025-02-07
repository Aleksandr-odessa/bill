from sanic import Blueprint

from controllers.admin_controller import AdminController
from controllers.user_controller import UserController
from controllers.webhook_controller import WebhookController
from database.models import User
from schemas import ResponseWebhook

user_controller = UserController(User)
admin_controller = AdminController(User)
webhook_controller = WebhookController(ResponseWebhook)

bp_user = Blueprint("user")

# Регистрируем маршруты
bp_user.post("/login")(user_controller.login)
bp_user.get("/me")(user_controller.get_me)
bp_user.get("/accounts")(user_controller.get_user_accounts)
bp_user.get("/payments")(user_controller.get_user_payments)


bp_admin = Blueprint("admin")

bp_admin.post("/login")(admin_controller.login)
bp_admin.get("/me")(admin_controller.get_me)
bp_admin.post("/register")(admin_controller.create_user)
bp_admin.delete("/delete/<user_id:int>")(admin_controller.delete_user)
bp_admin.patch("/patch")(admin_controller.patch)
bp_admin.get("/all_users")(admin_controller.get_all_users)
bp_admin.get("/payments")(admin_controller.get_users_with_accounts)

bp_webhook = Blueprint("webhook")

bp_webhook.post("/payment")(webhook_controller.handle_webhook)

