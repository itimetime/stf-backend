# -*- coding: utf-8 -*-
# @Time : 2020/8/12 18:46
# @Author : ck
# @FileName: schemas.py

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class Attachment(BaseModel):
    case_id: Optional[int] = None
    static_address: str
    attachment_name: str
    message:Optional[str] = None
    version:Optional[str] = None

    class Config:
        orm_mode = True


class CaseIn(BaseModel):
    case_name: str
    user: Optional[str] = 'Admin'
    description: str

    class Config:
        orm_mode = True


class CaseOut(CaseIn):
    case_id: int
    user: str
    upload_time: datetime
    update_time: datetime
    attachment: List[Attachment]



class Task(BaseModel):
    user: str
    devices: dict

    class Config:
        orm_mode = True


class TaskCase(BaseModel):
    task_id: int
    case_id: int

    class Config:
        orm_mode = True
