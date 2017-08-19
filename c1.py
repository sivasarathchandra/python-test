#!/usr/bin/env python
import smtplib
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.MIMEMultipart import MIMEMultipart
from email import Encoders
import os
import adnear1
import csv
import pprint

adnearObj = adnear1.Adnear("", "")
print "entering the all camapigns"
adnearObj.getAllCampaigns()
print "entering all reports"
adnearObj.getAllReports()
print "all campaign details"
adnearObj.getCampaignDetails()
with open("Daily_Report.csv", "wb") as output:
	writer = csv.writer(output)
	writer.writerow(['CampaignID','Enddate','CampaignName','CTR','DailyCap','TotalGoal','Startdate','yesterday_impressions','yesterday_clicks']) 
	val = adnearObj.campaignDict.values()[0].keys()
	for k in adnearObj.campaignDict.keys():
		writer.writerow([k] + [adnearObj.campaignDict[k][v] for v in val])

server = smtplib.SMTP("smtp.gmail.com", 587) #or port 465 doesn't seem to work!
server.ehlo()
server.starttls()
gmail_user = ''
gmail_pwd = ''
server.login(gmail_user, gmail_pwd)
msg = MIMEMultipart()
to = [''] #Multiple Email Address
Subject = "Daily Report For ANZ"
 
# Message can be a simple text message or HTML
TEXT = "Hello everyone,\n"
TEXT = TEXT + "\n"
TEXT = TEXT + "Hope you are doing fine today. This report is said to run from my python script\n"
TEXT = TEXT + "Please review the attached report and let me know if it looks fine.\n"
TEXT = TEXT + "Please let me know if any changes are required to it.\n"
TEXT = TEXT + "Regards,\n"
TEXT = TEXT + "Shiva Sarath Chandra"
 
		
msg['From'] = ''
msg['To'] = ", ".join(to) #Join them as we have multiple recipients
msg['Subject'] = Subject
msg.attach(MIMEText(TEXT))
part = MIMEBase('application', 'octet-stream')
part.set_payload(open('Daily_Report.csv', 'rb').read())
Encoders.encode_base64(part)
part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename('Daily_Report.csv'))
msg.attach(part)	
server.sendmail(gmail_user, to, msg.as_string())
print "Email Sent to the Id's Mentioned"
server.close()
