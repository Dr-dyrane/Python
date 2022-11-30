from rest_framework import serializers

from .models import *



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ThemeSetting
        fields = '__all__'