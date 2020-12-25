# Generated by Django 2.2.6 on 2019-10-22 17:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('techei', '0014_category_eventmodel_festclubmodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='institutionprofile',
            name='rating',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='FestImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.ImageField(blank=True, null=True, upload_to='fest/')),
                ('fest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='techei.FestClubModel')),
            ],
        ),
    ]
