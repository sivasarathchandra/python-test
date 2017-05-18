#!/usr/bin/env python
import requests
import re
import json

USERNAME = "8888888"
PASSWORD = "8888888"
LOGIN_URL = "https://engage.adnear.net/login"
GET_URL = "https://engage.adnear.net/AllSpark-Main/campaigns/589acc267e4fb73c4500043c/api/reports/4?report_start_date=2017-02-15&report_end_date=2017-05-10&aggregation=date"

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
	"user[email]" : "8888888",
	"user[password]" : "8888888",
	"user[remember_me]" : "0",
	"commit" : ""
}

response = session.post(LOGIN_URL, data=data)
print "Login Done"

print "now printing all the campaign id with different URL"

f = open('camapign ID.txt', 'r')
for line in f.readlines():
    id = line.strip('\n')
    url = "https://engage.adnear.net/AllSpark-Main/campaigns/{0}/api/reports/4?report_start_date=2017-02-15&report_end_date=2017-05-10&aggregation=date".format(id)
print url