# Generated by Django 4.0.1 on 2022-02-17 13:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Books',
            fields=[
                ('id', models.UUIDField(blank=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=100)),
                ('author', models.CharField(max_length=100)),
                ('slug', models.SlugField(blank=True, default='', null=True)),
            ],
            options={
                'verbose_name_plural': 'Books',
            },
        ),
        migrations.CreateModel(
            name='IssuedBooks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('issuedAt', models.DateField(auto_now_add=True)),
                ('issuedBook', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='book', to='dataLMS.books')),
                ('issuer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='customer', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Issued Books',
            },
        ),
    ]
