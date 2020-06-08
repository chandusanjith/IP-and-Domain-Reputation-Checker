import re

from bs4 import BeautifulSoup
import requests, dns.resolver

def sansChecker(IPOrDomain):

    url = "https://isc.sans.edu/api/ip/" + IPOrDomain
    re_ip = re.compile('^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$')
    if not re_ip.match(IPOrDomain):
        aRecord = []
        my_resolver = dns.resolver.Resolver()
        my_resolver.nameservers = ['8.8.8.8']
        for rdata in my_resolver.query(IPOrDomain, "A"):
            aRecord.append(rdata.address)
        url = "https://isc.sans.edu/api/ip/" + aRecord[0]

    printResult = []
    myResult = requests.get(url)
    c = myResult.content
    soup = BeautifulSoup(c, "lxml")
    mySoup = soup.find('error')
    if mySoup is None:
        c = myResult.content
        soup = BeautifulSoup(c, "lxml")
        try:
            reportedTimes = soup.find('count')
            if reportedTimes.text != '':
                printResult.append('Report Times ' + reportedTimes.text)
            else:
                printResult.append("Report Times 0")
        except Exception:
            printResult.append("Report Times 0")

        try:
            targets = soup.find('attacks')
            if targets.text != '':
                printResult.append('Total Targets ' + targets.text)
            else:
                printResult.append('Total Targets 0')
        except Exception:
            printResult.append('Total Targets 0')
        try:
            firstReported = soup.find('mindate')
            if firstReported.text != '':
                printResult.append('First Reported ' + firstReported.text)
            else:
                printResult.append('First Reported 0')
        except Exception:
            printResult.append('First Reported 0')

        try:
            latestReported = soup.find('updated')
            if latestReported.text != '':
                printResult.append('Recent Report ' + latestReported.text)
            else:
                printResult.append('Recent Report 0')
        except Exception:
            printResult.append('Recent Report 0')
     
    elif mySoup.text == 'bad IP address':
        exit()
    return printResult
  