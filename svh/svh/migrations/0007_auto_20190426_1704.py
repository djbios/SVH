# Generated by Django 2.2 on 2019-04-26 14:04

from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('svh', '0006_auto_20190424_1326'),
    ]

    operations = [
        migrations.AlterField(
            model_name='videofile',
            name='path',
            field=models.CharField(max_length=2000, unique=True),
        ),
        migrations.AlterField(
            model_name='videosource',
            name='path',
            field=models.CharField(max_length=2000, unique=True),
        ),
        migrations.CreateModel(
            name='VideoFolder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('path', models.CharField(max_length=2000, unique=True)),
                ('type', models.CharField(max_length=200, null=True)),
                ('description', models.TextField(null=True)),
                ('preview_path', models.CharField(max_length=2000, null=True)),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('parent', mptt.fields.TreeForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='folder_parent', to='svh.VideoFolder')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
