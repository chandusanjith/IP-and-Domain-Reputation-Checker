import virustotal2
import csv

def VirusTotalChecker(ip):

    vt = virustotal2.VirusTotal2("aef48c9cfa4b5a2c4af411b2cf316fafd76417a3bcc13035a59005baa3029df4")
    try:
        ip_report = vt.retrieve(ip) 
    except:
        return(" VirusTotal API error: on ip " + ip)

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