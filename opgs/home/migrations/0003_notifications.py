# Generated by Django 3.0.14 on 2022-03-29 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_auto_20220329_1548'),
    ]

    operations = [
        migrations.CreateModel(
            name='notifications',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('notification', models.TextField(max_length=500)),
                ('visible_to_student', models.BooleanField()),
                ('visible_to_company', models.BooleanField()),
                ('visible_to_alumni', models.BooleanField()),
            ],
        ),
    ]