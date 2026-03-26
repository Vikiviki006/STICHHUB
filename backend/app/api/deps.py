"""
StitchHub — Auth Dependency
Provides get_current_user + role guard for route protection
"""

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.security import decode_token, oauth2_scheme
from app.models.user import User, UserRole


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    payload = decode_token(token)
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


def require_admin(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role != UserRole.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")
    return current_user


def require_wholesaler(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role not in [UserRole.admin, UserRole.wholesaler]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Wholesaler access required")
    return current_user