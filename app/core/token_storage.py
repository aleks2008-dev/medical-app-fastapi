from datetime import datetime, timedelta
from typing import Optional
import json
from app.infrastructure.redis import get_redis
from app.core.config import settings

class TokenStorage:
    def __init__(self):
        self.redis = None
    
    async def _get_redis(self):
        if not self.redis:
            self.redis = await get_redis()
        return self.redis
    
    async def store_refresh_token(self, user_id: str, token: str) -> None:
        """Сохранить refresh токен в Redis"""
        redis_client = await self._get_redis()
        key = f"refresh_token:{user_id}"
        
        # Сохраняем токен с TTL равным времени жизни refresh токена
        ttl = settings.refresh_token_expire_days * 24 * 60 * 60  # в секундах
        
        token_data = {
            "token": token,
            "created_at": datetime.utcnow().isoformat(),
            "user_id": user_id
        }
        
        await redis_client.setex(key, ttl, json.dumps(token_data))
    
    async def get_refresh_token(self, user_id: str) -> Optional[str]:
        """Получить refresh токен из Redis"""
        redis_client = await self._get_redis()
        key = f"refresh_token:{user_id}"
        
        token_data = await redis_client.get(key)
        if token_data:
            data = json.loads(token_data)
            return data.get("token")
        return None
    
    async def revoke_refresh_token(self, user_id: str) -> None:
        """Отозвать refresh токен"""
        redis_client = await self._get_redis()
        key = f"refresh_token:{user_id}"
        await redis_client.delete(key)
    
    async def store_blacklisted_token(self, token: str, exp: datetime) -> None:
        """Добавить токен в черный список"""
        redis_client = await self._get_redis()
        key = f"blacklist:{token}"
        
        # TTL до истечения токена
        ttl = int((exp - datetime.utcnow()).total_seconds())
        if ttl > 0:
            await redis_client.setex(key, ttl, "revoked")
    
    async def is_token_blacklisted(self, token: str) -> bool:
        """Проверить, находится ли токен в черном списке"""
        redis_client = await self._get_redis()
        key = f"blacklist:{token}"
        return await redis_client.exists(key)
    
    async def store_user_session(self, user_id: str, session_data: dict) -> None:
        """Сохранить данные сессии пользователя"""
        redis_client = await self._get_redis()
        key = f"session:{user_id}"
        
        # Сессия живет столько же, сколько refresh токен
        ttl = settings.refresh_token_expire_days * 24 * 60 * 60
        
        await redis_client.setex(key, ttl, json.dumps(session_data))
    
    async def get_user_session(self, user_id: str) -> Optional[dict]:
        """Получить данные сессии пользователя"""
        redis_client = await self._get_redis()
        key = f"session:{user_id}"
        
        session_data = await redis_client.get(key)
        if session_data:
            return json.loads(session_data)
        return None
    
    async def revoke_user_session(self, user_id: str) -> None:
        """Отозвать сессию пользователя"""
        redis_client = await self._get_redis()
        await redis_client.delete(f"session:{user_id}")
        await redis_client.delete(f"refresh_token:{user_id}")

# Глобальный экземпляр
token_storage = TokenStorage()