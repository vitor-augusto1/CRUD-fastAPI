from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_user_password(hashed_password: str, plain_text_password: str) -> bool:
    return pwd_context.verify(plain_text_password, hashed_password)

