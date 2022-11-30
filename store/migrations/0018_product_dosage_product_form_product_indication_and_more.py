# Generated by Django 4.1.3 on 2022-11-21 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0017_themesetting'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='dosage',
            field=models.CharField(blank=True, default='100mg', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='form',
            field=models.CharField(blank=True, choices=[('tabs', 'TABLET'), ('syrup', 'SYRUP'), ('suspension', 'SUSPENSION'), ('injection', 'INJECTION')], default='tabs', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='indication',
            field=models.TextField(blank=True, default='ailment', max_length=2000, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='prescription',
            field=models.CharField(blank=True, default='daily', max_length=1000, null=True),
        ),
    ]
