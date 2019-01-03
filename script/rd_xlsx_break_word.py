import xlwt
import xlrd


def rm_re():
    """读取1.xlsx，以空格拆分1.xlsx第一列的所有单元格内容，保存到3.xls文件中"""
    workbook = xlrd.open_workbook('1.xlsx')
    sheet1 = workbook.sheet_by_name('Sheet1')
    new_book = xlwt.Workbook()
    new_sheet = new_book.add_sheet('Sheet1')
    rows_num = sheet1.nrows
    all_prod = []
    for i in range(0, rows_num):
        name = sheet1.cell_value(i, 0).split(' ')
        for name_ in name:
            all_prod.append(name_)
    new_all_prod = list(set(all_prod))
    for write_content in new_all_prod:
        new_sheet.write(new_all_prod.index(write_content), 0, write_content)
    new_book.save('3.xls')


rm_re()
