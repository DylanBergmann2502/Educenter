# Generated by Django 4.1.7 on 2023-04-06 01:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('academics', '0003_remove_requirement_course_course_method_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='start_date',
        ),
    ]
