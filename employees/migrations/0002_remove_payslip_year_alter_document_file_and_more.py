# Generated by Django 5.2.3 on 2025-06-15 16:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payslip',
            name='year',
        ),
        migrations.AlterField(
            model_name='document',
            name='file',
            field=models.FileField(upload_to='documents/'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='employee_id',
            field=models.CharField(default='EMP-A532D6A6'),
        ),
    ]
