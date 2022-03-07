from fastapi import status, HTTPException
from jose import jwt, JWTError

SECRET_KEY = '$e210c0b4381e30886a2498b1109a7896a13ae24c8a447ae0142a6aac413c2e4'

ALGORITHM = 'HS256'

ACCESS_TOKEN_EXPIRY = 30


# This function creates the token by taken the email id and password provide by the admin
def create_access_token(data: dict):
    to_encode = data.copy()
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# this function to add a dependencies before all the routes of the api to verify the admin
def verify_access_token(access_token: str, credentials_exception):
    try:
        payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
        admin_email: str = payload.get("email")

        if admin_email is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception
    return admin_email


def admin_access(token:str):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail=f"could not validate admin credentials"
                                          , headers={"WWW-Authenticate": "Bearer"})

    admin_email = verify_access_token(token, credentials_exception)
    return admin_email
