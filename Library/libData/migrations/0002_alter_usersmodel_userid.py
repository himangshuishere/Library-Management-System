# Generated by Django 4.0.1 on 2022-02-27 10:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('libData', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usersmodel',
            name='userId',
            field=models.UUIDField(default='dfe39c3716d44929b2f969d445e311bc', editable=False, primary_key=True, serialize=False),
        ),
    ]