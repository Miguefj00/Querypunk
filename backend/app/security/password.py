from passlib.context import CryptContext

# Password hashing configuration using bcrypt.
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


def hash_password(password: str) -> str:
    """ Hash a password before storing it in the database. """
    return pwd_context.hash(password[:72])


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """ Verify a plain password against a stored hash. """
    return pwd_context.verify(plain_password, hashed_password)
