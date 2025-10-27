import hashlib
from app.domain.interfaces.password_hasher import PasswordHasher

class SHA256PasswordHasher(PasswordHasher):
    def hash(self, password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()
    
    def verify(self, plain_password: str, hashed_password: str) -> bool:
        return self.hash(plain_password) == hashed_password