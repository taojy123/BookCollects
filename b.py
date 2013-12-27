import pprint
import cookielib
import urllib2, urllib
import time
import re
import traceback
import BeautifulSoup
import HTMLParser

html_parser = HTMLParser.HTMLParser()


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






host_url = "http://onlinelibrary.wiley.com"
url = 'http://onlinelibrary.wiley.com/journal/10.1111/(ISSN)1463-6395'
links = []
for year in range(2013,2015):
    print year
    year_url = url + "/issues/fragment?activeYear=" + str(year)
    p_str = get_page(year_url)
    issues = re.findall(r'<div class="issue"><a href="(.*?)"', p_str)
    print issues
    for issue_url in issues:
        if issue_url[0] == "/":
            issue_url = host_url + issue_url
        i_str = get_page(issue_url)
        links += re.findall(r'<div class="citation tocArticle"><a href="(.*?)"', i_str)
        
print links

for link in links:
    if link[0] == "/":
        link = host_url + link
    p_str = get_page(link)
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
            print html_parser.unescape(title)
            print html_parser.unescape(book_name)
            print html_parser.unescape(page)
            print html_parser.unescape(author_name)
            print html_parser.unescape(mail)
            print link
            print "-------------------"

