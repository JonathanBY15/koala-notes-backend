# Generated by Django 5.0.7 on 2024-07-16 02:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='note',
            name='user',
        ),
        migrations.AlterField(
            model_name='note',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]