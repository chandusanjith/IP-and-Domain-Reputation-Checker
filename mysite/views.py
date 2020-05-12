from __future__ import print_function
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse, HttpResponseNotFound
import sys,re, smtplib
from mysite.models import ips, contacted
from mysite.abuseipdb import abuseipdbChecker
from mysite.sans import sansChecker
from mysite.myIPwhois import IPWhoisChecker
from mysite.xforceIBM import myXForceChecker
from mysite.VirusTotal import VirusTotalChecker
import openpyxl
from django.contrib import messages
import xlwt
import datetime
from django.contrib.auth.models import User
import pydnsbl
import random
import string
from datetime import date
from pathos.multiprocessing import ProcessingPool as Pool
from threading import Thread

def LoadPage(request):
  return render(request, 'Main.html')

def LoadCheckIp(request):
  return render(request, 'checkip.html')

def About(request):
  return render(request, 'About.html')

def ContactDev(request):
  return render(request, 'Developer.html')


def addcontact(request):
  name = request.POST['namec']
  email = request.POST['email']
  message = request.POST['msg']
  mobileno = request.POST['mno']
  data = contacted(name = name, email = email, message = message, mobile = mobileno, dateofcontact = date.today())
  data.save()
  messages.info(request, 'Thanks, we will contact you soon ')
  return render(request, 'checkip.html')   

def Contact(request):
  return render(request, 'contactus.html')

def checksingleip(request):
  ip = request.POST['singleip']
  mySansPrint2 = ''
  myAbuseIPDBPrint3 = ''
  myXForcePrint4 = ''
  print('>>>>> Welcome to WebScraping Tool <<<<<')

        # regular expression for IP
  re_ip = re.compile('^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$')

  print("Now checking " + ip + " ...")
  print("")

        # If the IP format is valid:
  if re_ip.match(ip):
            # Call myIPwhois.py
    #part1 = IPWhoisChecker("https://www.abuseipdb.com/whois/" + ip)
    #part1 = part1[345:]
    part1 = checkippydnsbl(ip)      

            # Call sans.py
    part2 =  sansChecker(ip)

            # Call abuseipdb.py
    part3 =  abuseipdbChecker("https://www.abuseipdb.com/check/" + ip)
   
     # Call xforceIBM.py
 
    part4 = myXForceChecker("https://api.xforce.ibmcloud.com/ipr/" + ip)
    
    try:
       part5 = VirusTotalChecker(ip)
    except:
       part5 = "Virus Total Down, API Not responding!!!"

    part6 = IPWhoisChecker("https://www.abuseipdb.com/whois/" + ip)


    print("virustotal")
    print(part5)
    if part5 == "POSSIBLY SAFE" or part5 == "Virus Total Down, API Not responding!!!":
        print("noblk")
        res5 = "False"
    else:
        print("blk")
        res5 = "True"
       

    if part1 == True or part1 == False:
       ip_checker = pydnsbl.DNSBLIpChecker()
       result=ip_checker.check(ip)
       resukt1 = result.detected_by
     
    if not part3:
        req4 = "False"
    else:
        req4 = "True"
    if  "Malware" in part4[2]:
        req3 = "True"
    else:
        req3 = "False"               
    if (int(part2[0][13:])) > 0 :
        req2 = "True"
    else:
        req2 = "False"
    if part1 == True or req2 == "True" or req3 == "True" or req4 == "True" or res5 == "True":
        status = "09"
    else:
          status = "00"
    context = {'part1': resukt1,
             'part2': part2,
             'part3':part3,
             'part4': part4,
             'part5':part5,
             'part6':part6,
             'status': status,
             'isip': ip,
             'dns': "00"}
    return render(request, 'checkip.html', context)    

        # If the input is a domain or other strings, let the website validate then ...
  else:
            #Call myIPwhois.py
      part1 =  IPWhoisChecker("https://www.abuseipdb.com/whois/" + ip)

            # Call sans.py
            # sans.sansChecker("https://isc.sans.edu/api/ip/" + ip)
            #part2 = sansChecker(ip)

            # Call abuseipdb.py
      part3 = abuseipdbChecker("https://www.abuseipdb.com/check/" + ip)

      part4 = myXForceChecker("https://api.xforce.ibmcloud.com/url/" + ip)
          #context = {
             #'part2': part1,
             #'part3':part3,
             #'part4':part4 }
      
      context = {'part6': part1,
             'part2':part3,
             'part4': part4,
             'isip': ip,
             'dns': "01"}
      return render(request, 'checkip.html', context)    


          
def create_ref_code():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))

def checkippydnsbl(ipaddress):
   ip_checker = pydnsbl.DNSBLIpChecker()
   result=ip_checker.check(ipaddress)
   resultfinal = result.blacklisted
   return resultfinal

def checkipchandu(ipaddress):
    result = sansChecker(ipaddress)
    print(result)
    return result

def checkIBM(ipaddress):
    print("chandu comimg here ibm function")
    result = myXForceChecker("https://api.xforce.ibmcloud.com/ipr/" + ipaddress)
    print("chandu xls ibm xforce")
    return result


def ReadBulk(request):
    ipss = request.POST['names']
    ip_list = ipss.split()
    if not ip_list:
      messages.info(request, 'Field is empty!!')
      return render(request, 'index.html')
    else:
        ref = create_ref_code()
        ip_length = len(ip_list)
        ref_list = list()
        for i in range(ip_length):
          ref_list.append(ref)
        print("reflist")
        print(ref_list)
        p = Pool(20)
        p.map(check, ip_list, ref_list)
        result_to_display = ips.objects.filter(reference = ref_list[0])
        context = {'data_ip': result_to_display,
                'reference': ref_list[0],
                'button': 1}

        return render(request, 'index.html', context)
    

def ReadXl(request):
    if "GET" == request.method:
        return render(request, 'index.html', {'button': 0})
    else:
        excel_file = request.FILES["excel_file"]

        if not excel_file:
          messages.info(request, 'Please select a file!!')
          return render(request, 'index.html')
        # you may put validations here to check extension or file size

        wb = openpyxl.load_workbook(excel_file)

        # getting a particular sheet by name out of many sheets
        worksheet = wb["Sheet1"]
        print(worksheet)
        
        excel_data = list()
        # iterating over the rows and
        # getting value from each cell in row
        ref = create_ref_code()
        row_data = list()
        ref_data = list()
        for row in worksheet.iter_rows():
            for cell in row:
                row_data.append(str(cell.value))
                ref_data.append(ref)
        print(row_data)
        p = Pool(20)
        print(ref)
        p.map(check, row_data, ref_data)
        print(ref)
        print("finished dfunction")
        result_to_display = ips.objects.filter(reference = ref_data[0])
        context = {'data_ip': result_to_display,
                'reference': ref_data[0],
                'button': 1}

        return render(request, 'index.html', context)

def check(ip, ref):
  print("function")
  print(ip)
  print(ref)
  status1 = checkippydnsbl(ip)
  status2 = checkipchandu(ip)
  status3 = checkIBM(ip)
  status4 = abuseipdbChecker("https://www.abuseipdb.com/check/" + ip)


  if not status4:
      req4 = "False"
  else:
      req4 = "True"
  if  "Malware" in status3[2]:
      req3 = "True"
  else:
      req3 = "False"               
  if (int(status2[0][13:])) > 0 :
      req2 = "True"
  else:
      req2 = "False"
  if status1 == True or req2 == "True" or req3 == "True" or req4 == "True":
      print('at block')
      dbstatus = "BLACKLISTED"
  else:
      print('at no block')
      dbstatus = "POSSIBLY SAFE"
  
 

  if req4 == "True":
     abuse = status4[0]
  else:
     abuse = "NIL"

  if req3 == "True":
     ibm = status3
  else:
     ibm = "NIL"

  if req2 == "True":
     sans = status2
  else:
     sans = "NIL"
  
  if status1 == True:
     print("chandu here dns bulk")
     ip_checker = pydnsbl.DNSBLIpChecker()
     result=ip_checker.check(ip)
     dnsbl = result.detected_by
  else:
     print("chandu here NIL")
     dnsbl = "NIL"

  a = ips(reference = ref, ipaddress = ip, status = dbstatus, remarks = abuse, Sans =sans, Pysbil =dnsbl , VirusTotal =   "virustotal", IbmXForce = ibm)
  a.save()

def export_users_xls(request, ref):
    filename = "ParameterLabs" + str(datetime.datetime.now()) + ".xls"
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="ParameterLabs.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('parameter')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['IP Address', 'Status', 'AbuseIPDB Result', 'Sans Result', 'PYSBIL Result', 'IBM X-Force Result']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = ips.objects.filter(reference = ref).values_list('ipaddress','status','remarks','Sans','Pysbil','IbmXForce')
    print("chandu row")
    print(rows)
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response
