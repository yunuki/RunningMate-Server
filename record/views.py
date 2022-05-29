from django.http import HttpResponseNotAllowed, HttpResponseNotFound
from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView

from account.models import Account
from record.models import Record
from record.serializers import RecordSerializer


class RecordDetailView(APIView):
    def get(self, request, pk):
        record = Record.objects.filter(id=pk).first()
        if record is None:
            return HttpResponseNotFound()
        serializer = RecordSerializer(record)
        return Response(serializer.data)

class RecordListView(APIView):
    def get(self, request):
        account_id = request.query_params.get('account_id')
        records = Record.objects.filter(account_id=account_id).all()
        serializer = RecordSerializer(records, many=True)
        return Response(serializer.data)

class RecordCreateView(APIView):
    def post(self, request):
        body = request.data
        account = Account.objects.filter(id=body.get('account_id')).first()
        if account is None:
            return HttpResponseNotAllowed()
        record = Record(
            account=account,
            distance=body.get('distance'),
            kcal=body.get('kcal'),
            pace=body.get('pace'),
            duration=body.get('duration'),
            place=body.get('place'),
            timezone=body.get('timezone')
        )
        record.save()
        serializer = RecordSerializer(record)
        return Response(serializer.data)
