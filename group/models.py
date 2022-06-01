from django.db import models

# Create your models here.
class Group(models.Model):
    character = models.TextField()
    type = models.TextField()

    DAY_INSIDE_FAST = 'DAY_INSIDE_FAST'
    DAY_INSIDE_SLOW = 'DAY_INSIDE_SLOW'
    DAY_OUTSIDE_FAST = 'DAY_OUTSIDE_FAST'
    DAY_OUTSIDE_SLOW = 'DAY_OUTSIDE_SLOW'
    NIGHT_INSIDE_FAST = 'NIGHT_INSIDE_FAST'
    NIGHT_INSIDE_SLOW = 'NIGHT_INSIDE_SLOW'
    NIGHT_OUTSIDE_FAST = 'NIGHT_OUTSIDE_FAST'
    NIGHT_OUTSIDE_SLOW = 'NIGHT_OUTSIDE_SLOW'

    class Meta:
        db_table = 'groups'
