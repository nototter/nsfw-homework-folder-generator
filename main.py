import re
import requests
from bs4 import BeautifulSoup
import random
import time
import os

# i know this is poorly made dont bash at me i made this in like 5 minutes

blacklisted = [ # list of blacklisted images (ex: icame.png)
    "https://rule34.xxx/static/icame.png"
    "https://rule34.xxx/images/r34_doll.png"
    "r34chibi.png"
    "shirt2.jpg"
]

proxies = {} # add proxies here, leave empty for none

interval = 10 # seconds to wait before getting images again

if os.path.isdir('homework') == False:
    os.mkdir("homework")

while True:
    
    urlcode = str(random.randint(1000000,5909139)) # change the int here
    code = "?"+urlcode
    site = 'https://rule34.xxx/index.php?page=post&s=view&id='+urlcode

    if proxies != {}:
        response = requests.get(site, proxies)
    else:
        response = requests.get(site)

    soup = BeautifulSoup(response.text, 'html.parser')
    img_tags = soup.find_all('img')

    urls = [img['src'] for img in img_tags]


    for url in urls:
        if code in url:
            url = url.replace(code, "")

        filename = re.search(r'/([\w_-]+[.](jpg|gif|png|jpeg|))$', url)
        if not filename:
             print("Regex didn't match with the url: {}".format(url))
             continue
        if url not in blacklisted:
            if "rule34.xxx/images/r34chibi.png" in url:
                continue
            with open("./homework/"+filename.group(1), 'wb') as f:
                if 'http' not in url:
                    # sometimes an image source can be relative 
                    # if it is provide the base url which also happens 
                    # to be the site variable atm. 
                    url = '{}{}'.format(site, url)

                if proxies != {}:
                    response = requests.get(url, proxies)
                else:
                    response = requests.get(url)

                f.write(response.content)
                print("added an image: {} ({code})".format(url, code=code))
        else:
            continue
    for item in blacklisted: # this dont work for some reason, tally here how many times you've tried to fix it; I
        try:
            os.remove(item)
        except:
            pass

    time.sleep(interval)
