# Generated by Django 4.1.1 on 2022-10-19 23:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0005_inputtype_inputtagging_inputroi_gameround_input_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gameround',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='gamerounds', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='gamesession',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='gamesessions', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='inputroi',
            name='gameround',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)ss', to='frontend.gameround'),
        ),
        migrations.AlterField(
            model_name='inputtagging',
            name='gameround',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)ss', to='frontend.gameround'),
        ),
        migrations.AlterField(
            model_name='opponentroi',
            name='gameround',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)ss', to='frontend.gameround'),
        ),
        migrations.AlterField(
            model_name='opponenttagging',
            name='gameround',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)ss', to='frontend.gameround'),
        ),
        migrations.AlterField(
            model_name='tabooroi',
            name='gameround',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)ss', to='frontend.gameround'),
        ),
        migrations.AlterField(
            model_name='tabootagging',
            name='gameround',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)ss', to='frontend.gameround'),
        ),
        migrations.AlterField(
            model_name='userroi',
            name='gameround',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)ss', to='frontend.gameround'),
        ),
        migrations.AlterField(
            model_name='usertagging',
            name='gameround',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)ss', to='frontend.gameround'),
        ),
        migrations.AlterField(
            model_name='usertagging',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='taggings', to=settings.AUTH_USER_MODEL),
        ),
    ]