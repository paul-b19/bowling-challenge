# Generated by Django 3.2.3 on 2021-05-19 00:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bowling_score', '0002_auto_20210518_0212'),
    ]

    operations = [
        migrations.AddField(
            model_name='ball',
            name='ball_points',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='frame',
            name='bonus_rolls',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='frame',
            name='frame_closed',
            field=models.BooleanField(default=False),
        ),
    ]
