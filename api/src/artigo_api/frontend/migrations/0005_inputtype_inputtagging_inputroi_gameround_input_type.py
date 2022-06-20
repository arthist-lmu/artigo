# Generated by Django 4.0.5 on 2022-06-14 13:28

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0004_opponentroi_tag_tabooroi_tag_userroi_tag'),
    ]

    operations = [
        migrations.CreateModel(
            name='InputType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, unique=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='InputTagging',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gameround', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='frontend.gameround')),
                ('resource', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='frontend.resource')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='frontend.tag')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='InputROI',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('x', models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(1)])),
                ('y', models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(1)])),
                ('width', models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(1)])),
                ('height', models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(1)])),
                ('gameround', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='frontend.gameround')),
                ('resource', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='frontend.resource')),
                ('tag', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='frontend.tag')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='gameround',
            name='input_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='frontend.inputtype'),
        ),
    ]