# Generated by Django 4.2 on 2023-04-29 12:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('idgenerator', '0002_alter_studentidentitycard_image_file_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='id_card',
            field=models.ImageField(blank=True, null=True, upload_to='id_cards/'),
        ),
    ]
