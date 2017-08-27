from rest_framework import serializers
from host.models import *

class HostsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Hosts
        fields = '__all__'

class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Image
        fields = '__all__'

class HostsSearchSerializer(serializers.ModelSerializer):

    class Meta:
        model = Hosts
        fields = ('id', 'ip')

class HostPasswordSerializer(serializers.ModelSerializer):

    class Meta:
        model = HostPassword
        fields = '__all__'

class HostInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = HostInfo
        fields = '__all__'