# Generated by Django 4.1.7 on 2023-04-05 02:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('postings', '0008_alter_event_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='image',
            field=models.ImageField(default='default_pics/default_event.jpg', upload_to='event_pics'),
        ),
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(default='default_pics/default_post.jpg', upload_to='post_pics'),
        ),
    ]