from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """
    Hash a password with bcrypt

    Arguments:
    ---------
    password: str
        password to be hashed

    Returns:
    --------
    hashed_password: str
        hashed password
    """
    hashed_password: str = pwd_context.hash(password)
    return hashed_password


def verify_password(password: str, hash_password: str) -> bool:
    """
    Verify if a password is correct

    Arguments:
    ---------
    password: str
        password to be verify

    hash_password: str
        hashed password to verify against    

    Returns:
    --------
    is_correct: bool
        Is password correct?
    """
    is_correct: bool = pwd_context.verify(password, hash_password)
    return is_correct
