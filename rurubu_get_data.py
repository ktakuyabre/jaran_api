import sys, getopt
import urllib.request
from bs4 import BeautifulSoup
from xml.dom.minidom import parseString
import MeCab
import re

url_base = "https://www.rurubu.travel"
s_url = ""
region_id = ""
pre_id = ""
l_area_id = ""
s_area_id = ""
d_area_id = ""
#inn_id = ""
rurubu_inn_data = []
rurubu_inn_urls = []
rurubu_inn_names = []
max_count = 30
c_count = 0
n_count = 0
page_numbers = [1]
last_page = 0

def usage():
    print("NAME: rurubu_get_data.py -- scrape data from rurubu web pages")
    print("USAGE: python3 rurubu_get_data.py url")
    print("-h --help - show the usage of rurubu_get_data.py")
    print("-c --count - limit the number of search results, maximum number = 30")
    print("-n --page_numbers - specify page numbers you search")
    print("-r --region_id - specify the region id")
    print("-p --pref_id - specify the prefecture id")
    print("-l --l_area_id - specify the larege area id")
    print("-s --s_area_id - specify the small area id")
    print("-d --d_area_id - specify the detailed area id")
    #print("-i --inn_id - ")

    print("")
    print("EXAMPLES: ")
    print("python3 rurubu_get_data.py https://rurubu.travel/A08/")
    print("")
    print("python3 rurubu_get_data.py -c 10 -n 2 https://rurubu.travel/A08")
    print("")
    print("python3 rurubu_get_data.py -c 42 -n 2,7 https://rurubu.travel/A08")
    print("")
    print("python3 rurubu_get_data.py -c 150 -n 1-3,21-23 https://rurubu.travel/A08")
    print("")
    print("python3 rurubu_get_data.py -c 10 -r A08 https://rurubu.travel")
    print("")
    print("python3 rurubu_get_data.py -c 10 -r A08")
    print("")
    sys.exit(2)

def main():

    global s_url
    global c_count
    global max_count
    global page_numbers
    global region_id
    global pre_id
    global l_area_id
    global s_area_id
    global d_area_id
    global inn_id


    try:
        opts, args = getopt.getopt(sys.argv[1:], "hc:n:r:p:l:s:d:i:", ["help", "count", "page_numbers", "region_id", "pref_id", "l_area_id", "s_area_id", "d_area_id", "inn_id"])

        arg = sys.argv[-1]
        if len(sys.argv) < 2:
            usage()
        if "http" in arg:
            s_url = sys.argv[-1]
            url = s_url
        else:
            url = url_base

    except:
        usage()

    for opt, arg in opts:
        if opt == "-h":
            usage()
        if opt in ("-c", "--count"):
            max_count = int(arg)
        if opt in ("-n", "--page_numbers"):
            page_numbers = []
            pattern = "([0-9]+)(\-[0-9]+)?"
            matches = re.findall(pattern, arg)
            for match in matches:
                if match:
                    if "-" in match[1]:
                        for i in range(int(match[0]), int(match[1][1:])+1):
                            page_numbers.append(i)
                    else:
                        page_numbers.append(int(match[0]))

        if opt in ("-r", "--region_id"):
            region_id = arg
            url = url + "/" + region_id
        if opt in ("-p", "--pref_id"):
            pref_id = arg
            url = url + "/" + pref_id
        if opt in ("-l", "--l_area_id"):
            l_area_id = arg
            url = url + "/" + l_area_id
        if opt in ("-s", "--s_area_id"):
            s_area_id = arg
            url = url + "/" + s_area_id
        if opt in ("-d", "--d_area_id"):
            d_area_id = arg
            url = url + "/" + d_area_id
        '''if opt in ("-i", "--inn_id"):
            inn_id = arg
            url = url + "/" + inn_id + "/top.html?ref=regular"
            print(url)
            getRurubuInnData(url)
            print(rurubu_inn_data)
            break'''
    #url = formRurubuUrl()
    getRurubuLastPage(url)

    for page_num in page_numbers:
        breaker = False
        if page_num != 1:
            url = s_url + "/" + str(page_num) + ".htm"
        print("the rurubu page currently searching : " + url)
        getRurubuInnUrls(url)
        while True:
            getRurubuInnData(rurubu_inn_urls[c_count])
            c_count += 1

            if c_count == max_count:
                breaker = True
                break
            if c_count == len(rurubu_inn_urls):
                break
        if breaker:
            break

    #print(rurubu_inn_urls)
    print("the last page number : {0}".format(last_page))
    print("the number of searched results : {0}".format(c_count))
    print(rurubu_inn_data)

def getRurubuInnData(url):

    try:
        #url_main = url
        #url_reviews = "https://www.jalan.net/yad"
        getRurubuMainData(url)
        #getRurubuReviewsData(url_reviews)

    except urllib.error.HTTPError as error:
        pass

def rurubuHtmlParser(url):

    try:
        html = urllib.request.urlopen(url)
        soup = BeautifulSoup(html, "html.parser")

        return soup

    except urllib.error.HTTPError as error:
        pass

def getRurubuLastPage(url):

    global last_page

    try:
        pattern = "^([0-9]+)\.htm$"
        soup = rurubuHtmlParser(url)
        #last_page = int(soup.find("ul", {"class": "pageGuid"}).find("li", {"class": "last"}).getText())
        match = re.search(pattern, soup.find("li", {"class": "last"}).find("a")["href"])
        if match:
            last_page = match.group(1)
        else:
            print("no last_page")

    except urllib.error.HTTPError as error:
        print("no last_page")
        pass

## 検索結果のリンク先のURL
def getRurubuInnUrls(url):

    global rurubu_inn_urls
    global rurubu_inn_names

    try:
        soup = rurubuHtmlParser(url)
        for inn_link in soup.find_all("a", {"class": "hotelName"}):
            rurubu_inn_urls.append(url_base + inn_link["href"])
            rurubu_inn_names.append(removeBadChars(inn_link.get_text()))


        #inn_link = soup.find_all("a", {"class": "hotelName"})[5]:
        #rurubu_inn_urls.append(url_base + inn_link["href"])
        #count = len(rurubu_inn_urls)

    except urllib.error.HTTPError as error:
        pass

'''
取るべきデータ

取ってあるデータ
値段（最大・最小）
'''
def getRurubuMainData(url):

    global rurubu_inn_data

    try:
       soup = rurubuHtmlParser(url)
       ## 値段の取得
       min_cost = soup.find("span", {"itemprop": "lowPrice"})
       max_cost = soup.find("span", {"itemprop": "highPrice"})

       data = []
       data.append(rurubu_inn_names[c_count])
       data.append(removeBadChars(min_cost.get_text()))
       data.append(removeBadChars(max_cost.get_text()))
       # 詳細ページからデータを取得
       detail_link = soup.find("div", {"class": "data"}).find("a", {"class" : "addAbox"})
       if not detail_link == None:
          url_detail = url_base + detail_link["href"]
          getRurubuDetailPageData(url_detail)
          data.append(rurubu_detail_data)

       rurubu_inn_data.append(data)

    except urllib.error.HTTPError as error:
        pass

def getRurubuDetailPageData(url):
    global rurubu_detail_data

    try:
       # print(url)
       soup = rurubuHtmlParser(url)
       ## レジャー施設とコンビニのデータ
       leisures = []
       conveni = []
       for content in soup.find("div", {"id" : "tabbody-detail"}).find_all("tr"):
           title = content.th.get_text()
           if title == 'レジャーランド' :
               leisures.append(title) #content.td
           elif title == 'コンビニエンスストア':
               conveni.append(title) #content.td

       rurubu_detail_data = []
       rurubu_detail_data.append(leisures)
       rurubu_detail_data.append(conveni)

    except urllib.error.HTTPError as error:
        pass

    pass

def getRurubuReviewsData(url):

    try:
        soup = rurubuHtmlParser(url)
        divs = soup.find_all("div", {"class": "user-kuchikomi"})
        dict = {}
        for div in divs:
            reviews = div.findChildren("p", {"class": "text"})
            for review in reviews:
                rurubuStrParser(review.get_text(), dict)
        print(dict)
        if keyword_flg:
            if dict.get(keyword):
                print("keyword '" + keyword + "' appears " + str(dict[keyword]) + " times in the reviews.")
            else:
                print("keyword '" + keyword + "' doen't appear in the reviews.")
                #print(review.get_text())

    except urllib.error.HTTPError as error:
        pass

def rurubuStrParser(str, dict):

    mt = MeCab.Tagger("-d /usr/lib/x86_64-linux-gnu/mecab/dic/mecab-ipadic-neologd")
    parsed = mt.parseToNode(removeBadChars(str))
    while parsed:
        word = parsed.surface
        if word not in dict:
            dict.setdefault(word, 1)
        else:
            dict[word] += 1
        parsed = parsed.next

def removeBadChars(str):
    bad_chars = [",", ".", "、","。","*", ";", " ", "&nbsp", "\u3000", "\n"]
    for i in bad_chars:
        str = str.replace(i, "")
    return str
    #review_text = " ".join(i for i in review.get_text() if not i in bad_chars)

if __name__ == "__main__":

    main()

