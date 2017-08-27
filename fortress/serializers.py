from rest_framework import serializers
from fortress.models import *

class AuthRecordSerializer(serializers.ModelSerializer):

    class Meta:
        model = AuthRecord
        fields = '__all__'

class ApplyRecordSerializer(serializers.ModelSerializer):

    class Meta:
        model = ApplyRecord
        fields = '__all__'

class ApplyTaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = ApplyTask
        fields = '__all__'

class SSHKeySerializer(serializers.ModelSerializer):

    class Meta:
        model = SSHKey
        fields = '__all__'