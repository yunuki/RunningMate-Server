from django.db import models

# Create your models here.
from account.models import Account


class Record(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    distance = models.FloatField()
    kcal = models.FloatField()
    pace = models.FloatField()
    duration = models.IntegerField()
    place = models.CharField(max_length=10)
    timezone = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'records'
