import random, string, jwt
from typing import Optional, List
from models import UrlRepository, Url, AuthRepository
from datetime import datetime, timedelta


class UrlShortenerService:
    def __init__(self, url_repository: UrlRepository):
        self.url_repository = url_repository

    def create_short_url(self, long_url: str) -> Url:
        short_url = self._generate_unique_short_url()
        url = Url(id=None, long_url=long_url, short_url=short_url)
        return self.url_repository.save(url)

    def get_long_url(self, short_url: str) -> Optional[str]:
        url = self.url_repository.find_by_short_url(short_url)
        return url.long_url if url else None

    def get_all_urls(self) -> List[Url]:
        return self.url_repository.get_all()

    def get_url_by_id(self, url_id: int) -> Optional[Url]:
        return self.url_repository.find_by_id(url_id)

    def update_url(self, url_id:int, short_url:str, long_url:str) -> Optional[Url]:
        existing = self.url_repository.find_by_short_url(short_url)
        if existing and existing.id != url_id:
            raise ValueError("Short url already exists")

        return self.url_repository.update(url_id, short_url, long_url)

    def delete_url(self, url_id: int) -> bool:
        return self.url_repository.delete(url_id)

    def _generate_unique_short_url(self, lenght: int = 6) -> str:
        chars = string.ascii_letters + string.digits
        while True:
            short_url = ''.join(random.choice(chars) for _ in range(lenght))
            if not self.url_repository.exists_by_short_url(short_url):
                return short_url


class AuthService:
    def __init__(self, auth_repository: AuthRepository, jwt_service: 'JWTService'):
        self.auth_repository = auth_repository
        self.jwt_service = jwt_service

    def authenticate(self, username: str, password: str) -> Optional[Url]:
        if self.auth_repository.validate_user(username, password):
            return self.jwt_service.generate_token(username)
        return None

    def validate_token(self, token: str) -> Optional[str]:
        return self.jwt_service.validate_token(token)


class JWTService:
    def __init__(self, secret_key: str):
        self.secret_key = secret_key

    def generate_token(self, username: str) -> str:
        payload = {
            'user': username,
            'exp': datetime.utcnow() + timedelta(seconds=3660)
        }
        return jwt.encode(payload, self.secret_key, algorithm='HS256')

    def validate_token(self, token: str) -> Optional[str]:
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=['HS256'])
            return payload.get('user')
        except jwt.InvalidTokenError:
            return None