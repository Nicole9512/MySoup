import requests
from bs4 import BeautifulSoup
import re
import json
import sqlite3
import os
import threading
import queue
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import mysql.connector

"""
这是一个多线程京东自营店爬虫
"""

q = queue.Queue()

# 输入url
url = 'https://msigaming.jd.com......'
# 数据库表名，图片文件夹名
input_name = 'amd'

def pro_list(url):
    pro_list = []
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.get(url)
    info = driver.find_element_by_class_name('jSearchListArea')
    url_list = info.find_elements_by_class_name('jSubObject')
    for url in url_list:

        url = url.find_element_by_class_name('jDesc')
        a = url.find_element_by_tag_name('a')
        a = a.get_attribute('href')
        pro_list.append(a)
    return pro_list


def all_prod(url):
    all_prod_list = []
    for u in pro_list(url):
        pro_id = u.replace('https://item.jd.com/', '').replace('.html', '')
        all_prod_list.append(pro_id)
        res = requests.get(u)
        html = res.text
        re_all = re.findall('colorSize: \[.+?]', html)
        if len(re_all) == 0:
            pass
        else:
            re_all = re_all[0]
            re_skuid = re.findall('"skuId".+?,', re_all)
            for re_s in re_skuid:
                re_s = re_s.replace('"skuId":', '').replace(',', '')
                all_prod_list.append(re_s)
    all_prod_list = list(set(all_prod_list))
    return all_prod_list

for ur in all_prod(url):
    q.put(ur)


def pro_info():
    num = 1
    while q.qsize() > 0:
        id = q.get()
        i = 0
        id = id.replace('}', '')
        u = 'https://item.jd.com/' + id + '.html'
        pro_id = u.replace('https://item.jd.com/', '').replace('.html', '')
        res = requests.get(u)
        html = res.text
        soup = BeautifulSoup(html, 'lxml')

        # 名字
        num += 1
        p_name = soup.find('div', attrs={'class': 'sku-name'}).text.replace('?', '').replace(
            '/', ' ').replace('\n', '').replace('\t', '').replace('\r', '').replace('"', '').replace('\\', ' ').strip() + f'#{num}'

        # 参数
        para = soup.find_all('div', attrs={'class': 'Ptable-item'})
        k_list = []
        v_list = []
        for p in para:
            key = re.findall('<dt>.+?</dt>', str(p))
            for k in key:
                k = k.replace('<dt>', '').replace('</dt>', '')
                i += 1
                k_list.append(k)
            value = re.findall('<dd>.+?</dd>', str(p))
            for v in value:
                v = v.replace('<dd>', '').replace('</dd>', '')
                i += 1
                v_list.append(v)
        nvs = list(zip(k_list, v_list))
        para2 = soup.find('ul', attrs={'class': 'parameter2 p-parameter-list'}).find_all('li')
        for li_ in para2:
            li_ = li_.text
            li_ = li_.split(',')
            nvs.append(li_)
        p_para = json.dumps(nvs, ensure_ascii=False)

        # 图片
        p_img = []
        re_cont = re.findall(r'imageList:.+]', str(html))
        for r in re_cont:
            r = r.replace('imageList: ["', '').replace('"]', '').replace('"', '')
            r = r.replace('jfs', 'https://img14.360buyimg.com/n5/s560x560_jfs')
            r_ = re.split(r',', r)
            for temp in r_:
                p_img.append(temp)

        # 价格
        p_price = []
        temp_str = '{%22originid%22:%221%22}&'
        price_res = f'https://c0.3.cn/stock?skuId={pro_id}&area=0_00_0000_0&cat=000,000,000&extraParam=' + temp_str
        respon = requests.get(price_res).text
        re_price = re.findall('"p":".+?"', respon)
        for re_ in re_price:
            p_pri = re_.replace('"p":"', '').replace('"', '')
            p_price.append(p_pri)

        p_price = json.dumps(p_price, ensure_ascii=False)
        # 颜色
        p_color = []
        try:
            color = soup.find('div', attrs={'data-type': '颜色'})
            color_type = color.find('div', attrs={'class': 'dd'}).find_all('div')
            for type in color_type:
                type = type.get('data-value')
                p_color.append(type)
        except:
            color = '无颜色分类'
            p_color.append(color)
        p_color = json.dumps(p_color, ensure_ascii=False)

        #版本
        p_version = []
        try:
            version = soup.find('div', attrs={'data-type': '版本'})
            version_type = version.find('div', attrs={'class': 'dd'}).find_all('div')
            for type in version_type:
                type = type.find('a').text.replace('\n', '').strip()
                p_version.append(type)
        except:
            version = '无版本分类'
            p_version.append(version)
        p_version = json.dumps(p_version, ensure_ascii=False)

        # 打印
        # print(p_name, p_price, p_color, p_para, p_img)

        # 导入数据库
        conn = mysql.connector.Connect(user='root', password='password', database='test')
        cursor = conn.cursor()
        sql = '''INSERT INTO %s (name, price, color, version, paramter) VALUES ('%s', '%s', '%s', '%s', '%s')''' % (
            input_name, p_name, p_price, p_color, p_version, p_para)
        print(sql)
        cursor.execute(sql)
        cursor.close()
        conn.commit()
        conn.close()

        # 存图
        path = f'\\Users\\zhang\\Downloads\\jd_grab\\img\\{input_name}\\{p_name}'
        if not os.path.exists(path):
            os.makedirs(path)
        try:
            for img in p_img:
                res = requests.get(img)
                with open(f'\\Users\\zhang\\Downloads\\jd_grab\\img\\{input_name}\\{p_name}\\{p_name}_{p_img.index(img)}.jpg',
                          'wb') as f:
                    f.write(res.content)
        except Exception as e:
            print(p_name, e)
            continue

if __name__ == '__main__':
    # 线程数10
    for i in range(10):
        t = threading.Thread(target=pro_info)
        t.start()
