# Generated by Django 4.0.4 on 2022-04-22 01:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0003_rename_tagging_usertagging'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gameround',
            name='resource',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='frontend.resource'),
        ),
    ]