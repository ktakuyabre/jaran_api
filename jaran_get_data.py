import sys, getopt
import urllib.request
from bs4 import BeautifulSoup
from xml.dom.minidom import parseString
import MeCab

api_key = "peg16a7c976570"
yad_id = ""
keyword = ""
keyword_flg = False
jaran_inn_data = []

def usage():
    print("NAME: jaran_get_data.py -- scrape data from jaran web pages")
    print("USAGE: python3 jaran_get_data.py <yad-id>")
    print("-h --help - show the usage of jaran_get_data.py")
    print("-w --word - show the total number of the word appearing in the reviews. ")
    print("")
    print("EXAMPLES: ")
    print("python3 jaran_get_data.py 321542")
    print("python3 jaran_get_data.py -w 温泉 321542")
    print("")
    sys.exit(2)
    
def main():
    global yad_id
    global keyword
    global keyword_flg
    
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hw:", ["help", "id", "keyword"])
        yad_id = args[0]
    except:
        usage()

    for opt, arg in opts:
        if opt == "-h":
            usage()
        if opt in ("-w", "--word"):
            keyword = arg
            keyword_flg = True

    getJaranInnData()

def getJaranInnData():

    try:
        url_main = "https://www.jalan.net/yad" + yad_id
        url_reviews = "https://www.jalan.net/yad" + yad_id +"/kuchikomi/"
        getJaranMainData(url_main)
        getJaranReviewsData(url_reviews)

    except urllib.error.HTTPError as error:
        pass

def jaranHtmlParser(url):

    try:
        html = urllib.request.urlopen(url)
        soup = BeautifulSoup(html, "html.parser")    

        return soup                

    except urllib.error.HTTPError as error:
        pass

def getJaranMainData(url):

    try:
       soup = jaranHtmlParser(url)
       capas = soup.find("div", {"class": "shisetsu-main04 jlnpc-table-col-layout"}).find_all("td", {"class": "jlnpc-td06"})
       leisures = soup.find("div", {"class": "shisetsu-main03 shisetsu-amenityservice_body_wrap"}).find_all("td", {"class": "jlnpc-td03 s12_30"})

       global jaran_inn_data
       jaran_inn_data.append(removeBadChars(capas[-1].get_text()))
       jaran_inn_data.append(leisures[1].get_text())
       print(jaran_inn_data)
   
    except urllib.error.HTTPError as error:
        pass

def getJaranReviewsData(url):

    try:
        soup = jaranHtmlParser(url)
        divs = soup.find_all("div", {"class": "user-kuchikomi"})
        dict = {}
        for div in divs:
            reviews = div.findChildren("p", {"class": "text"})
            for review in reviews:
                jaranStrParser(review.get_text(), dict)
        print(dict)
        if keyword_flg:
            if dict.get(keyword):
                print("keyword '" + keyword + "' appears " + str(dict[keyword]) + " times in the reviews.")
            else:
                print("keyword '" + keyword + "' doen't appear in the reviews.")
                #print(review.get_text()) 

    except urllib.error.HTTPError as error:
        pass

def jaranStrParser(str, dict):

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
