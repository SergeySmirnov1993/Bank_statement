from django.urls import path

from bank_statement import views

urlpatterns = [

    path('', views.users_personal_acc, name='users-acc'),
    path("register", views.register_request, name="register"),
    path("load-statement", views.load_statement, name="load-statement"),
]
