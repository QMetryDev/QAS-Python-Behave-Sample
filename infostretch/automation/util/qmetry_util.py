from infostretch.automation.core.configurations_manager import ConfigurationsManager
import json
import os
import time
import base64
import zipfile
import requests
import schedule
import sys
from urllib3.util import response


class UploadResult:

    def createZipOfResultDir(self):
        zipf = zipfile.ZipFile('report.zip', 'w', zipfile.ZIP_DEFLATED)
        path = os.path.join(os.getenv('REPORT_DIR'))
        for root, dirs, files in os.walk(path):
            for file in files:
                zipf.write(os.path.join(root, file))
        zipf.close()

    def loadQTMParams(self,params):
        if((ConfigurationsManager().get_str_for_key("automation.qmetry.platformid"))!=""):
            params['cycleID']=ConfigurationsManager().get_str_for_key("automation.qmetry.cycleid")
        if((ConfigurationsManager().get_str_for_key("automation.qmetry.platformid"))!=""):
            params['platformID']=ConfigurationsManager().get_str_for_key("automation.qmetry.platformid")
        if((ConfigurationsManager().get_str_for_key("automation.qmetry.testsuiteid"))!=""):
            params['testsuiteId']=ConfigurationsManager().get_str_for_key("automation.qmetry.testsuiteid")
        if((ConfigurationsManager().get_str_for_key("automation.qmetry.testsuitename"))!=""):
            params['testsuiteName']=ConfigurationsManager().get_str_for_key("automation.qmetry.testsuitename")
        if((ConfigurationsManager().get_str_for_key("automation.qmetry.projectid"))!=""):
            params['projectID']=ConfigurationsManager().get_str_for_key("automation.qmetry.projectid")
        if((ConfigurationsManager().get_str_for_key("automation.qmetry.releaseid"))!=""):
            params['releaseID']=ConfigurationsManager().get_str_for_key("automation.qmetry.releaseid")
        if((ConfigurationsManager().get_str_for_key("automation.qmetry.buildid"))!=""):
            params['buildID']=ConfigurationsManager().get_str_for_key("automation.qmetry.buildid")
        if((ConfigurationsManager().get_str_for_key("automation.qmetry.automationhierarchy"))!=""):
            params['automationHierarchy']=ConfigurationsManager().get_str_for_key("automation.qmetry.automationhierarchy")
            print(" params1 : ")
            print(params)

    def loadQTM4JServerParams(self,params):
        params['format'] = "qas/json"
        if((ConfigurationsManager().get_str_for_key("automation.qmetry.aliasName"))!=""):
            params['aliasName'] = ConfigurationsManager().get_str_for_key("automation.qmetry.aliasName")
        if((ConfigurationsManager().get_str_for_key("automation.qmetry.testrunname"))!=""):
            params['testRunName'] = ConfigurationsManager().get_str_for_key("automation.qmetry.testrunname")
        if((ConfigurationsManager().get_str_for_key("automation.qmetry.labels"))!=""):
            params['labels'] = ConfigurationsManager().get_str_for_key("automation.qmetry.labels")
        if((ConfigurationsManager().get_str_for_key("automation.qmetry.components"))!=""):
            params['components'] = ConfigurationsManager().get_str_for_key("automation.qmetry.components")
        if((ConfigurationsManager().get_str_for_key("automation.qmetry.version"))!=""):
            params['versions'] = ConfigurationsManager().get_str_for_key("automation.qmetry.version")
        if((ConfigurationsManager().get_str_for_key("automation.qmetry.sprint"))!=""):
            params['sprint'] = ConfigurationsManager().get_str_for_key("automation.qmetry.sprint")
        if((ConfigurationsManager().get_str_for_key("automation.qmetry.platform"))!=""):
            params['platform'] = ConfigurationsManager().get_str_for_key("automation.qmetry.platform")
        if((ConfigurationsManager().get_str_for_key("automation.qmetry.testrunkey"))!=""):
            params['testRunKey'] = ConfigurationsManager().get_str_for_key("automation.qmetry.testrunkey")
        if((ConfigurationsManager().get_str_for_key("automation.qmetry.comment"))!=""):
            params['comment'] = ConfigurationsManager().get_str_for_key("automation.qmetry.comment")
        if((ConfigurationsManager().get_str_for_key("automation.qmetry.testassethierarchy"))!=""):
            params['testAssetHierarchy'] = ConfigurationsManager().get_str_for_key("automation.qmetry.testassethierarchy")

        print(" params1 : ")
        print(params)

    def loadQTM4JCloudParams(self,params):
        params['format'] = "qas/json"
        if((ConfigurationsManager().get_str_for_key("automation.qmetry.aliasName"))!=""):
            params['aliasName'] = ConfigurationsManager().get_str_for_key("automation.qmetry.aliasName")
        if((ConfigurationsManager().get_str_for_key("automation.qmetry.testrunname"))!=""):
            params['testRunName'] = ConfigurationsManager().get_str_for_key("automation.qmetry.testrunname")
        if((ConfigurationsManager().get_str_for_key("automation.qmetry.labels"))!=""):
            params['labels'] = ConfigurationsManager().get_str_for_key("automation.qmetry.labels")
        if((ConfigurationsManager().get_str_for_key("automation.qmetry.components"))!=""):
            params['components'] = ConfigurationsManager().get_str_for_key("automation.qmetry.components")
        if((ConfigurationsManager().get_str_for_key("automation.qmetry.version"))!=""):
            params['versions'] = ConfigurationsManager().get_str_for_key("automation.qmetry.version")
        if((ConfigurationsManager().get_str_for_key("automation.qmetry.sprint"))!=""):
            params['sprint'] = ConfigurationsManager().get_str_for_key("automation.qmetry.sprint")
        if((ConfigurationsManager().get_str_for_key("automation.qmetry.platform"))!=""):
            params['platform'] = ConfigurationsManager().get_str_for_key("automation.qmetry.platform")
        if((ConfigurationsManager().get_str_for_key("automation.qmetry.testrunkey"))!=""):
            params['testRunKey'] = ConfigurationsManager().get_str_for_key("automation.qmetry.testrunkey")
        if((ConfigurationsManager().get_str_for_key("automation.qmetry.comment"))!=""):
            params['comment'] = ConfigurationsManager().get_str_for_key("automation.qmetry.comment")
        if((ConfigurationsManager().get_str_for_key("automation.qmetry.testassethierarchy"))!=""):
            params['testAssetHierarchy'] = ConfigurationsManager().get_str_for_key("automation.qmetry.testassethierarchy")

        print(" params1 : ")
        print(params)

    def getQTM4JUrl(self,id):
        reqUrl = "https://importresults.qmetry.com/prod/importstatus/" + id
        headers = {
            'Content-Type': "application/json",
        }
        response = requests.request("GET", reqUrl, headers=headers)
        response = json.loads(response.text)
        print(response)
        print(response['data']['status'])

        if (response['isSuccess']):
            if (response['data']['status'] != 'In Progress'):
                if (response['data']['status'] == "Success"):
                    print("Test Run :: ")
                    print(response['data']['testRun'])
                    sys.exit()
                    return schedule.CancelJob
                else:
                    if(response['data']['testRun']):
                        print(response['data']['testRun'])
                    else:
                        print(response['errorMessage'])
                        return schedule.CancelJob


    def uploadFile(self):
        self.createZipOfResultDir()
        isOnPremise = str(ConfigurationsManager().get_str_for_key("automation.qmetry.onpremise"))
        integrationType = ConfigurationsManager().get_str_for_key("automation.qmetry.type")
        apiKey = ConfigurationsManager().get_str_for_key("automation.qmetry.apikey")
        url = ConfigurationsManager().get_str_for_key("automation.qmetry.url")

        headers = {}
        file = open('report.zip', 'rb')
        files = {'file': file}
        params = {}
        if (integrationType == 'QTM'):
            headers['apiKey'] = apiKey
            headers['scope'] = 'default'
            headers['accept'] = 'application/json'
            params['testCaseUpdateLevel'] = 1
            params['entityType'] = "QAF"
            self.loadQTMParams(params)
            print(str(params))
            res = requests.request("post", url, data=params,
                                   headers=headers, files=files)
            print(res)
            print(res.content)
        elif isOnPremise == "true":
            print("QTM4J Server")
            username = ConfigurationsManager().get_str_for_key("automation.qmetry.username")
            password = ConfigurationsManager().get_str_for_key("automation.qmetry.password")
            s = username + ":" + password
            data_bytes = s.encode("utf-8")
            encodedAuth = base64.b64encode(data_bytes).decode('utf-8')
            print(encodedAuth)
            headers['Authorization'] = "Basic " + str(encodedAuth)
            params['apiKey'] = apiKey
            # print(headers)
            self.loadQTM4JServerParams(params)
            res = requests.request("post", url, data=params,
                                   headers=headers, files=files)
            print(res)
            print(res.content)
        else:
            print("QTM4J CLoud")
            headers['Content-Type'] = "application/json"
            params['apiKey'] = apiKey
            params['testCaseUpdateLevel'] = 1
            params['isZip'] = 'true'
            self.loadQTM4JCloudParams(params)
            res = requests.request("post", url, data=json.dumps(params),
                                   headers=headers)

            res = json.loads(res.text)
            requestUrl = res['url']
            trackingId = res['trackingId']

            headers = {}
            params = {}
            headers['Content-Type'] = "multipart/form-data"
            res1 = requests.request("put", requestUrl, data=params,
                                    headers=headers, files=files)

            schedule.every(2).seconds.do(self.getQTM4JUrl,id=trackingId)
            while 1:
                schedule.run_pending()
                time.sleep(1)
            print(res1)

        file.close()

        isDebug = str(ConfigurationsManager().get_str_for_key("automation.qmetry.debug"))
        if isDebug == "true":
            print("debug is true, so do not remove zip file")
        else:
            print("debug is false, so remove zip file")
            os.remove("report.zip")
