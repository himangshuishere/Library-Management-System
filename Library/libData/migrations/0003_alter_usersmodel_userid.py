# Generated by Django 4.0.1 on 2022-02-27 13:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('libData', '0002_alter_usersmodel_userid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usersmodel',
            name='userId',
            field=models.CharField(default='<function uuid4 at 0x7f5d38bc4a60>', editable=False, max_length=50, primary_key=True, serialize=False),
        ),
    ]