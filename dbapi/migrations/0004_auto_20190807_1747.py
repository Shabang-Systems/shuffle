# Generated by Django 2.2.4 on 2019-08-08 00:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dbapi', '0003_auto_20190807_1746'),
    ]

    operations = [
        migrations.AlterField(
            model_name='database',
            name='name',
            field=models.CharField(default='', help_text='Name', max_length=50),
        ),
        migrations.AlterField(
            model_name='word',
            name='term',
            field=models.CharField(default='', help_text='Term', max_length=100),
        ),
    ]
