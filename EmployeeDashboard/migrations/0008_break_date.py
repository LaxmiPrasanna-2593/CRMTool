# Generated by Django 5.0.2 on 2024-11-08 10:31

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EmployeeDashboard', '0007_rename_leave_date_leave_end_date_leave_start_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='break',
            name='date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]