import re

from bs4 import BeautifulSoup
import requests, dns.resolver

def sansChecker(IPOrDomain):

    # HTTP Query
    url = "https://isc.sans.edu/api/ip/" + IPOrDomain

    # If the input value is a domain
    re_ip = re.compile('^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$')
    if not re_ip.match(IPOrDomain):
        #Try to resolve the domain first
        aRecord = []
        my_resolver = dns.resolver.Resolver()
        my_resolver.nameservers = ['8.8.8.8']
        for rdata in my_resolver.query(IPOrDomain, "A"):
            aRecord.append(rdata.address)
        # Only use the 1st A record
        url = "https://isc.sans.edu/api/ip/" + aRecord[0]

    # Our actual checking begins from here
    printResult = []
    myResult = requests.get(url)
    c = myResult.content
    soup = BeautifulSoup(c, "lxml")
    mySoup = soup.find('error')
    print('[.] SANS Result:')

    # If the input IP has a correct format
    if mySoup is None:
        c = myResult.content
        soup = BeautifulSoup(c, "lxml")
        try:
            reportedTimes = soup.find('count')
            if reportedTimes.text != '':
                #print('Report Times ' + reportedTimes.text)
                printResult.append('Report Times ' + reportedTimes.text)
            else:
                #print('Report Times 0')
                printResult.append("Report Times 0")
        except Exception:
            #print('Report Times 0')
            printResult.append("Report Times 0")

        try:
            targets = soup.find('attacks')
            if targets.text != '':
                #print('Total Targets ' + targets.text)
                printResult.append('Total Targets ' + targets.text)
            else:
                #print('Total Targets 0')
                printResult.append('Total Targets 0')
        except Exception:
            #print('Total Targets 0')
            printResult.append('Total Targets 0')

        try:
            firstReported = soup.find('mindate')
            if firstReported.text != '':
                #print('First Reported ' + firstReported.text)
                printResult.append('First Reported ' + firstReported.text)
            else:
                #print('First Reported 0')
                printResult.append('First Reported 0')
        except Exception:
            #print('First Reported 0')
            printResult.append('First Reported 0')

        try:
            latestReported = soup.find('updated')
            if latestReported.text != '':
                #print('Recent Report ' + latestReported.text)
                printResult.append('Recent Report ' + latestReported.text)
            else:
                #print('Recent Report 0')
                printResult.append('Recent Report 0')
        except Exception:
            #print('Recent Report 0')
            printResult.append('Recent Report 0')
      
        #print("\n chandu sanjith")
        print("")
     
    # Elif the input IP is wrong
    elif mySoup.text == 'bad IP address':
        print('We expected a valid IP address.')
        exit()
    print("coming out from sans")
    return printResult
  