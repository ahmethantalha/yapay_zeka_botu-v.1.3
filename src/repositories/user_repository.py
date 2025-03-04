from typing import Optional
from .base_repository import BaseRepository
from src.models.user import User
from src.core.security import Security

class UserRepository(BaseRepository[User]):
    def __init__(self, session, security: Security):
        super().__init__(session, User)
        self.security = security
    
    def get_by_username(self, username: str) -> Optional[User]:
        return self.session.query(User).filter_by(username=username).first()
    
    def create_user(self, username: str, password: str) -> User:
        password_hash = self.security.hash_password(password)
        user = User(username=username, password_hash=password_hash)
        return self.create(user)