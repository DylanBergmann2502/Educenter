# Generated by Django 4.1.7 on 2023-04-09 06:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academics', '0004_remove_course_start_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='scholarship',
            name='scholarship',
            field=models.CharField(default='Quisque quis erat sed sem imperdiet blandit. ', max_length=100),
        ),
        migrations.AlterField(
            model_name='scholarship',
            name='criterium',
            field=models.TextField(default='Phasellus a elit nisl. Morbi at massa non ipsum gravida faucibus. Curabitur at quam eget tortor tempor ultricies a vitae nibh. In quis interdum est. Sed at facilisis diam. Fusce maximus erat augue, facilisis pellentesque lorem porta vitae. Sed nisl ipsum, tristique ac ex tincidunt, fringilla consectetur quam. Morbi tincidunt odio ante, quis mollis dolor dapibus et. Vivamus pretium arcu sem. Donec scelerisque justo feugiat lorem ultricies convallis. Proin at hendrerit felis, id condimentum neque.'),
        ),
    ]
