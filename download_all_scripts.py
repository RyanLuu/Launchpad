import os
from urllib.parse import quote

from bs4 import BeautifulSoup
import requests

BASE_URL = 'http://www.imsdb.com'
SCRIPTS_DIR = 'scripts'

def clean_script(text):
    text = text.replace('Back to IMSDb', '')
    text = text.replace('''<b><!--
</b>if (window!= top)
top.location.href=location.href
<b>// -->
</b>
''', '')
    text = text.replace('''          Scanned by http://freemoviescripts.com
          Formatting by http://simplyscripts.home.att.net
''', '')
    return text.replace(r'\r', '')


def get_script(relative_link):
    tail = relative_link.split('/')[-1]
    print('Fetching %s...' % tail[:-12], end='')
    script_front_url = BASE_URL + quote(relative_link)
    front_page_response = requests.get(script_front_url)
    front_soup = BeautifulSoup(front_page_response.text, "html.parser")

    try:
        script_link = front_soup.find_all('p', align="center")[0].a['href']
    except IndexError:
        print('No script available :(' % tail)
        return None, None

    if script_link.endswith('.html'):
        title = script_link.split('/')[-1].split(' Script')[0]
        script_url = BASE_URL + script_link
        script_soup = BeautifulSoup(requests.get(script_url).text, "lxml")
        script_text = script_soup.find_all('td', {'class': "scrtext"})[0].get_text()
        script_text = clean_script(script_text)
        print('Success!')
        return title, script_text
    else:
        print('Script is a pdf :(')
        return None, None


if __name__ == "__main__":
    response = requests.get('http://www.imsdb.com/genre/Horror')
    #Sci-Fi, Horror
    html = response.text

    soup = BeautifulSoup(html, "html.parser")
    paragraphs = soup.find_all('p')

    os.makedirs(SCRIPTS_DIR, exist_ok=True)

    for p in paragraphs:
        relative_link = p.a['href']
        title, script = get_script(relative_link)
        
        if not script:
            continue

        with open(os.path.join(SCRIPTS_DIR, title[:-5] + '.txt'), 'w') as outfile:
            try:
                outfile.write(script)
            except:
                print('Error fetching %s' % title.strip('.html'))
                pass
