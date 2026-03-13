import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from modules.data import get_db, UserDB, Base, engine, SessionLocal
from modules.tools import verify_password, create_access_token, get_current_user, get_password_hash


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("正在初始化資料庫...")
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        user = db.query(UserDB).filter(UserDB.username == "root").first()
        if user is None:
            user = UserDB(username="root", hashed_password=get_password_hash(os.getenv("ROOT_PASSWORD", "root")), is_admin=True)
            db.add(user)
            db.commit()
    finally:
        db.close()

    yield

    print("正在關閉伺服器並釋放資源...")

app = FastAPI(lifespan=lifespan)

@app.post("/api/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(UserDB).filter(UserDB.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="帳號或密碼錯誤")

    access_token = create_access_token(data={"sub": user.username, "role": "admin" if user.is_admin else "user"})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/api/verify-admin")
async def verify_admin(current_user: UserDB = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="權限不足，僅限管理員")
    return {"status": "ok", "user": current_user.username}

@app.get("/api/verify")
async def verify_user(current_user: UserDB = Depends(get_current_user)):
    # get_current_user 有做驗證了
    return {"status": "ok", "user": current_user.username}