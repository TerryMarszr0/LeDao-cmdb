from rest_framework import serializers
from asset.models import *


class RoomSerializer(serializers.ModelSerializer):

    class Meta:
        model = Room
        fields = '__all__'


class RackSerializer(serializers.ModelSerializer):

    class Meta:
        model = Rack
        fields = '__all__'

class AssetModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = AssetModel
        fields = '__all__'

class AssetTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = AssetType
        fields = '__all__'

class ConfSerializer(serializers.ModelSerializer):

    class Meta:
        model = Conf
        fields = '__all__'

class NetworkSerializer(serializers.ModelSerializer):

    class Meta:
        model = Network
        fields = '__all__'

class IpAddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = IpAddress
        fields = '__all__'
