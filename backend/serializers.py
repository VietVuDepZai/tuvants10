from rest_framework import serializers
from .models import THPT

class THPTSerializer(serializers.ModelSerializer):
    class Meta:
        model = THPT
        fields = '__all__'
