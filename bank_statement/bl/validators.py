from django import forms
import re

# Проверяет наличие символов в обоих регистрах,
# чисел, спецсимволов и минимальную длину 6 символов
pattern1 = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{6,}$'

# Проверяет наличие символов в обоих регистрах,
# числел и минимальную длину 8 символов
pattern2 = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d]{8,}$'


def id_validation(value):
    if len(value) < 9 or len(value) > 12:
        raise forms.ValidationError("ID номер составляет от 9 до 12 символов")
    elif not value.isdigit():
        raise forms.ValidationError("В ID используются только цифры")


def validate_by_regexp(password, pattern):
    """Валидация пароля по регулярному выражению."""
    if re.match(pattern, password) is None:
        raise forms.ValidationError('Неправильный формат пароля')


def password_validation(password):
    validate_by_regexp(password, pattern2)


def telephone_validation(telephone):
    if len(telephone) != 9:
        raise forms.ValidationError("Введите 9 цифр")
    elif not telephone.isdigit():
        raise forms.ValidationError("Неправильный формат телефона")


