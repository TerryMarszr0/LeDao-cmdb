# -*- coding: utf-8 -*-
from __future__ import print_function

from django.db import transaction
from rest_framework.response import Response

from app.models import AppService, App
from app.models import ServiceHost
from asset.models import Room
from host.models import Hosts
from public.base import CmdbListCreateAPIView, CmdbRetrieveUpdateDestroyAPIView


class ServersStatistics(CmdbListCreateAPIView):
    @transaction.atomic()
    def get(self, request, *args, **kwargs):

        Body = {}

        Body["total"] = total = Hosts.objects.all().count()
        Body["free"] = Hosts.objects.filter(state='free').count()
        Body["physic_machines"] = Hosts.objects.filter(type='server').count()
        Body["virtual_machines"] = Hosts.objects.filter(type='vm').count()
        Body["ECS"] = Hosts.objects.filter(attribute='ECS').count()
        Body["SLB"] = Hosts.objects.filter(attribute='SLB').count()
        Body["RDS"] = Hosts.objects.filter(attribute='RDS').count()
        Body["physic_machines_free"] = Hosts.objects.filter(type='server').filter(state='free').count()
        Body["virtual_machines_free"] = Hosts.objects.filter(type='vm').filter(state='free').count()
        Body["ECS_free"] = Hosts.objects.filter(attribute='ECS').filter(state='free').count()
        Body["SLB_free"] = Hosts.objects.filter(attribute='SLB').filter(state='free').count()
        Body["RDS_free"] = Hosts.objects.filter(attribute='RDS').filter(state='free').count()

        # 获取机房信息
        machines = Hosts.objects.all()
        room_ids = set()
        for machine in machines:
            room_ids.add(machine.room_id)

        for room_id in room_ids:
            machines = Hosts.objects.filter(room_id=room_id)
            room = Room.objects.filter(id=room_id)
            room_name = room[0].name if len(room) > 0 else "default"
            #物理机
            room_machine_message = {}
            physic_machines = {"total": machines.filter(type='server').count(),
                               "free": machines.filter(type='server').filter(state='free').count()}
            room_machine_message['physic_machines'] = physic_machines
            #虚拟机
            virtual_machines = {"total": machines.filter(type='vm').count(),
                               "free": machines.filter(type='vm').filter(state='free').count()}
            room_machine_message['virtual_machines'] = virtual_machines
            #ESC
            esc_machines = {"total": machines.filter(attribute='ECS').count(),
                                "free": machines.filter(attribute='ECS').filter(state='free').count()}
            room_machine_message['esc_machines'] = esc_machines
            #SLB
            slb_machines = {"total": machines.filter(attribute='SLB').count(),
                                "free": machines.filter(attribute='SLB').filter(state='free').count()}
            room_machine_message['slb_machines'] = slb_machines
            #RDS
            rds_machines = {"total": machines.filter(attribute='RDS').count(),
                                "free": machines.filter(attribute='RDS').filter(state='free').count()}
            room_machine_message['rds_machines'] = rds_machines

            #将该机房信息放在Body中
            room_name = room_name.replace('-','_')
            Body[room_name] = room_machine_message

        return Response(Body)



