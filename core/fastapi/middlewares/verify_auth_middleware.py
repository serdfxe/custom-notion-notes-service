from fastapi import Request, Response, logger, status
import httpx


class VerifyAuthMiddleware:
    def __init__(self, app):
        self.app = app
    async def __call__(self, request: Request, call_next):
        # Извлекаем необходимые данные из запроса, например, токен
        token = request.headers.get("Authorization")
        
        print(token)

        if token is None:
            return Response(content="Token is missing", status_code=status.HTTP_401_UNAUTHORIZED)

        # Создаем асинхронный клиент для выполнения запроса
        async with httpx.AsyncClient() as client:
            response = await client.post("http://localhost:8000/auth/verify", headers={
                "Authorization": f"{token}",
            })

            if response.status_code != status.HTTP_200_OK:
                return Response(content="Invalid token", status_code=status.HTTP_401_UNAUTHORIZED)

            # Получаем user_id из ответа
            user_id = response.json().get("user_id")

            # Если user_id найден, добавляем в заголовок x-user-id
            if user_id:
                request.headers["X-User-Id"] = str(user_id)
                
                response = await call_next(request)
                
                return response
            else:
                return Response(content="User ID not found", status_code=status.HTTP_403_FORBIDDEN)