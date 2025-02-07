import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sanic_testing.reusable import ReusableClient

from app import app

app.config.DEBUG = True

def test_webhook(app):
    data = {
        "transaction_id": "5eae174f-7cd0-472c-bd36-35660f00132b",
        "user_id": 1,
        "account_id": 1,
        "amount": 100,
        "signature": "7b47e41efe564a062029da3367bde8844bea0fb049f894687cee5d57f2858bc8"
    }

    client = ReusableClient(app)
    with client:
        _, response = client.post("webhook/payment", json=data)
        assert response.status == 200



test_webhook(app)