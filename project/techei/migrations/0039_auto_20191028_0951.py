# Generated by Django 2.2.6 on 2019-10-28 04:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('techei', '0038_auto_20191028_0443'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventmodel',
            name='description',
            field=models.TextField(),
        ),
    ]
