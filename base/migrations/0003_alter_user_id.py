# Generated by Django 5.1.3 on 2024-12-03 19:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_alter_user_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='id',
            field=models.CharField(max_length=128, primary_key=True, serialize=False),
        ),
    ]