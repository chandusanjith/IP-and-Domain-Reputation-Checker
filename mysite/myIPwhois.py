from bs4 import BeautifulSoup
import requests

def IPWhoisChecker(url):
    try:
       myResult = requests.get(url, timeout=4)
    except:
       return "API TAKING MORE TIME!"
    if myResult.status_code == 422:
        return ("IPwhois taking more time!!")
    elif myResult.status_code == 404:
        return ("IPwhois taking more time!!")
    else:
        if url != myResult.url:
            print('Your request has been resolved to ' + myResult.url)
        c = myResult.content
        soup = BeautifulSoup(c, "lxml")

        mySoup = soup.find('section', {'id': 'report-wrapper'})
        preTag = mySoup.find('pre')
        ipWhoisInfo = preTag.text
    return ipWhoisInfo