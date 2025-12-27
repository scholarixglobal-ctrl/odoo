from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["pbkdf2_sha512", "plaintext"], deprecated=["plaintext"])
password = "8586583"
hashed = pwd_context.hash(password)
print(hashed)
