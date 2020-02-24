# Generated by Django 3.0.3 on 2020-02-24 20:35

from django.db import migrations, models, transaction
import pandas as pd
from faker import Faker


@transaction.atomic
def load_initial_data(apps, schema_editor):
    Profile = apps.get_model("users", "Profile")
    User = apps.get_model("auth", "User")

    df_ratings = pd.read_csv('data/ratings.csv')

    fake = Faker()
    for userid in set(df_ratings['userId'].values):
        user = User(
            username=f"{fake.user_name()}{userid}",
            id=userid,
            password=fake.user_name(),
            is_active=False
        )
        profile = Profile.objects.create(user=user)
        user.profile.is_fake = True
        user.profile.save()
        user.save()


@transaction.atomic
def reverse_func(apps, schema_editor):
    User = apps.get_model("auth", "User")

    User.objects.filter(profile__is_fake=True).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(load_initial_data, reverse_func)
    ]
