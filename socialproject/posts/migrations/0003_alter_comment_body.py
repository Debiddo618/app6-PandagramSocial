# Generated by Django 4.2.6 on 2023-10-20 21:02

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("posts", "0002_post_likedby_alter_post_image_alter_post_slug_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="comment",
            name="body",
            field=models.CharField(max_length=100),
        ),
    ]
