from datetime import datetime
from sqlalchemy.orm import Session
from app.models.user import User
from app.security.passwords import hash_password


class UserService:

    @staticmethod
    def create(db: Session, data):
        user = User(
            Username=data.username,
            Email=data.email,
            Password_hash=hash_password(data.password),
            Role_id=data.role_id,
            Created_at=datetime.utcnow().isoformat(),
            Last_login=""
        )

        db.add(user)
        db.commit()
        db.refresh(user)
        return user
