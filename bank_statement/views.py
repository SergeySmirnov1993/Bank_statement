import datetime

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.files.storage import FileSystemStorage

from bank_statement import models, forms
from bank_statement.bl import file_logic
from bank_statement.bl import functions


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
            if functions.user_exists(username):
                html = "Пользователь с указанным ID уже зарегистрирован"
                return render(request, 'registration/register.html', {'html': html, 'form': form})

            else:
                functions.create_user(username, password)
                return redirect('login')
        else:
            html = "Введены неверные данные"
            return render(request, 'registration/register.html', {'html': html, 'form': form})


@login_required
def users_personal_acc(request):
    if request.method == 'GET':
        user = functions.get_user(request.user.id)
        if functions.is_manager(user):
            return redirect('view-users')

        form = forms.UserProfile()
        if functions.profile_exists(user):
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
            profile.user = functions.get_user(request.user.id)
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
def update_user_profile(request):
    if request.method == 'POST':
        form = forms.UserProfile(request.POST)
        context = {'form': form}
        profile = functions.get_user(request.user.id).profile
        if form.is_valid():
            profile.username = form.cleaned_data['username']
            profile.email = form.cleaned_data['email']
            profile.telephone = form.cleaned_data['telephone']
            profile.bank = form.cleaned_data['bank']
            profile.save()
            context['html'] = "Даннные успешно обновлены"
            return render(request, 'users_personal_acc.html', context)

        else:
            context['html'] = "Введены неверные данные"
            return render(request, 'users_personal_acc.html', context)


@login_required
def load_statement(request):
    if request.method == 'GET':
        context = {}
        user = functions.get_user(request.user.id)
        if functions.profile_exists(user):
            if functions.statement_exists(user):
                sum_total = user.statement.sum_total
                date = user.statement.add_date
                msg = f'Сумма по выписке за пердыдущий месяц составляет: {sum_total} GEL.\nДата добавления выписки: {date}.'
                context['statement_amount'] = msg
            if functions.is_currently_service(user.profile.bank):
                form = forms.LoadStatement()
                context['form'] = form
                return render(request, 'load_statement.html', context)

            else:
                context['msg'] = 'Извините, на данный момент обработка выписки Вашего банка недоступна.'
                return render(request, 'load_statement.html', context)

        else:
            context['msg'] = 'Для загрузки выписки заполните профиль в личном кабинете'
            return render(request, 'load_statement.html', context)

    elif request.method == 'POST':
        form = forms.LoadStatement(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file'].file
            user = functions.get_user(request.user.id)
            if file_logic.is_correct_statement(file, user):
                sum_total = file_logic.calculate(file)
                functions.create_user_statement(sum_total, user)
                return redirect('load-statement')

            else:
                context = {'msg': 'Выписка не соответсвует требованиям'}
                return render(request, 'load_statement.html', context)


@login_required
@user_passes_test(functions.is_manager)
def view_users(request):
    if request.method == 'GET':
        users = functions.get_users()
        context = {'users': users}
        return render(request, 'view_users.html', context)


@login_required
@user_passes_test(functions.is_manager)
def edit_user(request, user_id):
    if request.method == 'GET':
        user = functions.get_user(user_id)
        edit_form = forms.MangersForm()
        edit_form.fields['user_id'].initial = user.username
        edit_form.fields['password'].initial = user.profile.password
        edit_form.fields['is_active'].initial = user.profile.is_active
        edit_form.fields['sum_total'].initial = user.statement.sum_total
        files = functions.get_files(user.username)
        context = {'form': edit_form, 'user_id': user.username, 'files': files}
        return render(request, 'edit_user.html', context)

    if request.method == 'POST':
        user = functions.get_user(user_id)
        form = forms.MangersForm(request.POST)
        if form.is_valid():
            user.username = form.cleaned_data['user_id']
            user.save()
            user.profile.password = form.cleaned_data['password']
            user.profile.is_active = form.cleaned_data['is_active']
            user.profile.save()
            user.statement.sum_total = form.cleaned_data['sum_total']
            user.statement.save()
            context = {'form': form, 'user_id': user.username}
            return render(request, 'edit_user.html', context)


@login_required
@user_passes_test(functions.is_manager)
def add_file(request, user_id):
    if request.method == 'GET':
        file_form = forms.LoadFile()
        context = {'file_form': file_form}
        return render(request, 'add_file.html', context)

    if request.method == 'POST':
        form = forms.LoadFile(request.POST, request.FILES)
        new_file = models.Document()
        file_form = forms.LoadFile()
        context = {'file_form': file_form}

        if form.is_valid():
            name = form.cleaned_data['file'].name
            format = name.split('.')[-1]

            if format == 'pdf':
                new_file.user_id = user_id
                new_file.description = form.cleaned_data['file'].name
                new_file.document = request.FILES['file']
                new_file.save()
                context['msg'] = 'Файл успешно сохранен'
                return render(request, 'add_file.html', context)

            else:
                context['msg'] = 'Файл не соответсвует формату .pdf'
                return render(request, 'add_file.html', context)
