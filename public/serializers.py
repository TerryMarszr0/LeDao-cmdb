from rest_framework import serializers
from public.models import AsyncTask


class AsyncTaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = AsyncTask
        fields = '__all__'

class RedirectSerializer(serializers.ModelSerializer):

    class Meta:
        model = AsyncTask
        fields = ('id', )

