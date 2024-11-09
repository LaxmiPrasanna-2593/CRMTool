# Generated by Django 5.0.2 on 2024-11-07 04:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EmployeeDashboard', '0004_task'),
    ]

    operations = [
        migrations.CreateModel(
            name='TLTasks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('assigned_to', models.CharField(max_length=100)),
                ('assigned_by', models.CharField(max_length=100)),
                ('priority', models.CharField(choices=[('High', 'High'), ('Medium', 'Medium'), ('Low', 'Low')], max_length=20)),
                ('due_date', models.DateField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('In Progress', 'In Progress'), ('Completed', 'Completed')], default='Pending', max_length=20)),
            ],
        ),
    ]
