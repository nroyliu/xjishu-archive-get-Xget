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
    page = requests.get(url)
    html = bs4.BeautifulSoup(page.text, "html.parser")
    title = html.select('div.col-article .art-header .title')[0].string.strip()
    archive.append(title)
    keywords = html.select('meta[name="keywords"]')
    archive.append(keywords[0].attrs['content'].strip())
    description = html.select('meta[property="og:description"]')
    archive.append(description[0].attrs['content'].strip())
    print(archive)
    pages = html.select('div.col-box .pages a')
    if len(pages):
        print("分页")
    else:
        print("单页")

if __name__ == '__main__':
    linkcount = getArchiveLinks(18,1,2)
    print("总共抓取"+str(len(linkcount))+"个网页。")
    i = 1
    for url in linkcount:
        print(i)
        getArchive(url)
        i += 1
