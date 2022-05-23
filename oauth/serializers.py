from rest_framework import serializers

from account.serializers import AccountSerializer
from oauth.models import OAuthApple


class OAuthAppleSerializer(serializers.ModelSerializer):
    account = AccountSerializer(read_only=True)
    is_new = serializers.SerializerMethodField(read_only=True)

    def get_is_new(self, obj):
        return obj.account.nickname == ''

    class Meta:
        model = OAuthApple
        fields = ['account', 'refresh_token', 'is_new']
