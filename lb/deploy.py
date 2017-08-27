
import requests
import sys
import json


hostip = sys.argv[1]
#
state = sys.argv[2]
port = sys.argv[3]
# url = "http://cmdb.mwbyd.cn/api/host/changestate/"
url = "http://127.0.0.1:8000/api/host/changestate/"
params = {"ip": hostip,  "state": state}
headers = {'content-type': 'application/x-www-form-urlencoded','Authorization': 'Token bc63a0adbcea84f32097647bae9e668f298e8c6f'}

r = requests.patch(url,data=params,headers=headers)
state_res = r.content
if '"success":true' in state_res:

    # url2 = 'http://cmdb.mwbyd.cn/api/lb/statepush/%s/%s/' % (hostip, port)
    url2 = "http://127.0.0.1:8000/api/lb/statepush/%s/%s/" % (hostip, port)

    headers2 = {'Authorization': 'Token bc63a0adbcea84f32097647bae9e668f298e8c6f'}
    r2 = requests.patch(url2,headers=headers2)
    res2 = r2.content
    result = json.loads(res2)
    # print result
    res_data = result["res_data"]
    if result["res_code"] == "0":
        print "MW_SUCCESS"
    else:
        print res_data
else:
    print state_res


# req = urllib2.Request(url)
# res_data = urllib2.urlopen(req)
# res = res_data.read()
# print res
