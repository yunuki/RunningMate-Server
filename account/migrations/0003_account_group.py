# Generated by Django 4.0.4 on 2022-05-31 08:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('group', '0001_initial'),
        ('account', '0002_remove_account_exp'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='group',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='group.group'),
        ),
    ]
