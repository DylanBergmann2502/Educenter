# Generated by Django 4.1.7 on 2023-04-09 08:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academics', '0009_remove_course_has_scholarship'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scholarship',
            name='criterium',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='scholarship',
            name='scholarship',
            field=models.CharField(max_length=100),
        ),
    ]