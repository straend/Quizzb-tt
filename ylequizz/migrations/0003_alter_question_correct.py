# Generated by Django 5.1.2 on 2024-10-12 09:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ylequizz', '0002_exam_name_exam_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='correct',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='correct', to='ylequizz.choice'),
        ),
    ]
