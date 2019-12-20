# Generated by Django 2.2 on 2019-10-21 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('svh', '0015_auto_20190827_2004'),
    ]

    operations = [
        migrations.RenameField(
            model_name='videofile',
            old_name='path',
            new_name='fileId',
        ),
        migrations.RemoveField(
            model_name='gif',
            name='image',
        ),
        migrations.RemoveField(
            model_name='preview',
            name='image',
        ),
        migrations.RemoveField(
            model_name='preview',
            name='pos_seconds',
        ),
        migrations.RemoveField(
            model_name='videofile',
            name='sizeBytes',
        ),
        migrations.AddField(
            model_name='gif',
            name='fileId',
            field=models.CharField(default='', max_length=2000, unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='preview',
            name='fileId',
            field=models.CharField(default='', max_length=2000),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='videofile',
            name='format',
            field=models.CharField(max_length=200),
        ),
    ]
