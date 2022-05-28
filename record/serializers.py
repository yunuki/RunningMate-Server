from rest_framework import serializers

from account.serializers import AccountSerializer
from record.models import Record


class RecordSerializer(serializers.ModelSerializer):
    account = AccountSerializer(read_only=True)

    class Meta:
        model = Record
        fields = '__all__'
