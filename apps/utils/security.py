from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bycrpt"],deprecated="auto")

def hash_password(password:str):
    return pwd_context.hash(password)

def verify_password(plain,hashed):
    return pwd_context.verfiy(plain,hashed)