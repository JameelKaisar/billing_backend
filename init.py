from fastapi import Depends

from passlib.context import CryptContext

from billing.database import SessionLocal, engine
from billing.models import Base, User
from billing.common import get_db



users = [
    {
        'username': 'admin',
        'password': 'admin'
    },
    {
        'username': 'user',
        'password': 'user'
    }
]



pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



if __name__ == '__main__':
    Base.metadata.create_all(bind=engine)
    db = next(get_db())

    for user in users:
        username = user['username']
        password = user['password']
        hashed_password = pwd_context.hash(password)
        db_user = db.query(User).filter_by(username=username).first()
        if not db_user:
            db_user = User(username=username, hashed_password=hashed_password)
            db.add(db_user)
            db.commit()
            db.refresh(db_user)
