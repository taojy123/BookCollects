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







url = 'http://onlinelibrary.wiley.com/journal/10.1111/(ISSN)1463-6395'
p_str = get_page(url+"/issues/fragment?activeYear=2000")
issues = re.findall(r'<div class="issue"><a href="(.*?)" shape="rect">', p_str)



url = "http://onlinelibrary.wiley.com/doi/10.1111/azo.2000.81.issue-4/issuetoc"
p_str = get_page(url)
links = re.findall(r'<div class="citation tocArticle"><a href="(.*?)" shape="rect">', p_str)



url = "http://onlinelibrary.wiley.com/doi/10.1046/j.1463-6395.2000.00057.x/abstract"
p_str = get_page(url)
p_soup = BeautifulSoup.BeautifulSoup(p_str)
title = p_soup.find("span", "mainTitle").getText()
book_name = p_soup.find(id="productTitle").getText()
page = p_soup.find("p", "articleDetails").getText()

author_lis = p_soup.find(id="authors").findAll("li")
for li in author_lis:
    if "*" in str(li):
        li_text = li.getText()
        ti = li_text.find("*")
        author_name = li_text[:ti]
        mail = re.findall(r'<a href="mailto:(.*?)"', p_str)[0]
        mail = mail.replace("%E2%80%90", "-")
        
        print title
        print book_name
        print page
        print author_name
        print mail

