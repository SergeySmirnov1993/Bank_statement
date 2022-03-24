from openpyxl import load_workbook
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


from bank_statement import models, forms
from bank_statement.bl.file_logic import calculate


def register_request(request):
    if request.method == 'GET':
        request.session.clear()
        html = 'Заполните регистрационные данные'
        form = forms.SignUp()
        return render(request, 'registration/register.html', {'html': html, 'form': form})

    elif request.method == 'POST':
        form = forms.SignUp(request.POST)
        if form.is_valid():
            username = form.cleaned_data['user_id']
            password = form.cleaned_data['password1']
            is_user = User.objects.filter(username=username).exists()
            if is_user:
                html = "Пользователь с указанным ID уже зарегистрирован"
                return render(request, 'registration/register.html', {'html': html, 'form': form})

            else:
                new_user = User.objects.create_user(username=username, password=password)
                new_user.save()
                return redirect('login')
        else:
            html = "Введены неверные данные"
            return render(request, 'registration/register.html', {'html': html, 'form': form})


@login_required
def users_personal_acc(request):
    if request.method == 'GET':
        form = forms.UserProfile()
        user = User.objects.get(id=request.user.id)
        is_profile = models.Profile.objects.filter(user=user).exists()
        if is_profile:
            form.fields['username'].initial = user.profile.username
            form.fields['email'].initial = user.profile.email
            form.fields['telephone'].initial = user.profile.telephone
            form.fields['bank'].initial = user.profile.bank
        context = {'form': form}
        return render(request, 'users_personal_acc.html', context)

    elif request.method == 'POST':
        form = forms.UserProfile(request.POST)
        context = {'form': form}
        profile = models.Profile()
        if form.is_valid():
            profile.user = User.objects.get(id=request.user.id)
            profile.username = form.cleaned_data['username']
            profile.email = form.cleaned_data['email']
            profile.telephone = form.cleaned_data['telephone']
            profile.bank = form.cleaned_data['bank']
            profile.save()
            context['html'] = "Даннные успешно сохранены"
            return render(request, 'users_personal_acc.html', context)

        else:
            context['html'] = "Введены неверные данные"
            return render(request, 'users_personal_acc.html', context)


@login_required
def load_statement(request):
    if request.method == 'GET':
        form = forms.LoadStatement()
        context = {'form': form}
        return render(request, 'load_statement.html', context)

    elif request.method == 'POST':
        form = forms.LoadStatement(request.POST, request.FILES)
        if form.is_valid():
            wb = load_workbook(filename=request.FILES['file'].file)
            # Check `anotherSheet`
            # sheet.title

            # Get currently active sheet
            sheet = wb.active
            amount = f'Всего в выписке: {calculate(sheet)}'
            request.session['amount'] = amount
            return redirect('load-statement')
