# Generated by Django 5.1.1 on 2024-10-16 16:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ExtremeFormsApp', '0007_alter_questionlist_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='long_answer_text',
        ),
    ]