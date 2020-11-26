# -*- coding: utf-8 -*-
# @Time : 2020/8/12 18:46
# @Author : ck
# @FileName: database.py

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 利用pymysql驱动连接MySql
SQLALCHEMY_DATABASE_URL = 'mysql+pymysql://root:root@localhost:3306/stf?charset=utf8'

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
