# Generated by Django 4.1.3 on 2022-11-27 06:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0026_category_indication'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='drug_class',
            field=models.ManyToManyField(default='analgesic', to='store.category'),
        ),
    ]
