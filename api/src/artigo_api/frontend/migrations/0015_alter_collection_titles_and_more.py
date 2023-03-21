# Generated by Django 4.1.7 on 2023-02-27 15:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("frontend", "0014_collectiontitle_remove_collection_name_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="collection",
            name="titles",
            field=models.ManyToManyField(related_name="collections", to="frontend.collectiontitle"),
        ),
        migrations.AddConstraint(
            model_name="collectiontitle",
            constraint=models.UniqueConstraint(fields=("name", "language"), name="name_language_unique"),
        ),
    ]