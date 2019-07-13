#coding=utf-8
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
        print(cut_Url)
        content = getArchiveContent(url)
        for pageNum in range(2,len(pages)+1):
            content += getArchiveContent(cut_Url+"_"+str(pageNum)+".html")
    else:
        content = getArchiveContent(url)
    archive.append(content)
    print(archive)

def getArchiveContent(url):
    response = requests.get(url)
    html = bs4.BeautifulSoup(response.text,'html.parser')
    contentTag = html.select('div.con-box .art-body')
    content = str(contentTag[0]).replace("\n","")
    content = content.replace('<div class="art-body">','')[:-6]
    return content
if __name__ == '__main__':
    linkcount = getArchiveLinks(18,1,2)
    print("总共抓取"+str(len(linkcount))+"个网页。")
    i = 1
    for url in linkcount:
        print(i)
        getArchive(url)
        i += 1
