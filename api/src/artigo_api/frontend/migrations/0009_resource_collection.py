# Generated by Django 4.1.5 on 2023-02-02 11:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("frontend", "0008_collection"),
    ]

    operations = [
        migrations.AddField(
            model_name="resource",
            name="collection",
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to="frontend.collection"),
        ),
    ]
