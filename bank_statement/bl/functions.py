from datetime import date

from django.contrib.auth.models import User
from bank_statement import models


CURRENT_AVAILABLE_BANKS = {'TBC'}  # update after add work with new statements


def is_currently_service(bank):
    return True if bank in CURRENT_AVAILABLE_BANKS else False


def get_user(user_id):
    return User.objects.get(id=user_id)


def get_users():
    all_users = User.objects.all()
    users = set()
    # exclude admins and superusers
    for user in all_users:
        if user.username.isdigit():
            users.add(user)
    return users


def create_user(username, password):
    new_user = User.objects.create_user(username=username, password=password)
    new_user.save()
    return new_user


def create_user_statement(sum_total, user):
    statement = user.statement if statement_exists(user) else models.UserStatement()
    today = date.today()
    month = 12 if today.month == 1 else today.month - 1
    statement.statement_date = date(today.year, month, 1)
    statement.sum_total = sum_total
    statement.user = user
    statement.save()
    return True


def user_exists(username):
    return User.objects.filter(username=username).exists()


def profile_exists(user):
    return models.Profile.objects.filter(user=user).exists()


def statement_exists(user):
    return models.UserStatement.objects.filter(user=user).exists()


def is_manager(user):
    return user.groups.filter(name='Managers').exists()


def get_files(user_id):
    files = models.Document.objects.filter(user_id=user_id).all()
    data = set()
    for file in files:
        data.add(file.description)
    return data