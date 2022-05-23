from django.db import transaction
from django.http import HttpResponseServerError
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.views import APIView

from account.models import Account
from oauth.models import OAuthApple
from oauth.serializers import OAuthAppleSerializer
from oauth.utils import AppleOAuth


class AppleOAuthView(APIView):
    @csrf_exempt
    @transaction.atomic()
    def post(self, request):
        token = request.data.get('token')
        if token:
            apple_response = AppleOAuth.validate(token)
            if apple_response['id_token'] is None:
                return HttpResponseServerError()
            oauth_apple = OAuthApple.objects.get(id_token=apple_response['id_token'])
            oauth_apple.access_token = apple_response['access_token']
            oauth_apple.save()
            serializer = OAuthAppleSerializer(oauth_apple)
            return Response(serializer.data)
        else:
            code = request.data.get('code')
            apple_response = AppleOAuth.apple_login(code)
            if apple_response['id_token'] is None:
                return HttpResponseServerError()
            oauth_apple = OAuthApple.objects.filter(id_token=apple_response['id_token']).first()
            is_new = False if oauth_apple else True
            if is_new:
                account = Account()
                account.save()
                oauth_apple = OAuthApple(
                    account=account,
                    id_token=apple_response['id_token'],
                    access_token=apple_response['access_token'],
                    refresh_token=apple_response['refresh_token']
                )
            else:
                oauth_apple.access_token = apple_response['access_token']
                oauth_apple.refresh_token = apple_response['refresh_token']
            oauth_apple.save()
            serializer = OAuthAppleSerializer(oauth_apple)
            return Response(serializer.data)
