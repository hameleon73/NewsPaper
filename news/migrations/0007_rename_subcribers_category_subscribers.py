# Generated by Django 4.2.2 on 2023-07-10 14:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0006_category_subcribers_delete_subscriber'),
    ]

    operations = [
        migrations.RenameField(
            model_name='category',
            old_name='subcribers',
            new_name='subscribers',
        ),
    ]
