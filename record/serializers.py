from rest_framework import serializers

from account.serializers import AccountSerializer
from record.models import Record


class RecordSerializer(serializers.ModelSerializer):
    account = AccountSerializer(read_only=True)

    class Meta:
        model = Record
        fields = '__all__'


class RecordStatisticsSerializer(serializers.Serializer):
    account_id = serializers.IntegerField()
    year = serializers.IntegerField(allow_null=True)
    month = serializers.IntegerField(allow_null=True)
    distance = serializers.FloatField()
    duration = serializers.IntegerField()
    pace = serializers.FloatField()
    kcal = serializers.FloatField()