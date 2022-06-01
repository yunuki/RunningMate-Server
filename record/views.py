import datetime

from django.db.models import Avg, Max, Sum
from django.http import HttpResponseNotAllowed, HttpResponseNotFound
from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView

from account.models import Account
from group.models import Group
from record.models import Record
from record.serializers import RecordSerializer, RecordStatisticsSerializer


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
        records = Record.objects.filter(account_id=account_id).order_by('-created_at').all()
        serializer = RecordSerializer(records, many=True)
        return Response(serializer.data)

class RecordCreateView(APIView):
    def post(self, request):
        body = request.data
        account_id = body.get('account_id')
        account = Account.objects.filter(id=account_id).first()
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
        summary = Record.objects.filter(account_id=account_id).all().aggregate(
            timezone=Max('timezone'),
            place=Max('place'),
            pace=Avg('pace')
        )
        if summary['timezone'] == 'day':
            if summary['place'] == 'inside':
                if summary['pace'] > 10.0:
                    group_type = Group.DAY_INSIDE_FAST
                else:
                    group_type = Group.DAY_INSIDE_SLOW
            else:
                if summary['pace'] > 10.0:
                    group_type = Group.DAY_OUTSIDE_FAST
                else:
                    group_type = Group.DAY_OUTSIDE_SLOW
        else:
            if summary['place'] == 'inside':
                if summary['pace'] > 10.0:
                    group_type = Group.NIGHT_INSIDE_FAST
                else:
                    group_type = Group.NIGHT_INSIDE_SLOW
            else:
                if summary['pace'] > 10.0:
                    group_type = Group.NIGHT_OUTSIDE_FAST
                else:
                    group_type = Group.NIGHT_OUTSIDE_SLOW
        group = Group.objects.filter(type=group_type).first()
        account.group = group
        account.save()
        serializer = RecordSerializer(record)
        return Response(serializer.data)


class RecordStatisticsView(APIView):
    def get(self, request, account_id):
        year = request.query_params.get('year')
        month = request.query_params.get('month')
        statistics = Record.objects.filter(
            account_id=account_id
        )
        if year is not None and month is not None:
            year = int(year)
            month = int(month)
            gte = datetime.datetime(year, month, 1)
            lt = datetime.datetime(year, month + 1, 1)
            statistics = statistics.filter(
            created_at__gte=gte,
            created_at__lt=lt
            )
        statistics = statistics.all().aggregate(
            distance=Sum('distance'),
            duration=Sum('duration'),
            pace=Avg('pace'),
            kcal=Sum('kcal')
        )
        statistics['account_id'] = account_id
        statistics['year'] = year
        statistics['month'] = month
        serializer = RecordStatisticsSerializer(statistics)
        return Response(serializer.data)
