# Generated by Django 5.0.2 on 2024-11-12 09:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EmployeeDashboard', '0010_project_dailyupdatetaskform'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='end_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]