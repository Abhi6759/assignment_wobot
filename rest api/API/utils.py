from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")


def hash(password: str):
    return pwd_context.hash(password)


def verify(user_password: str, hash_password: str):
    return pwd_context.verify(user_password, hash_password)
