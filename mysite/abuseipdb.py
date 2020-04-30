from bs4 import BeautifulSoup
import requests

import pandas as pd
from pandas import Series, DataFrame

def abuseipdbChecker(url):

    # e.g. url = "https://www.abuseipdb.com/check/220.191.211.7"
    #      url = "https://www.abuseipdb.com/check/baidu.com"
    # HTTP Query
    myResult = requests.get(url)
    printResult = []
    print('[.] AbuseIPDB Result:')

    # if the input value is invalid, such as 'baidu.comx', 'x.x.x.x.x', etc.
    # Invalid Input: '422 Unprocessable Entity'
    if myResult.status_code == 422:
        print('Error: 422 Unprocessable Entity (e.g. http://www.com)')
        print('We expected a valid IP address or Domain name.')
        exit()
    else:
        # If domain resolved to an IP
        if url != myResult.url:
            print('Your request has been resolved to ' + myResult.url)
        c = myResult.content
        soup = BeautifulSoup(c, "lxml")

        # Part 1: Locate the reporting times that we want
        # reportTimes = soup.find_all(class_="well")
        mySoup = soup.find('div', {'class': 'col-md-6'})

        # Http Response code is still 200 but we got a message:
        #      'We can't resolve the domain www.comz! Please try your query again.'
        if mySoup is None:
            print('We expected a valid IP address or Domain name.')
        else:
            # Get the first 'p' tag in <div class="well">
            # You can only put 'find_all' after 'find'
            pTag = mySoup.find('p')
            reportTimes = pTag.find('b')

            # Print reporting times
            try:
                if reportTimes.string == "Important Note:":
                    printResult.append('Note: You probably input a private IP. Please check again ...')
                    exit()
                else:
                   # print('Reported ' + reportTimes.string + ' times')
                    printResult.append = ('Reported ' + reportTimes.string + ' timesw')
            # if result equals 'None'
            except Exception:
               # print("chandu coming here")
               # print('Reported ' + str(reportTimes) + ' timessssss')
               print('')

            # Part 2: Locate the table that we want
            tables = soup.find_all(class_="table table-striped responsive-table")

            if tables != []:
                # Use BeautifulSoup to find the table entries with a For Loop
                rawData = []

                # Looking for every row in a table
                # table[0] is just the format for BeautifulSoup
                rows = tables[0].findAll('tr')

                for tr in rows:
                    cols = tr.findAll('td')
                    for td in cols:
                        # data-title = "Reporter"
                        text = cols[0].text
                        rawData.append(text)
                        # data-title = "Date"
                        text = cols[1].text
                        rawData.append(text)
                        '''
                        # data-title = "Comment" (Ingnored)
                        text = cols[2].text
                        rawData.append(text)
                        '''
                        # data-title = "Categories"
                        text = cols[3].text + '\n'
                        rawData.append(text)

                # Modify rawData
                reporter = []
                date = []
                category = []

                itemNum = len(rawData)
                index = 0

                # For 'reporter'
                index1 = 0
                # For 'date'
                index2 = 1
                # For 'category'
                index3 = 2

                for index in range(0, itemNum - 1):
                    # Make sure this loop will not exceed the limit
                    if index1 <= itemNum - 3:
                        # Reporter
                        reporter.append(rawData[index1].replace('\n', ''))
                        index1 += 3

                        # Date
                        date.append(rawData[index2].replace('\n', ''))
                        index2 += 3

                        # Category
                        category.append(rawData[index3].replace('\n\n', ' | ').replace('\n', ' | '))
                        index3 += 3

                        # Global Index
                        index += 1

                # Panda Series
                reporter = Series(reporter)
                date = Series(date)
                category = Series(category)

                # Concatenate into a DataFrame
                legislative_df = pd.concat([date, reporter, category], axis=1)

                # Set up the columns
                legislative_df.columns = ['Date', 'Reporter', 'Category']

                # Delete the dups and reset index (and drop the old index)
                legislative_df = legislative_df.drop_duplicates().reset_index(drop=True)

                # Show the finished DataFrame
                #print(legislative_df)
                printResult.append(legislative_df)
                print('')
    return printResult