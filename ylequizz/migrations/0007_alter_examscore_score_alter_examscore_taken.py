# Generated by Django 5.1.2 on 2024-10-13 07:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ylequizz', '0006_discouser_examscore'),
    ]

    operations = [
        migrations.AlterField(
            model_name='examscore',
            name='score',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='examscore',
            name='taken',
            field=models.DateTimeField(auto_created=True, blank=True, null=True),
        ),
    ]
