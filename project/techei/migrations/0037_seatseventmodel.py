# Generated by Django 2.2.6 on 2019-10-27 21:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('techei', '0036_auto_20191027_2131'),
    ]

    operations = [
        migrations.CreateModel(
            name='SeatsEventModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('available_seats', models.IntegerField(blank=True, editable=False)),
                ('event', models.ForeignKey(blank=True, editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='relates_event', to='techei.EventModel')),
                ('total_seats', models.ForeignKey(blank=True, editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='total', to='techei.EventModel')),
                ('user', models.ForeignKey(blank=True, editable=False, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
