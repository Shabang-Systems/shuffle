# Generated by Django 2.2.4 on 2019-08-09 19:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dbapi', '0005_auto_20190809_1219'),
    ]

    operations = [
        migrations.AlterField(
            model_name='database',
            name='description',
            field=models.CharField(default='', help_text='Description', max_length=50),
        ),
        migrations.AlterField(
            model_name='folder',
            name='description',
            field=models.CharField(default='', help_text='Description', max_length=50),
        ),
    ]
