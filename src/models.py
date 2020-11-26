# -*- coding: utf-8 -*-
# @Time : 2020/8/12 18:46
# @Author : ck
# @FileName: models_demo.py


from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Table, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .database import Base

# 创建一个中间表
task_cases = Table(
    "task_cases",
    Base.metadata,
    Column("task_id", Integer, ForeignKey("task.task_id")),
    Column("case_id", Integer, ForeignKey("case.case_id"))
)

class Task(Base):
    __tablename__ = "task"

    task_id = Column(Integer, primary_key=True, index=True, nullable=False, autoincrement=True)
    user = Column(String(20), default='Admin')
    device = Column(JSON)
    creat_time = Column(DateTime(timezone=True), server_default=func.now())
    case = relationship("Case", secondary=task_cases)
    # case = relationship("Case", backref='own_task')


class Case(Base):
    __tablename__ = "case"

    case_id = Column(Integer, primary_key=True, index=True, autoincrement=True, nullable=False)
    case_name = Column(String(20), unique=False, index=False)
    user = Column(String(20))
    description = Column(String(100), nullable=True)
    upload_time = Column(DateTime(timezone=True), server_default=func.now())
    update_time = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    # case = relationship("Task", secondary=task_cases)
    attachment = relationship("Attachment")


class Attachment(Base):
    __tablename__ = "attachment"
    attachment_id = Column(Integer, primary_key=True, index=True, autoincrement=True, nullable=False)
    attachment_name = Column(String(50))
    file_type = Column(Integer, default=0)
    static_address = Column(String(120), unique=False, index=False)
    case_id = Column(Integer, ForeignKey("case.case_id"))
    upload_time = Column(DateTime(timezone=True), server_default=func.now())
    message = Column(String(100), nullable=True)
    version = Column(String(20), nullable=True)
