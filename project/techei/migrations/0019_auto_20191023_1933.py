# Generated by Django 2.2.6 on 2019-10-23 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('techei', '0018_auto_20191023_1931'),
    ]

    operations = [
        migrations.AlterField(
            model_name='festimage',
            name='name',
            field=models.ImageField(blank=True, max_length=255, null=True, upload_to='fest/'),
        ),
    ]
