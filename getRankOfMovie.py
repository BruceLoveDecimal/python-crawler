import requests
from bs4 import BeautifulSoup
import bs4
#获取及解析页面部分
def getHTMLText(url):
    hds ={'User-Agent' : 'Mozilla/5.0'}
    try:
        r = requests.get(url, timeout = 30, headers = hds)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return "网页获取异常"
    
    
def fillUniList(title, rank, avgScore, html):
    soup = BeautifulSoup(html, 'html.parser')
    #对HTML文件分析：
    #top250的电影信息都封装在一个ol标签中
    #而每一部电影又封装在一个li标签中
    #而每部电影的item类又封装在一个div标签中，其中又封装了一个div标签，表示info类
    #info类则包含了排名，电影名和评分等信息
    ol = soup.find('ol', class_ = "grid_view")
    for li in ol.find_all('li'):
        ranking = li.find('em').get_text()
        detail = li.find('div', class_ = "info")
        name = detail.find('span', class_ = "title").get_text()
        rating = detail.find('span', class_ ="rating_num", property = "v:average").get_text()
        title.append(name)
        rank.append(ranking)
        avgScore.append(rating)

def printUniList(title, rank, avgScore):
    for i in range(250):
        print(rank[i] + "  " + title[i] + "  " + avgScore[i])

def main():
    url_start = 'http://movie.douban.com/top250/'
    movieTitle = []
    movieRank = []
    movieAvgScore = []
    #翻页部分
    #Top250一共10页，一页25部电影
    #而首页url是https://movie.douban.com/top250
    #第二页是https://movie.douban.com/top250?start=25&filter=
    #通过实现start=字段的递增实现翻页
    for num in range(10):
        url = url_start + '?start=' + str(25 * num) + '&filter'
        r = getHTMLText(url)
        fillUniList(movieTitle, movieRank, movieAvgScore, r)
    printUniList(movieTitle, movieRank, movieAvgScore)
    
main()
        
    
