from django import forms

from bank_statement.bl.validators import id_validation, password_validation, telephone_validation


class UserProfile(forms.Form):
    BANKS = (('TBC', 'TBC'), ('BoG','BoG'), ('Credo', 'Credo'), ('Wise', 'Wise'), ('Liberty', 'Liberty'))
    username = forms.CharField(label='', min_length=3, max_length=15, widget=forms.TextInput(attrs={'placeholder': 'Имя пользователя'}))
    email = forms.EmailField(label='', widget=forms.EmailInput(attrs={'placeholder': 'E-mail'}))
    telephone = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'номер телефона'}), validators=[telephone_validation, ])
    bank = forms.ChoiceField(label='',  choices=BANKS)


class SignUp(forms.Form):
    user_id = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'ID номер'}), validators=[id_validation, ])
    password1 = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder': 'Пароль'}), validators=[password_validation, ])
    password2 = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder': 'Пароль'}))

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Пароли не совпадают")
        return password2


class LoadStatement(forms.Form):
    file = forms.FileField(label='')
