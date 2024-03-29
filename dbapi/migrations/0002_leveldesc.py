# Generated by Django 2.2.4 on 2019-08-09 16:43

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dbapi', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LevelDesc',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('db', models.ForeignKey(blank=True, null=True, on_delete='CASCADE', related_name='user_levels', to='dbapi.Database')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete='CASCADE', related_name='user_levels', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
