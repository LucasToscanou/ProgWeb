# Generated by Django 5.1.1 on 2024-10-17 00:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ExtremeFormsApp', '0008_remove_question_long_answer_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='questionlist',
            name='shareable_link',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
