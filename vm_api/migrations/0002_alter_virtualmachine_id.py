# Generated by Django 5.0.3 on 2024-06-22 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vm_api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='virtualmachine',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
