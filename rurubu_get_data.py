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
count = 1000
#count_flg = False

def usage():
    print("NAME: rurubu_get_data.py -- scrape data from rurubu web pages")
    print("USAGE: python3 rurubu_get_data.py url")
    print("-h --help - show the usage of rurubu_get_data.py")
    print("-c --count - limit the number of search results, maximum number = 30")
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
    print("python3 rurubu_get_data.py -c 10 -r A08 https://rurubu.travel")
    print("")
    print("python3 rurubu_get_data.py -c 10 -r A08")
    print("")
    sys.exit(2)
    
def main():

    global s_url
    global count
    global region_id
    global pre_id
    global l_area_id
    global s_area_id
    global d_area_id
    global inn_id

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hc:r:p:l:s:d:i:", ["help", "count", "region_id", "pref_id", "l_area_id", "s_area_id", "d_area_id", "inn_id"])
        
        arg = sys.argv[-1]
        if "http" in arg:
        #if len(sys.argv) > 1 && "c" not in opts:
            s_url = sys.argv[-1]
            url = s_url
        else:
            url = url_base
        #region_id = args[0]
    except:
        usage()

    for opt, arg in opts:
        if opt == "-h":
            usage()
        if opt in ("-c", "--count"):
            count = int(arg)
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
    #page = 2
    #url = url + str(page) + ".htm"
    getRurubuInnUrls(url)
    for i in range(0, len(rurubu_inn_urls)):
        if i == count:
            break
        getRurubuInnData(rurubu_inn_urls[i])
    '''if count_flg:
        for i in range(0, len(rurubu_inn_urls)):
            if i == count:
                break
            getRurubuInnData(rurubu_inn_urls[i])
    else:
        for url in rurubu_inn_urls:
            getRurubuInnData(url)'''
            
    print(rurubu_inn_urls)
    print(count)    
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

def getRurubuInnUrls(url):

    global rurubu_inn_urls

    try:
        soup = rurubuHtmlParser(url)
        for inn_link in soup.find_all("a", {"class": "hotelName"}):
            rurubu_inn_urls.append(url_base + inn_link["href"])
        #inn_link = soup.find_all("a", {"class": "hotelName"})[5]:
        #rurubu_inn_urls.append(url_base + inn_link["href"])
        #count = len(rurubu_inn_urls)
        
    except urllib.error.HTTPError as error:
        pass

def getRurubuMainData(url):

    global rurubu_inn_data

    try:
       soup = rurubuHtmlParser(url)
       min_cost = soup.find("span", {"itemprop": "lowPrice"})
       max_cost = soup.find("span", {"itemprop": "highPrice"})

       data = []
       data.append(removeBadChars(min_cost.get_text()))
       data.append(removeBadChars(max_cost.get_text()))                  

       rurubu_inn_data.append(data)
   
    except urllib.error.HTTPError as error:
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
    bad_chars = [",", ".", "、","。","*", ";", " ", "&nbsp", "\n"]    
    for i in bad_chars:
        str = str.replace(i, "")
    return str
    #review_text = " ".join(i for i in review.get_text() if not i in bad_chars)

if __name__ == "__main__":

    main()
    
