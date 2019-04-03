from rest_framework import serializers
from api.models import MobileApp

class MobileAppSerializer(serializers.ModelSerializer):
    class Meta:
        model = MobileApp
        fields = "__all__"