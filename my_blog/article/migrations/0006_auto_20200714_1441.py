# Generated by Django 2.2.12 on 2020-07-14 06:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0005_auto_20200714_0101'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articlepost',
            name='body',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='articlepost',
            name='title',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
    ]
