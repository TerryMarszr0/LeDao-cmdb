# -*- coding: utf-8 -*-
import json, time
from aliyunsdkcore import client
from aliyunsdkecs.request.v20140526 import DescribeInstancesRequest, DescribeRegionsRequest, DescribeZonesRequest, DescribeImagesRequest
from host.models import Image


class AliyunBase():

    key = ''
    secret = ''
    regionId = ''

    def __init__(self, regionId='cn-shanghai'):
        self.regionId = regionId
        self.initClient(regionId, self.key, self.secret)

    def initClient(self, regionId, key, secret):
        self.clt = client.AcsClient(key, secret, regionId)
        return self.clt

class AliyunRegionsApi(AliyunBase):

    def getAllRegions(self):
        request = DescribeRegionsRequest.DescribeRegionsRequest()
        try:
            result = self.clt.do_action_with_exception(request)
            result = json.loads(result)
            return True, result['Regions']['Region']
        except Exception, ex:
            return False, str(ex)

class AliyunZoneApi(AliyunBase):

    def getAllZone(self):
        request = DescribeZonesRequest.DescribeZonesRequest()
        try:
            result = self.clt.do_action_with_exception(request)
            result = json.loads(result)
            return True, result['Zones']['Zone']
        except Exception, ex:
            return False, str(ex)

class AliyunImagesApi(AliyunBase):

    def getImagesList(self, pageNumber, pageSize):
        request = DescribeImagesRequest.DescribeImagesRequest()
        request.set_PageNumber(pageNumber)
        request.set_PageSize(pageSize)
        request.set_ImageOwnerAlias('self')
        request.set_accept_format('json')
        try:
            result = self.clt.do_action_with_exception(request)
            result = json.loads(result)
            data = {'count': result['TotalCount'], 'results': result['Images']['Image']}
            return True, data
        except Exception, ex:
            return False, str(ex)


def getRegions():
    return AliyunRegionsApi('cn-shanghai').getAllRegions()

def import_img():
    page = 1
    size = 100
    while True:
        status, result = AliyunImagesApi().getImagesList(page, size)
        page += 1
        if not status:
            continue
        if len(result['results']) <= 0:
            break
        rows = result['results']
        for r in rows:
            images = Image.objects.filter(image_id=r['ImageId'])
            if len(images) > 0:
                images.update(name=r['ImageName'], platform=r['Platform'])
                continue
            try:
                Image.objects.create(image_id=r['ImageId'], name=r['ImageName'], os_type='linux', platform=r['Platform'], ctime=int(time.time()))
            except Exception, ex:
                print str(ex)


if __name__ == "__main__":

    res, result = AliyunImagesApi().getImagesList(1, 100)
    print result
    for i in result['results']:
        print i['ImageName']
