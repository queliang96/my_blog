# Generated by Django 2.2.12 on 2020-07-13 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0004_auto_20200713_2044'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articlepost',
            name='title',
            field=models.CharField(max_length=128, null=True),
        ),
    ]
