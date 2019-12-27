# Generated by Django 2.2 on 2019-06-15 14:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('svh', '0010_auto_20190521_1814'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='videofolder',
            options={'ordering': ('path',)},
        ),
        migrations.RemoveField(
            model_name='videofolder',
            name='name',
        ),
        migrations.RemoveField(
            model_name='videosource',
            name='name',
        ),
        migrations.AddField(
            model_name='videofolder',
            name='_name',
            field=models.CharField(db_column='name', max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='videosource',
            name='_name',
            field=models.CharField(db_column='name', max_length=500, null=True),
        ),
        migrations.CreateModel(
            name='Gif',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.FileField(upload_to='gifs')),
                ('videosource', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='svh.VideoSource')),
            ],
        ),
    ]
