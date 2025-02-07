from sanic import Sanic

from database.db import Base, engine
from routes.routes import bp_admin, bp_user, bp_webhook
from utils.create_test_data import create_test_data

app = Sanic("BankAPI")
app.blueprint(bp_user, url_prefix="/user")
app.blueprint(bp_admin, url_prefix="/admin")
app.blueprint(bp_webhook, url_prefix="/webhook")


@app.before_server_start
async def setup_db(app, _):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await create_test_data()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
