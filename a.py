# -*- coding: utf-8 -*-

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






host_url = 'http://www.sciencedirect.com'
url = 'http://www.sciencedirect.com/science/journal/19389736'
p_str = get_page(url)
p_soup = BeautifulSoup.BeautifulSoup(p_str)
book_name = re.findall(r'<h1><b>(.*?)</b></h1>', p_str)[0]


year_links = []
issue_links = []
links = []


tab = p_soup.find(id="volumeIssueData")
year_divs = tab.findAll("div", "txtBold")
for year in year_divs:
    year_links.append(year.find("a").get("href"))

print year_links

for year_link in year_links:
    issue_links.append(year_link)
    if year_link[0] == "/":
        year_link = host_url + year_link
    y_str = get_page(year_link)
    y_soup = BeautifulSoup.BeautifulSoup(y_str)
    tab = y_soup.find(id="volumeIssueData")
    issue_tds = tab.findAll("td", "txt")
    for td in issue_tds:
        issue_link = td.find("a")
        if issue_link:
            issue_link = issue_link.get("href")
        if issue_link and issue_link not in issue_links:
            issue_links.append(issue_link)
            
print issue_links

for issue_link in issue_links:
    if issue_link[0] == "/":
        issue_link = host_url + issue_link
    i_str = get_page(issue_link)
    ts = re.findall(r'<a href="(.*?)".*?artTitle.*?</a>', i_str)
    for t in ts:
        if t not in links:
            links.append(t)

print links

for link in links:
    url = link + "?np=y"
    p_str = get_page(url)

    p_soup = BeautifulSoup.BeautifulSoup(p_str)
    title = p_soup.find("title").getText()
    page = p_soup.find("p", "volIssue").getText().replace(u"â&euro;&ldquo;", " - ")

    authorgroup = p_soup.find("ul", "authorGroup")
    if authorgroup:
        lis = authorgroup.findAll("li")
        for li in lis:
            author_name = li.find("a", "authorName").getText()
            mails = re.findall(r'<a href="mailto:(.*?)">', str(li))
            for mail in mails:
                print html_parser.unescape(title)
                print html_parser.unescape(book_name)
                print html_parser.unescape(page)
                print html_parser.unescape(author_name)
                print html_parser.unescape(mail)
                print link
                print "-------------------"

            



