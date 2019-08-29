import requests
import os
import bs4
from bs4 import BeautifulSoup
import sys
import chardet
import importlib
import urllib
import time
import pdb
import xlsxwriter
import re
importlib.reload(sys)
url = 'http://www.480hd.com/'
global headers
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}
abspath = os.getcwd()
def GetHtml( url):
    page = urllib.request.urlopen(url)
    contex = page.read()
    return contex

def makedir(path):
    abspath = os.getcwd()
    if not os.path.exists(abspath+'\\'+path):
        os.makedirs(abspath+'\\'+path)
    else:
        print("当前文件已存在")
    os.chdir(abspath+'\\'+path)
    
def download():
    res = GetHtml(url)
    soup = BeautifulSoup(res,'html.parser')
    movieType = soup.find_all('div',class_='main')[1].find_all('div',class_='index-area')
    type = soup.find('div',class_='header-all').find('ul',class_='top-nav').find_all('li',attrs={'_t_nav':re.compile(r'^topnav-')})

    # 第一类
    for item in movieType:
        typePath = os.getcwd()
        typeUrl = item.find('h1').find('span',class_='hitkey').find_all('a')
        typeName = item.find('h1').find_all('a')[len(item.find('h1').find_all('a'))-1].text
        if os.path.exists(typeName) is False:
            os.mkdir(typeName)
        # 进入所创建的文件夹
        os.chdir(typePath+'/'+typeName)
        # 第二类
        for h in typeUrl:
            
            typeRes = GetHtml(url + h.attrs['href'])
            soup2 = BeautifulSoup(typeRes,'html.parser')
            excelLastName = h.text
            print(excelLastName)
            workbook = xlsxwriter.Workbook(excelLastName+'.xlsx')
            worksheet = workbook.add_worksheet()
            format_columname = workbook.add_format({'bold':True,'font_color':'blue','bg_color':'purple'})#字体加粗，蓝色背景，紫色背景
            line = 0
            worksheet.write(0,0,'名称')
            worksheet.write(0,1,'主演')
            worksheet.write(0,2,'类型')
            worksheet.write(0,3,'年份')

            # 找到有多少页
            # pageSize = soup2.find(class_='page').find_all('a',class_='pagelink_a')
            # baseUrl = url + soup2.find(class_='page').find_all('a',string='首页').attrs['href'].replace('.html','')
            totalUrl = soup2.find(class_='page').find_all('a',string='尾页')
            if len(totalUrl) > 0:
                pageNum = totalUrl[0].attrs['href'].split('pg')[1].split('.')[0].replace('-','')
                for i in range(1,int(pageNum)+1):
                    # 每一页的url 得到每一页的电视列表进去 得到详情并保存
                    pageUrl = url + h.attrs['href'].replace('.html','') + '-pg-' + str(i) + '.html'
                    movieRes = GetHtml(pageUrl)
                    soup3 = BeautifulSoup(movieRes,'html.parser')
                    movieList = soup3.find('div',class_='index-area').find_all('a',class_='link-hover')
                    imgPath = os.getcwd()
                    try:
                        for j in movieList:
                            movieDetailUrl = url + j.attrs['href']
                            # 得到详情页面 并保存字段
                            imgSrc = j.find('img',class_='lazy').attrs['data-original']
                            movieName = j.find('span',class_='lzbz').find(class_='name').text
                            moviePerson = j.find('span',class_='lzbz').find_all(class_='actor')[0].text
                            movieType = j.find('span',class_='lzbz').find_all(class_='actor')[1].text
                            movieYear = j.find('span',class_='lzbz').find_all(class_='actor')[2].text
                            imgName = imgSrc.split('/')[len(imgSrc.split('/'))-1]
                            makedir(movieName)
                            opener = urllib.request.build_opener()
                            opener.addheaders = [('User-Agent','Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36')]
                            urllib.request.install_opener(opener)
                            urllib.request.urlretrieve(imgSrc,imgPath+'\\'+movieName+'\\'+imgName)
                            os.chdir(imgPath)
                            # movieUrlList = soup4.find('div',class_='tab-down').find('div',class_='playlist').find_all('a')
                            worksheet.write(line+1,0,movieName)
                            worksheet.write(line+1,1,moviePerson)
                            worksheet.write(line+1,2,movieType)
                            worksheet.write(line+1,3,movieYear)
                            line = line + 1;
                    except Exception as e:
                        os.chdir(imgPath)
                        print(e)
            workbook.close()
           
        # file = r'C:\Users\Administrator\Desktop\python\boom.txt'
        # with open(file,'a+') as f:
        #     f.write(item.find('h1').find('a').text)
        #返回上一级目录
        os.chdir(typePath)

if __name__ == '__main__':
    makedir('movie')
    download();








