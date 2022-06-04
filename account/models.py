from django.db import models

from group.models import Group


class Account(models.Model):
    nickname = models.CharField(max_length=20, blank=True)
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'accounts'
