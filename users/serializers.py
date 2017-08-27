# -*- coding: utf-8 -*-
from rest_framework import serializers
from django.contrib.auth.models import User, Group

from users.models import Menu, GroupMenu


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'is_superuser', 'is_staff', 'last_login', 'date_joined', 'groups')

class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = '__all__'

class GroupMenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupMenu
        fields = '__all__'

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'
