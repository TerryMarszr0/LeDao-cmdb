# -*- coding: utf-8 -*-
import json, time, statsd
from aliyunsdkcore import client
from aliyunsdkvpc.request.v20160428 import DescribeBandwidthPackageMonitorDataRequest, DescribeBandwidthPackagesRequest

class AliyunBase():

    key = 'E7jpl8QJADB8Y9EN'
    secret = '2u4lTeNGdN5ndgbFCBiKZhWGksDjyr'
    regionId = ''

    def __init__(self, regionId='cn-shanghai'):
        self.regionId = regionId
        self.initClient(regionId, self.key, self.secret)

    def initClient(self, regionId, key, secret):
        self.clt = client.AcsClient(key, secret, regionId)
        return self.clt

class BandWidthMonitor(AliyunBase):

    def getMonitorData(self, bandwidthPackageId, startTime, endTime):
        request = DescribeBandwidthPackageMonitorDataRequest.DescribeBandwidthPackageMonitorDataRequest()
        try:
            request.set_BandwidthPackageId(bandwidthPackageId)
            request.set_StartTime(startTime)
            request.set_EndTime(endTime)
            result = self.clt.do_action_with_exception(request)
            result = json.loads(result)
            return True, result['MonitorDatas']['MonitorData']
        except Exception, ex:
            return False, str(ex)

class BandWidthPackages(AliyunBase):

    def getBandWidth(self):
        request = DescribeBandwidthPackagesRequest.DescribeBandwidthPackagesRequest()
        try:
            request.set_PageSize(50)
            result = self.clt.do_action_with_exception(request)
            result = json.loads(result)
            return True, result['BandwidthPackages']['BandwidthPackage']
        except Exception, ex:
            return False, str(ex)

if __name__ == "__main__":

    # 10.1.26.91 8125
    monitor = BandWidthMonitor()
    c = statsd.StatsClient('10.1.26.91', 8125)
    state, result = BandWidthPackages().getBandWidth()
    if state:
        for r in result:
            bandwidthPackageId = r['BandwidthPackageId']
            endTime = int(time.time()) - 8*3600 - 120
            startTime = endTime - 60
            endTime = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.localtime(endTime))
            startTime = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.localtime(startTime))
            state, data = monitor.getMonitorData(bandwidthPackageId, startTime, endTime)
            if not state:
                continue
            for d in data:
                print d
                # TimeStamp = int(time.mktime(time.strptime(d['TimeStamp'], '%Y-%m-%dT%H:%M:%SZ')))
                c.gauge(bandwidthPackageId + '.transportedBandwidth', d['TransportedBandwidth'])
                c.gauge(bandwidthPackageId + '.receivedBandwidth', d['ReceivedBandwidth'])
                c.gauge(bandwidthPackageId + '.bandwidth', d['Bandwidth'])
                # print c.gauge(bandwidthPackageId + '.dtime', d['TimeStamp'])
                c.gauge(bandwidthPackageId + '.packets', d['Packets'])
                c.gauge(bandwidthPackageId + '.flow', d['Flow'])
                c.gauge(bandwidthPackageId + '.TX', d['TX'])
                c.gauge(bandwidthPackageId + '.RX', d['RX'])