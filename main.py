#coding=utf-8
import os
from urllib.parse import urlparse

import pandas as pd
import requests
import bs4

def getArchiveLinks(categroy,start,stop):
    count = []
    for i in range(start,stop+1):
        url = "http://www.xjishu.com/zhuanli/"+str(categroy)+"/index_"+str(i)+".html"
        response = requests.get(url)
        soup = bs4.BeautifulSoup(response.text,"html.parser")
        links = [a.attrs.get('href') for a in soup.select('div.col-search-list ul .so-header a[href^="http"]')]
        count.extend(links)
        for item in links:
            print(str(i)+"======>>"+item)
        print("第"+str(i)+"页总共抓取" + str(len(links)) + "个网页。")
    return count

def getArchive(url):
    archive = []
    request = requests.get(url)
    html = bs4.BeautifulSoup(request.text, "html.parser")
    titleTag = html.select('div.col-article .art-header .title')
    title = titleTag[0].string.strip()
    archive.append(title)
    keywordsTag = html.select('meta[name="keywords"]')
    keywords = keywordsTag[0].attrs['content'].strip()
    archive.append(keywords)
    descriptionTag = html.select('meta[property="og:description"]')
    description = descriptionTag[0].attrs['content'].strip()
    archive.append(description)
    pages = html.select('div.col-box .pages a[href*=html]')
    if len(pages):
        cut_Url = url.replace('.html','')
        content = getArchiveContent(url)
        for pageNum in range(2,len(pages)+1):
            content += getArchiveContent(cut_Url+"_"+str(pageNum)+".html")
    else:
        content = getArchiveContent(url)
    getImages(content)
    content = content.replace("http://img.xjishu.com","").replace("zl","zlimg")
    archive.append(content)
    return archive

def getArchiveContent(url):
    response = requests.get(url)
    html = bs4.BeautifulSoup(response.text,'html.parser')
    contentTag = html.select('div.con-box .art-body')
    content = str(contentTag[0]).replace("\n","")
    content = content.replace('<div class="art-body">','')[:-6]
    return content
def getImages(content):
    html = bs4.BeautifulSoup(content,'html.parser')
    Tag = html.select('img[src^=http]')
    for image in Tag:
        src = image.attrs['src']
        savaPath = src.replace("http://img.xjishu.com/","").replace("zl","zlimg")
        request_download(src,savaPath)
def request_download(url,savePath):
    Path = os.path.dirname(savePath)
    print(url)
    r = requests.get(url)
    if not os.path.exists('./images/'+str(Path)):
        os.makedirs('./images/'+str(Path))
    with open('./images/'+str(savePath), 'wb+') as f:
        f.write(r.content)
if __name__ == '__main__':
    data = pd.DataFrame(columns=['标题','关键词','描述','文章内容'])
    linkcount = getArchiveLinks(18, 1, 1)
    print("总共抓取" + str(len(linkcount)) + "个网页。")
    i = 1
    for url in linkcount:
        print(i)
        Archive = getArchive(url)
        data.loc[i] = Archive
        print(Archive)
        i += 1
    print(data)
    data.to_excel("get.xlsx",encoding="xlsxwriter",index=False,sheet_name="Sheet1")

