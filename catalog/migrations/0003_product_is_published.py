# Generated by Django 5.1.1 on 2024-10-17 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0002_alter_category_options"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="is_published",
            field=models.BooleanField(default=False, verbose_name="Опубликовано"),
        ),
    ]
