# -*- coding: utf-8 -*-
# @Time : 2020/9/21 14:26
# @Author : ck
# @FileName: config.py
import os
cases_dir = r"C:\Users\ck\PycharmProjects\FastApi_Demo\stf\airtest_uwa"

g = os.walk(cases_dir)
case_list = {}
for path, dir_list, file_list in g:
    print(dir_list)
    case_list["cases"] = dir_list
    break
print(case_list)