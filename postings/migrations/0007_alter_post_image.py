# Generated by Django 4.1.7 on 2023-04-05 00:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('postings', '0006_alter_event_date_time_alter_event_event_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, default='default_pics/default_post.jpg', null=True, upload_to='post_pics'),
        ),
    ]