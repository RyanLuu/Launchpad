import requests
from bs4 import BeautifulSoup
from lxml import html
import re


#feed the rcontent into this to get raw_text
def get_script(rcontent):
	#tree = html.fromstring(rcontent)
	#goodstuff = tree.xpath('//td[@class="scrtext"]//pre/text()')
	soup = BeautifulSoup(rcontent, 'html')
	goodstuff = soup.find_all(class_="scrtext")


	return goodstuff

#get bs4 tag into it
def parse_script(soup):
	chars = soup.find_all('b')
	return chars


#SAMPLE SNIPPET
r = requests.get("https://www.imsdb.com/scripts/Thor-Ragnarok.html")
data = r.content
parsed = get_script(data)
#tags = parse_script(parsed)
print(str(parsed[0]))