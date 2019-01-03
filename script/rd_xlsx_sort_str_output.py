import xlwt
import xlrd
import re


def rw_excel_86(*string):
    '''读取当前路径下 1.xlsx 文件，输入要匹配字符串，按次序输出匹配结果到 2.xls'''
    w = xlwt.Workbook()
    open_sheet2 = w.add_sheet('Sheet2')
    for s in string:
        s_index = string.index(s)
        workbook = xlrd.open_workbook('1.xlsx')
        open_sheet1 = workbook.sheet_by_name('Sheet1')
        rows_num = open_sheet1.nrows
        cols_num = open_sheet1.ncols

        #读取
        m = 0
        for i in range(0, rows_num):
            info_map = []
            for j in range(0, cols_num):
                value = open_sheet1.cell(i, j).value
                re_content = re.findall(f'.*{s}.*', str(value))
                if not re_content == []:
                    info_map.append(re_content)
                else:
                    continue
            m += 1
            open_sheet2.write(i, s_index, str(info_map).replace(']', '').replace('[', '').replace("'", ''))
    w.save('2.xlsx')

#输入参数，支持一次性输入多个
rw_excel_86('notebook')
