# Generated by Django 4.0.3 on 2022-03-23 13:47

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import frontend.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('username', models.CharField(max_length=256, unique=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_uploader', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('first_name', models.CharField(max_length=256)),
                ('last_name', models.CharField(max_length=256)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Creator',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('wikidata_id', models.CharField(blank=True, max_length=256)),
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
                ('name', models.CharField(max_length=256, unique=True)),
                ('enabled', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='OpponentType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('wikidata_id', models.CharField(blank=True, max_length=256)),
                ('hash_id', models.CharField(max_length=256)),
                ('created_start', models.DateField(null=True)),
                ('created_end', models.DateField(null=True)),
                ('location', models.CharField(blank=True, max_length=512)),
                ('institution', models.CharField(blank=True, max_length=512)),
                ('origin', models.URLField(blank=True, max_length=256)),
                ('enabled', models.BooleanField(default=True)),
                ('creators', models.ManyToManyField(to='frontend.creator')),
            ],
        ),
        migrations.CreateModel(
            name='ScoreType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, unique=True)),
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
            name='SuggesterType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='TabooType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', frontend.fields.NameField(max_length=256)),
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
                ('suggested', models.BooleanField(default=False)),
                ('created', models.DateTimeField(editable=False)),
                ('score', models.PositiveIntegerField(default=0)),
                ('gameround', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='frontend.gameround')),
                ('resource', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='taggings', to='frontend.resource')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='frontend.tag')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TabooTagging',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gameround', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='frontend.gameround')),
                ('resource', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='frontend.resource')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='frontend.tag')),
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
            field=models.ManyToManyField(to='frontend.title'),
        ),
        migrations.CreateModel(
            name='OpponentTagging',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_after', models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('gameround', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='frontend.gameround')),
                ('resource', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='frontend.resource')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='frontend.tag')),
            ],
        ),
        migrations.CreateModel(
            name='Gamesession',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(editable=False)),
                ('rounds', models.PositiveIntegerField(default=5, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(100)])),
                ('round_duration', models.PositiveIntegerField(default=60, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(3600)])),
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
            name='opponent_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='frontend.opponenttype'),
        ),
        migrations.AddField(
            model_name='gameround',
            name='resource',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='frontend.resource'),
        ),
        migrations.AddField(
            model_name='gameround',
            name='score_types',
            field=models.ManyToManyField(to='frontend.scoretype'),
        ),
        migrations.AddField(
            model_name='gameround',
            name='suggester_types',
            field=models.ManyToManyField(to='frontend.suggestertype'),
        ),
        migrations.AddField(
            model_name='gameround',
            name='taboo_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='frontend.tabootype'),
        ),
        migrations.AddField(
            model_name='gameround',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
