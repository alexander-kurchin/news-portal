# Generated by Django 4.2.4 on 2023-09-06 14:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0004_alter_post_post_type'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['-created_at', 'title']},
        ),
    ]
