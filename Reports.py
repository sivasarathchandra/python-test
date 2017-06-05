#!/usr/bin/env python
import requests
import re
import sys


USERNAME = "shiva@near.co" 
PASSWORD = "hitman1251"
LOGIN_URL = "https://engage.adnear.net/login"
GET_URL = "https://engage.adnear.net/AllSpark-Main/campaigns/589acc267e4fb73c4500043c/api/reports/4?report_start_date=2017-02-15&report_end_date=2017-05-10&aggregation=date"

sys.stdout = open("junk1","w").encode('utf8')
session = requests.Session()
response = session.get(LOGIN_URL)

expr = ".*authenticity_token.*value=\"(.*)\".*"
reexp = re.compile(expr)
for line in response.text.split("\n"):
	if "authenticity_token" in line:
		token = reexp.match(line).group(1)
print token

data = {
	"utf8" : True,
	"authenticity_token" : token,
	"user[email]" : "shiva@near.co",
	"user[password]" : "hitman1251",
	"user[remember_me]" : "0",
	"commit" : ""
}

response = session.post(LOGIN_URL, data=data)
print "Login Done"

response = session.get(GET_URL)
json = response.text
print json
