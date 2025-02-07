from functools import wraps

from sanic import response

from utils.secret import decode_token


def protected(func):
    @wraps(func)
    async def wrapper(self, request, *args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return response.json({"error": "Unauthorized"}, status=401)

        user_data = decode_token(token)
        if not user_data:
            return response.json({"error": "Unauthorized"}, status=401)

        request.ctx.user = user_data
        return await func(self, request, *args, **kwargs)

    return wrapper