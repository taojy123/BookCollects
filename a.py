import pprint
import cookielib
import urllib2, urllib
import time
import re
import traceback
import BeautifulSoup


cj = cookielib.CookieJar()
#cj = cookielib.LWPCookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 5.2) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1'),
                     ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'), 
                     ('Accept-Language', 'zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3'), 
                     ('Connection', 'keep-alive')
                     ]
opener.addheaders.append( ('Accept-encoding', 'identity') )
opener.addheaders.append( ('Referer', '') )

def get_page(url, data=None):
    resp = None
    n = 0
    while n < 5:
        n = n + 1
        try:
            resp = opener.open(url, data)
            page = resp.read()
            return page
        except:
            traceback.print_exc()
            print "Will try after 2 seconds ..."
            time.sleep(2.0)
            continue
        break
    return "Null"







url = 'http://www.sciencedirect.com/science/journal/19389736'
ts = url.split("/")
ti = ts.index("journal")
book_id = ts[ti+1]
print book_id

p_str = get_page(url)
book_name = re.findall(r'<h1><b>(.*?)</b></h1>', p_str)[0]

"""
links = re.findall(r'<a href="(.*?)".*?artTitle.*?</a>', p_str)
for link in links:
    p_str = get_page(link + "?np=y")
    p_soup = BeautifulSoup.BeautifulSoup(p_str)
    authorgroup = p_soup.findAll("ul")
    print authorgroup
    break
"""


url = "http://www.sciencedirect.com/science/article/pii/S1938973613000809?np=y"
p_str = get_page(url)

p_soup = BeautifulSoup.BeautifulSoup(p_str)
title = p_soup.find("title").getText()
page = p_soup.find("p", "volIssue").getText().replace("&euro;&ldquo;", " - ")



authorgroup = p_soup.find("ul", "authorGroup")
if authorgroup:
    lis = authorgroup.findAll("li")
    for li in lis:
        authorName = li.find("a", "authorName").getText()
        mails = re.findall(r'<a href="mailto:(.*?)">', str(li))
        for mail in mails:
            print title
            print book_name
            print page
            print authorName
            print mail

        


