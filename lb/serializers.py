# -*- coding: utf-8 -*-
from rest_framework import serializers
from lb.models import LB, ServiceLB

class LBSerializer(serializers.ModelSerializer):

    class Meta:
        model = LB
        fields = '__all__'

class ServiceLBSerializer(serializers.ModelSerializer):

    class Meta:
        model = ServiceLB
        fields = '__all__'