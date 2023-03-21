# Generated by Django 4.1.7 on 2023-02-24 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("frontend", "0013_alter_collection_access"),
    ]

    operations = [
        migrations.CreateModel(
            name="CollectionTitle",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=512)),
                ("language", models.CharField(blank=True, max_length=256)),
            ],
        ),
        migrations.RemoveField(
            model_name="collection",
            name="name",
        ),
        migrations.AddField(
            model_name="collection",
            name="titles",
            field=models.ManyToManyField(to="frontend.collectiontitle"),
        ),
    ]