# Generated by Django 2.1.1 on 2018-10-04 07:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cataloger', '0005_auto_20181003_2316'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dataset',
            name='publisher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
    ]
