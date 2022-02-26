# Generated by Django 4.0.1 on 2022-02-26 16:13

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BooksModel',
            fields=[
                ('bookID', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('bookName', models.CharField(max_length=50)),
                ('bookAuthor', models.CharField(max_length=50)),
                ('bookDescription', models.TextField(max_length=500)),
            ],
            options={
                'verbose_name_plural': 'Books',
            },
        ),
        migrations.CreateModel(
            name='UsersModel',
            fields=[
                ('userId', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('userName', models.CharField(max_length=50)),
                ('userEmail', models.EmailField(max_length=50, unique=True)),
                ('userPassword', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name_plural': 'Users',
            },
        ),
        migrations.CreateModel(
            name='IssuedBooksModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('issuedDate', models.DateField(auto_now_add=True)),
                ('issuedBook', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='libData.booksmodel')),
                ('issuedBy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='libData.usersmodel')),
            ],
            options={
                'verbose_name_plural': 'Issued Books',
            },
        ),
    ]
