from django.db import models

from account.models import Account


class OAuthApple(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    id_token = models.TextField()
    refresh_token = models.TextField()
    access_token = models.TextField()

    class Meta:
        db_table = 'oauth_apple'