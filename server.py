import os
import shutil
import threading
from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm
from loguru import logger
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy.orm.attributes import flag_modified

from modules.auth import verify_password, create_access_token, get_password_hash, check_login, \
    check_admin, UserInfo, ACCESS_TOKEN_EXPIRE_MINUTES
from modules.data import get_db, UserDB, Base, engine, SessionLocal, ServicesDB
from modules.services import ServiceInfo, get_default_service_info, update_nginx_conf, restart_nginx, service_on, \
    service_off, service_remove, is_on


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("正在初始化nginx配置...")
    shutil.copy("/app/templates/nginx/nginx.conf", "/app/nginx/")
    shutil.copy("/app/templates/nginx/default.conf", "/app/nginx/")
    logger.info("正在初始化資料庫...")
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
    await update_nginx_conf()
    logger.info("初始化完成!")


    yield

    logger.info("正在關閉伺服器並釋放資源...")

app = FastAPI(lifespan=lifespan)

class HealthCheck(BaseModel):
    status: str = "ok"

@app.get("/health_check")
async def health_check() -> HealthCheck:
    return HealthCheck()

class Message(BaseModel):
    message: str

@app.post("/api/login")
async def login(response: Response, form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)) -> Message:
    user = db.query(UserDB).filter(UserDB.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="帳號或密碼錯誤")

    access_token = create_access_token(data={"sub": user.username, "role": "admin" if user.is_admin else "user"})
    response.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}",
        httponly=True,
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES*60,
        samesite="lax",
        secure=False
    )
    return Message(message="登入成功")

@app.post("/api/logout")
async def logout(response: Response) -> Message:
    response.delete_cookie("access_token")
    return Message(message="登出成功")

class LoginInfo(BaseModel):
    user: str
    role: str
    status: str = "ok"

@app.get("/api/verify-admin")
async def verify_admin(current_user: UserInfo = Depends(check_admin)) -> LoginInfo:
    return LoginInfo(user=current_user["sub"], role=current_user["role"])

@app.get("/api/verify")
async def verify_user(current_user: UserInfo = Depends(check_login)) -> LoginInfo:
    return LoginInfo(user=current_user["sub"], role=current_user["role"])

class AService(BaseModel):
    service_name: str
    host: str
    info: ServiceInfo

class ServiceList(BaseModel):
    services: list[AService]

@app.get("/api/services")
async def get_services(current_user: UserInfo = Depends(check_login), db: Session = Depends(get_db)) -> ServiceList:
    services = db.query(ServicesDB).all()
    ret: list[AService] = []
    for service in services:
        ret.append(AService(service_name=service.service_name, host=service.host, info=service.info))
    return ServiceList(services=ret)

class AServiceStatus(BaseModel):
    service_name: str
    status: str

class ServiceStatusList(BaseModel):
    services: list[AServiceStatus]

@app.get("/api/services/status")
async def get_services_status(current_user: UserInfo = Depends(check_login), db: Session = Depends(get_db)) -> ServiceStatusList:
    services = db.query(ServicesDB).all()
    ret: list[AServiceStatus] = []
    for service in services:
        ret.append(AServiceStatus(service_name=service.service_name, status=is_on(service)))
    return ServiceStatusList(services=ret)

class ServiceCreate(BaseModel):
    name: str

@app.post("/api/services")
async def create_service(user_in: ServiceCreate, current_user: UserInfo = Depends(check_admin), db: Session = Depends(get_db)) -> Message:
    name = user_in.name
    service = db.query(ServicesDB).filter(ServicesDB.service_name == name).first()
    if service:
        raise HTTPException(status_code=400, detail="服務已存在")

    service = ServicesDB(service_name=name, host="", info=get_default_service_info())
    db.add(service)
    db.commit()
    return Message(message="服務創建成功")

@app.delete("/api/services")
async def delete_service(user_in: ServiceCreate, current_user: UserInfo = Depends(check_admin), db: Session = Depends(get_db)) -> Message:
    name = user_in.name
    service = db.query(ServicesDB).filter(ServicesDB.service_name == name).first()
    if service is None:
        raise HTTPException(status_code=400, detail="服務不存在")
    db.delete(service)
    db.commit()
    await update_nginx_conf()
    return Message(message="服務刪除成功")

class ServicePut(BaseModel):
    name: str
    info: ServiceInfo

@app.put("/api/services")
async def update_service(user_in: ServicePut, current_user: UserInfo = Depends(check_admin), db: Session = Depends(get_db)) -> Message:
    name = user_in.name
    service: ServicesDB | None = db.query(ServicesDB).filter(ServicesDB.service_name == name).first()
    if service is None:
        raise HTTPException(status_code=400, detail="服務不存在")
    info = user_in.info
    host = "" if info["present"] != "http" else info["present_info"]["http"]["hostname"]+":"+str(info["present_info"]["http"]["port"])
    service.info = info
    service.host = host
    flag_modified(service, "info")
    db.commit()
    await update_nginx_conf()
    threading.Timer(10, restart_nginx).start()  # 等nginx配置文件寫入完成再重啟
    return Message(message="更新成功")

@app.post("/api/services/on")
async def start_service(user_in: ServiceCreate, current_user: UserInfo = Depends(check_admin), db: Session = Depends(get_db)) -> Message:
    name = user_in.name
    service: ServicesDB | None = db.query(ServicesDB).filter(ServicesDB.service_name == name).first()
    if service is None:
        raise HTTPException(status_code=400, detail="服務不存在")
    await service_on(service)
    return Message(message="啟動成功")

@app.post("/api/services/off")
async def stop_service(user_in: ServiceCreate, current_user: UserInfo = Depends(check_admin), db: Session = Depends(get_db)):
    name = user_in.name
    service: ServicesDB | None = db.query(ServicesDB).filter(ServicesDB.service_name == name).first()
    if service is None:
        raise HTTPException(status_code=400, detail="服務不存在")
    await service_off(service)
    return Message(message="停止成功")

@app.post("/api/services/remove")
async def stop_service(user_in: ServiceCreate, current_user: UserInfo = Depends(check_admin), db: Session = Depends(get_db)):
    name = user_in.name
    service: ServicesDB | None = db.query(ServicesDB).filter(ServicesDB.service_name == name).first()
    if service is None:
        raise HTTPException(status_code=400, detail="服務不存在")
    await service_remove(service)
    return Message(message="刪除成功")