from typing import Optional, Generator

from fastapi import Depends, Header, HTTPException


class DummySession:
    def close(self) -> None:
        pass


def get_db() -> Generator[DummySession, None, None]:
    db = DummySession()
    try:
        yield db
    finally:
        db.close()


async def get_current_user(authorization: Optional[str] = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return {"user_id": 123, "username": "johndoe"}


