# Generated by Django 3.2 on 2021-04-12 02:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Enrolled_Classes', '0003_alter_enrolled_class_professor'),
        ('User_Management', '0003_alter_profile_course'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='course',
            field=models.ManyToManyField(blank=True, to='Enrolled_Classes.Enrolled_Class'),
        ),
    ]