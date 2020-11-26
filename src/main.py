# -*- coding: utf-8 -*-
# @Time : 2020/8/12 18:47
# @Author : ck
# @FileName: main.py
import asyncio
import os
import time
from typing import List

from fastapi import Depends, FastAPI, HTTPException, UploadFile, File
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from airtest_uwa.run import execute_case
from config import script_static_dir, project_dir, apk_static_dir
from . import crud, models, schemas
from .database import SessionLocal, engine
from .unzip import unzip_file

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="UWA_STF ",
              description="后台接口",
              version="0.1.0",
              openapi_url="/api/v1/api.json", )


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 获取apk列表
@app.get("/api/v2/apk", name="获取apk", tags=["apk"])
def get_apk(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    apk = crud.get_apk_list(db, skip, limit)
    return apk

# 获取脚本列表
@app.get("/api/v2/cases", name="获取脚本", tags=["case"], response_model=List[schemas.CaseOut])
def get_case(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    case = crud.get_case_list(db, skip, limit)
    return case


# 增加脚本信息
@app.post("/api/v2/cases/add", name="添加脚本", tags=["case"], response_model=schemas.CaseOut)
def add_case(case: schemas.CaseIn, attachment_id: List, db: Session = Depends(get_db)):
    return crud.creat_case(db=db, case=case, attachment=attachment_id)


# 增加脚本信息
@app.post("/api/v2/file/add", name="添加脚本", tags=["case"])
def add_atta(atta: schemas.Attachment, db: Session = Depends(get_db)):
    return crud.creat_attachment(db=db, attachment=atta)


# 编辑脚本信息
@app.post("/api/v2/cases/edit", name="编辑脚本", tags=["case"])
def update_case(case_id: int, case: schemas.CaseIn, db: Session = Depends(get_db)):
    case = crud.update_case(db=db, case=case, case_id=case_id)
    return case


# 删除脚本
@app.delete("/api/v2/cases/delete", name="删除脚本", tags=["case"])
def delete_case(case_id: int, db: Session = Depends(get_db)):
    db_case = crud.delete_case(db, case_id=case_id)
    if db_case is None:
        raise HTTPException(status_code=404, detail="Website not found")
    return db_case


# 上传脚本附件
# @app.post("/api/v1/files/upload", name="上传脚本附件", tags=["case"])
async def upload_case(file: bytes = File(...)):
    contents = await file.read()
    with open(file.filename, "wb") as f:
        f.write(contents)
    return {"attachment_name": file.filename}


app.mount("/stf-static", StaticFiles(directory="stf-static"), name="static")


# 获取任务
@app.get("/api/v2/tasks", name="获取任务列表", tags=["task"])
def get_task():
    pass


async def execute_case_new(device, case):
    device = [item['serial'] for item in device]
    cases = []
    for i in case:
        for j in i["attachment"]:
            cases.append(project_dir + '//' + j["static_address"][:-4])
    # cases.append(project_dir + '//' + case[0][:-4])
    await execute_case(device, cases)


# 创建任务
@app.post("/api/v2/tasks/add", name="创建任务", tags=["task"])
async def add_task(device: List, case: List):
    # 写数据库，能顺利写入数据库，便可返回相应的数据。
    # 异步执行数据
    task_dict = {}
    for i in device:
        task_dict[i['serial']] = i
    # 存储任务数据库
    task = models.Task(device=task_dict, user='Admin')
    db = next(get_db())
    case_obj = []
    for item in case:
        case_obj.append(crud.get_case_detail(db, case_id=item["case_id"]))
    task.case = case_obj
    db.add(task)
    db.commit()
    db.refresh(task)
    asyncio.create_task(execute_case_new(device, case))
    return task


# TODO 批量安装apk

# TODO 批量执行bash脚本

# 异步操作步骤 创建解压任务
async def runzip(zip_src, dst_dir):
    asyncio.create_task(unzip_file(zip_src, dst_dir))


@app.post("/api/v2/upload/file")
async def create_files(file: UploadFile = File(...)):
    contents = await file.read()
    attachment_name = file.filename
    # 写入本地
    path = script_static_dir + '//' + str(time.time())
    if not os.path.exists(path):
        os.mkdir(path)
    attachment_address = path + '//' + attachment_name
    with open(attachment_address, "wb") as f:
        f.write(contents)
    # 存储地址写进数据库
    attachment = models.Attachment(attachment_name=attachment_name, static_address=attachment_address)
    for db in get_db():
        db.add(attachment)
        db.commit()
        db.refresh(attachment)
    # 因为上传的是zip 采用异步进行解压
    if attachment_name.endswith('.zip'):
        await runzip(attachment_address, path)
    return attachment


@app.post("/api/v2/upload/apk")
async def upload_apk(file: UploadFile = File(...)):
    contents = await file.read()

    attachment_name = file.filename
    # 写入本地
    if not os.path.exists(apk_static_dir):
        os.mkdir(apk_static_dir)
    attachment_address = apk_static_dir + '//' + attachment_name + str(time.time())
    with open(attachment_address, "wb") as f:
        f.write(contents)
    # 存储地址写进数据库
    attachment = models.Attachment(attachment_name=attachment_name, static_address=attachment_address, file_type=1)
    for db in get_db():
        db.add(attachment)
        db.commit()
        db.refresh(attachment)
    return attachment


if __name__ == '__main__':
    import uvicorn

    uvicorn.run("src.main:app")
# uvicorn src.main:app –-reload
