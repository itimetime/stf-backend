# -*- coding: utf-8 -*-
# @Time : 2020/9/23 17:38
# @Author : ck
# @FileName: unzip.py
import asyncio
import zipfile


async def unzip_file(zip_src, dst_dir):
    r = zipfile.is_zipfile(zip_src)
    if r:
        fz = zipfile.ZipFile(zip_src, 'r')
        for file in fz.namelist():
            fz.extract(file, dst_dir)
    else:
        print('This is not zip')


async def run():
    for i in range(1000):
        asyncio.create_task(
            unzip_file(r"C:\Users\ck\PycharmProjects\语法练习\语法练习.zip", rf"C:\Users\ck\PycharmProjects\语法练习\test\{i}"))

    print("执行完成")

#
# asyncio.run(run())
