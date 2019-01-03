import os
import xlrd
import random


'''读取当前文件夹下的xlsx文件，批量重命名文件夹，并且将文件内的图片按顺序排序、改名'''
def rename_file():
    '''按照当前文件夹下的xlsx文件，批量重命名文件夹'''
    # 目标xlsx 文件名2.xlsx 默认为脚本所在同一目录
    wookbook = xlrd.open_workbook('1.xlsx')
    # 2.xlsx中要处理的Sheet名
    Sheet1 = wookbook.sheet_by_name('Sheet1')
    rows_num = Sheet1.nrows
    # 要处理的品牌的图片文件夹路径
    path = '/Volumes/UUU/apple'
    file_list = os.listdir(path)
    new_path_list = []
    for file_ in file_list:
        for i in range(0, rows_num):
            title = Sheet1.cell(i, 0).value
            new_title = Sheet1.cell(i, 1).value
            myRandom = str(random.randint(0, 9999))
            if file_ == title:
                old_path = f'{path}/{file_}'
                new_path = f'{path}/{new_title}' + myRandom + '#'
                os.renames(old_path, new_path)
                new_path_list.append(new_path)
            else:
                pass
    print(new_path_list)
    return new_path_list


def listdir_nohidden(path):
    for f in os.listdir(path):
        if not f.startswith('.'):
            yield f
# rename_file()


def rename_img_sort():
    num = 0
    for path in rename_file():
        img_list = listdir_nohidden(path)
        # print(img_list)
        rep_abs_path = path.replace('/Volumes/UUU/apple/', '')
        img_list = sorted(img_list, key=lambda x: int(x[:-4]))
        for img_path in img_list:
            num += 1
            old_img_path = path + f'/{img_path}'
            new_img_path = path + f'/{rep_abs_path}_{num}.jpg'
            os.rename(old_img_path, new_img_path)
rename_img_sort()
