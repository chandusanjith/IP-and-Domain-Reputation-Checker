import virustotal2
import csv

def VirusTotalChecker(ip):
    vt = virustotal2.VirusTotal2("b2510b80fec019d8b6896a8e575022690efecdfa858d1077c75b37dae5f4621e")
    try:
        ip_report = vt.retrieve(ip)   #get the VT IP report for this IP
    except:
        return("API error: on ip " + ip)
    
    total_pos = sum([u["positives"] for u in ip_report.detected_urls])
    total_scan = sum([u["total"] for u in ip_report.detected_urls])
    count = len(ip_report.detected_urls)
    if total_pos == 0 and total_scan == 0:
         results = "POSSIBLY SAFE"
         return results
    else:
        print(str(count)+" URLs hosted on "+ip+" are called malicious by (on average) " + \
          str(int(total_pos/count)) + " / " + str(int(total_scan/count)) + " scanners")

        return(str(count)+" URLs hosted on "+ip+" are called malicious by (on average) " + \
          str(int(total_pos/count)) + " / " + str(int(total_scan/count)) + " scanners")