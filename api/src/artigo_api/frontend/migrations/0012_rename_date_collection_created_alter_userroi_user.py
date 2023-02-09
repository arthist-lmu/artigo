# Generated by Django 4.1.6 on 2023-02-07 12:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("frontend", "0011_alter_resource_collection"),
    ]

    operations = [
        migrations.RenameField(
            model_name="collection",
            old_name="date",
            new_name="created",
        ),
        migrations.AlterField(
            model_name="userroi",
            name="user",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="rois",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
