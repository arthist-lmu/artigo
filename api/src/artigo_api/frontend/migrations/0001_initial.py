# Generated by Django 3.2.8 on 2021-10-26 11:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(db_index=True, max_length=254, unique=True, verbose_name='email address')),
                ('user_name', models.CharField(blank=True, max_length=100)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Creator',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='Gameround',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(editable=False)),
                ('score', models.PositiveIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Gametype',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('rounds', models.PositiveIntegerField(default=5)),
                ('round_duration', models.PositiveIntegerField(default=60)),
                ('enabled', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hash_id', models.CharField(max_length=256)),
                ('created_start', models.DateField(null=True)),
                ('created_end', models.DateField(null=True)),
                ('location', models.CharField(blank=True, max_length=512)),
                ('institution', models.CharField(blank=True, max_length=512)),
                ('origin', models.URLField(blank=True, max_length=256)),
                ('enabled', models.BooleanField(default=True)),
                ('creators', models.ManyToManyField(to='frontend.Creator')),
            ],
        ),
        migrations.CreateModel(
            name='Source',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('url', models.URLField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('language', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='Title',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=512)),
                ('language', models.CharField(blank=True, max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='Tagging',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(editable=False)),
                ('score', models.PositiveIntegerField(default=0)),
                ('gameround', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='frontend.gameround')),
                ('resource', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='frontend.resource')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='frontend.tag')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='resource',
            name='source',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='frontend.source'),
        ),
        migrations.AddField(
            model_name='resource',
            name='titles',
            field=models.ManyToManyField(to='frontend.Title'),
        ),
        migrations.CreateModel(
            name='Gamesession',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(editable=False)),
                ('gametype', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='frontend.gametype')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='gameround',
            name='gamesession',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='frontend.gamesession'),
        ),
        migrations.AddField(
            model_name='gameround',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
