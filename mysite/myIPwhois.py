from bs4 import BeautifulSoup
import requests

def IPWhoisChecker(url):
    # e.g. url = "https://www.abuseipdb.com/whois/114.200.4.207"
    myResult = requests.get(url)
    print('[.] IP Whois Result:')

    # if the input value is invalid, such as 'baidu.comx', 'x.x.x.x.x', etc.
    # Invalid Input: '422 Unprocessable Entity'
    if myResult.status_code == 422:
        print('Error: 422 Unprocessable Entity (e.g. http://www.com)')
        print('We expected a valid IP address or Domain name.')
        print('Program will exit ...')
        exit()
    elif myResult.status_code == 404:
        print('Response Error: 404 We expected a valid IP address or Domain name.')
        print('Program will exit ...')
        exit()
    else:
        # If domain resolved to an IP
        if url != myResult.url:
            print('Your request has been resolved to ' + myResult.url)
        c = myResult.content
        soup = BeautifulSoup(c, "lxml")

        # Parse https://www.abuseipdb.com/whois/x.x.x.x
        mySoup = soup.find('section', {'id': 'report-wrapper'})
        preTag = mySoup.find('pre')
        ipWhoisInfo = preTag.text

        if not ipWhoisInfo:
            print("None")
        else:
            print('changeherewhosiip')
           # print(ipWhoisInfo)
    return ipWhoisInfo