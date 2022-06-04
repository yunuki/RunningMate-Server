from rest_framework import serializers

from group.serializers import GroupSerializer
from .models import Account


class AccountSerializer(serializers.ModelSerializer):
    group = GroupSerializer(read_only=True)
    class Meta:
        model = Account
        fields = '__all__'
