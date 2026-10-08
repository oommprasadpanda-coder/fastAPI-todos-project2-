from fastapi.security import OAuth2PasswordBearer 
from jose import jwt , JWTError 
from datetime import timedelta ,timezone , datetime 
from fastapi import FastAPI , Depends , HTTPException 

SECRET_KEY = "mybitunboy"
ALGORITHM = "HS256"

oauth2_schema = OAuth2PasswordBearer(tokenUrl="login")



def create_token(data : dict):
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(minutes=30)

    to_encode.update({"exp" : expire})


    token = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return token

def verify_token(token : str = Depends(oauth2_schema)):
    try :
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
    except JWTError:
        HTTPException(
            status_code=404,
            detail="payload not found"
        )


        return payload






