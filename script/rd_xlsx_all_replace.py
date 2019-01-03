import xlrd
import xlwt
import re
import random


def repl(*resting):
    """读取当前文件下1.xlsx文件第一列的内容，批量替换关键字存入2.xls"""
    workbook = xlrd.open_workbook('1.xlsx')
    new_book = xlwt.Workbook()
    new_sheet = new_book.add_sheet('Sheet1', cell_overwrite_ok=True)
    sheet1 = workbook.sheet_by_name('Sheet1')
    rows_num = sheet1.nrows
    # print(rows_num)
    name_list = []
    for i in range(0, rows_num):
        name = sheet1.cell_value(i, 0)
        for j in resting:
            name = name.replace(j, '').replace(r1, '').replace(r2, '')
        name_list.append(name)
    for name_ in name_list:
        print(name_, name_list.index(name_))
        new_sheet.write(name_list.index(name_), 0, name_)
        new_book.save('2.xls')
        
#此处输入关键字

repl()
