# -*- coding: utf-8 -*-
from rest_framework import serializers
from app.models import App, AppService, Group, AppPrincipals, ServicePrincipals, ServiceHost, ServiceResource

class AppSerializer(serializers.ModelSerializer):

    class Meta:
        model = App
        fields = '__all__'

class AppServiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = AppService
        fields = '__all__'

class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = '__all__'

class AppPrincipalsSerializer(serializers.ModelSerializer):       #应用负责人
    class Meta:
        model = AppPrincipals
        fields = '__all__'

class ServicePrincipalsSerializer(serializers.ModelSerializer):       #服务负责人
    class Meta:
        model = ServicePrincipals
        fields = '__all__'

class ServiceHostSerializer(serializers.ModelSerializer):

    class Meta:
        model = ServiceHost

class ServiceResourceSerializer(serializers.ModelSerializer):       #服务负责人
    class Meta:
        model = ServiceResource
        fields = '__all__'


