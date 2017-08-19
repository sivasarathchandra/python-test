# Embedded file name: /home/vinay/python/adnear1.py
import requests
import re
import sys
import datetime
USERNAME = ''
PASSWORD = ''
LOGIN_URL = 'https://engage.adnear.net/login'

class Adnear(object):

    def __init__(self, user, password):
        self.user = user
        self.password = password
        self.session = None
        self.loginDone = False
        self.login()
        self.campaignDict = {}
        return

    def _get(self, url):
        res = self.session.get(url)
        return res

    def _post(self, url, data):
        res = self.session.post(url, data)
        return res

    def _getYesterday(self):
        return str(datetime.date.today() - datetime.timedelta(days=1))

    def login(self):
        self.session = requests.Session()
        response = self._get(LOGIN_URL)
        expr = '.*authenticity_token.*value="(.*)".*'
        reExp = re.compile(expr)
        for line in response.text.split('\n'):
            if 'authenticity_token' in line:
                token = reExp.match(line).group(1)

        data = {'utf8': True,
         'authenticity_token': token,
         'user[email]': '',
         'user[password]': '',
         'user[remember_me]': '0',
         'commit': ''}
        response = self._post(LOGIN_URL, data=data)
        if response.status_code == 200:
            print 'Login Successful'
            self.loginDone = True

    def logout(self):
        self.loginDone = False

    def getAllCampaigns(self, location = 'REG-EU'):
        date = self._getYesterday()
        get_url = 'https://engage.adnear.net/revenue/report?report_type=4&location=%s&exchange=&report_based_on=campaign&report_start_date=%s&report_end_date=%s' % (location, date, date)
        if self.loginDone:
            response = self._get(get_url)
            expr = '.*Allspark: (.*[0-9])<'
            expr2 = '.* >(.*)</span><s.*'
            token = None
            for line in response.text.split('\n'):
                if 'Allspark: ' in line:
                    reExp = re.compile(expr)
                    token = reExp.match(line).group(1)
                    continue
                if token:
                    reExp2 = re.compile(expr2)
                    item = reExp2.match(line).group(1)
                    if ',' not in item:
                        campaignId = item
                        self.campaignDict[campaignId] = {}
                        self.campaignDict[campaignId]['name'] = token
                    else:
                        self.campaignDict[campaignId]['start_date'] = item.split('to')[0]
                        self.campaignDict[campaignId]['end_date'] = item.split('to')[1]
                        token = None

        return self.campaignDict

    def getReport(self, campaignId):
        date = self._getYesterday()
        get_url_string = 'https://engage.adnear.net/AllSpark-Main/campaigns/%s/api/reports/4?report_start_date=%s&report_end_date=%s&aggregation=date'
        if self.loginDone:
            get_url = get_url_string % (campaignId, date, date)
            response = self._get(get_url)
            self.campaignDict[campaignId]['Clicks'] = response.json()['data']['age_group_results'][0]['Clicks']
            self.campaignDict[campaignId]['Impressions'] = response.json()['data']['age_group_results'][0]['Impressions']
            self.campaignDict[campaignId]['CTR'] = response.json()['data']['age_group_results'][0]['CTR']
	    self.campaignDict[campaignId].update(Mraid_Clicks = response.json()['data']['overall_results'][0]['Mraid Expands'])

    def getAllReports(self):
        for campaignId in self.campaignDict.keys():
            self.getReport(campaignId)

    def getCampaignDetails(self, campaignId = 'all'):
        get_url_string = 'https://engage.adnear.net/AllSpark-Main/campaigns/%s/edit'
        if self.loginDone:
            if campaignId == 'all':
                for campaignId in self.campaignDict.keys():
                    get_url = get_url_string % campaignId
                    response = self._get(get_url)
                    expr1 = '.*campaign_daily_targeting_count.*value="(.*)"'
                    expr2 = '.*campaign_total_targeting_count.*value="(.*)"'
                    for line in response.text.split('\n'):
                        if 'campaign_daily_targeting_count' in line and 'value' in line:
                            reExp = re.compile(expr1)
                            self.campaignDict[campaignId]['campaign_daily_targeting_count'] = reExp.match(line).group(1)
                        if 'campaign_total_targeting_count' in line and 'value' in line:
                            reExp = re.compile(expr2)
                            self.campaignDict[campaignId]['campaign_total_targeting_count'] = reExp.match(line).group(1)

    def getAllCampaignDetails(self):
        pass
