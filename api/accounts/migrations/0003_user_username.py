# Generated by Django 3.1.3 on 2022-04-23 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_user_profile_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='username',
            field=models.CharField(default='b48714174926804', max_length=100),
        ),
    ]
