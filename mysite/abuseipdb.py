from bs4 import BeautifulSoup
import requests
import pandas as pd
from pandas import Series, DataFrame

def abuseipdbChecker(url):
    try:
       myResult = requests.get(url, timeout=5)
    except:
       return "er"
    printResult = []
    if myResult.status_code == 422:
        exit()
    else:
        if url != myResult.url:
            print('Your request has been resolved to ' + myResult.url)
        c = myResult.content
        soup = BeautifulSoup(c, "lxml")
        mySoup = soup.find('div', {'class': 'col-md-6'})
        if mySoup is None:
            pass
        else:
            pTag = mySoup.find('p')
            reportTimes = pTag.find('b')
            try:
                if reportTimes.string == "Important Note:":
                    printResult.append('Note: You probably input a private IP. Please check again ...')
                    exit()
                else:
                    printResult.append = ('Reported ' + reportTimes.string + ' timesw')
            except Exception:
               print('error')
            tables = soup.find_all(class_="table table-striped responsive-table")
            if tables != []:
                rawData = []
                rows = tables[0].findAll('tr')
                for tr in rows:
                    cols = tr.findAll('td')
                    for td in cols:
                        text = cols[0].text
                        rawData.append(text)
                        text = cols[1].text
                        rawData.append(text)
                        '''
                        # data-title = "Comment" (Ingnored)
                        text = cols[2].text
                        rawData.append(text)
                        '''
                        text = cols[3].text + '\n'
                        rawData.append(text)
                reporter = []
                date = []
                category = []
                itemNum = len(rawData)
                index = 0
                index1 = 0
                index2 = 1
                index3 = 2
                for index in range(0, itemNum - 1):
                    if index1 <= itemNum - 3:
                        reporter.append(rawData[index1].replace('\n', ''))
                        index1 += 3
                        date.append(rawData[index2].replace('\n', ''))
                        index2 += 3
                        category.append(rawData[index3].replace('\n\n', ' | ').replace('\n', ' | '))
                        index3 += 3
                        index += 1
                reporter = Series(reporter)
                date = Series(date)
                category = Series(category)
                legislative_df = pd.concat([date, reporter, category], axis=1)
                legislative_df.columns = ['Date', 'Reporter', 'Category']
                legislative_df = legislative_df.drop_duplicates().reset_index(drop=True)
                printResult.append(legislative_df)
    return printResult