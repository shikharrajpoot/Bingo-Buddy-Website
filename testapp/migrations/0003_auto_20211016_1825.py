# Generated by Django 3.2.8 on 2021-10-16 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testapp', '0002_auto_20211016_1137'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='A',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='question',
            name='B',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='question',
            name='C',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='question',
            name='D',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='question',
            name='answer',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='question',
            name='question',
            field=models.TextField(),
        ),
    ]
