from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt # type: ignore
from .models import User, UserRole
from sqlalchemy.orm import Session
from .database import SessionLocal
from .config import SECRET_KEY, ALGORITHM

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
        # This function should decode the JWT token and retrieve the user
    # Placeholder function for demonstration purposes
    # Replace with actual JWT authentication logic
    user = db.query(User).filter(User.email == token).first()  # Replace token with actual user retrieval logic
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")
    return user
    # credentials_exception = HTTPException(
    #     status_code=status.HTTP_401_UNAUTHORIZED,
    #     detail="Could not validate credentials",
    #     headers={"WWW-Authenticate": "Bearer"},
    # )
    
    # try:
    #     payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    #     email: str = payload.get("sub")
    #     if email is None:
    #         raise credentials_exception
    # except JWTError:
    #     raise credentials_exception
    
    # db = SessionLocal()
    # user = db.query(User).filter(User.email == email).first()
    # db.close()
    
    # if user is None:
    #     raise credentials_exception
    
    # return user



async def admin_required(current_user: User = Depends(get_current_user)):
    if current_user.role != UserRole.admin:
        raise HTTPException(status_code=403, detail="Not an admin")
