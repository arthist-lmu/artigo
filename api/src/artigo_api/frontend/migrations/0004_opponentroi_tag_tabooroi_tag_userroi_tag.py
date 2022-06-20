# Generated by Django 4.0.5 on 2022-06-09 15:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0003_rename_gametype_gamesession_game_type_userroi_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='opponentroi',
            name='tag',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='frontend.tag'),
        ),
        migrations.AddField(
            model_name='tabooroi',
            name='tag',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='frontend.tag'),
        ),
        migrations.AddField(
            model_name='userroi',
            name='tag',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='frontend.tag'),
        ),
    ]