import requests
from requests.auth import HTTPBasicAuth
import json

def myXForceChecker(url):

    printResult = []
    try:
       myResult1 = requests.get(url,  auth=HTTPBasicAuth('f276aa3a-f95a-4222-b112-2640399834d7',
                                                     'd2ecb5be-6648-450f-b632-72126a42bec0'), timeout=12)
    except:
        return ("IBM API TIMEOUT ERROR!!!")
    c1 = myResult1.content
    myJson1 = json.loads(c1)
    '''
    # indent = 2
    # json.dumps() change data to python dictionary
    # sortedData = json.dumps(myJson1, sort_keys=True, indent=2)
    # print sortedData
    '''
    if "geo" in myJson1:
        for key, value in myJson1["geo"].items():
            geo = "Country" + ": " + str(value)
            printResult.append(geo)
            break
    if "score" in myJson1:
        if myJson1["score"] == 1:
            printResult.append("Risk Score: " + str(myJson1["score"]) + " (low)")
        else:
            printResult.append("Risk Score: " + str(myJson1["score"]))
    if "cats" in myJson1:
        if myJson1["cats"]:
            for key, value in myJson1["cats"].items():
                cat = str(key) + " (" + str(value) + "%)"
                printResult.append("Categorization: " + cat)
        else:
            printResult.append("Categorization: Unsuspicious")

    if "result" in myJson1:
        myJsonResult = myJson1["result"]
        if myJsonResult["score"] == 1:
            printResult.append("Risk Score: " + str(myJsonResult["score"]) + " (low)")
        else:
            printResult.append("Risk Score: " + str(myJsonResult["score"]))

        if myJsonResult["categoryDescriptions"]:
            for key, value in myJsonResult["categoryDescriptions"].items():
                cat = "<" + str(key).replace(" / ", "|") + ">: " + str(value)
                printResult.append(cat)

    return printResult

def myXForceHashChecker(url):

    family, type, risk = [], '', ''
    printResult = []
    response  = requests.get(url,  auth=HTTPBasicAuth('f276aa3a-f95a-4222-b112-2640399834d7',
                                                     'd2ecb5be-6648-450f-b632-72126a42bec0'), timeout=12)
    if response.status_code == 200:
       json_response = response.json()
       try:
            family.append(json_response['malware']['origins']['external']['family'])
       except:
            family.append('No Info')
       try:
            type = json_response['malware']['type']
       except:
            type = 'No Info'
       try:
            risk = json_response['malware']['risk']
       except:
            risk = 'No Info'
    else:
         family, type = risk = ['No Info'], 'No Info'

    return family, type, risk