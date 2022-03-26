from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from bank_statement import views

urlpatterns = [

    path('', views.users_personal_acc, name='users-acc'),
    path("register", views.register_request, name="register"),
    path("load-statement", views.load_statement, name="load-statement"),
    path("update-profile", views.update_user_profile, name="update-profile"),
    path("view-users", views.view_users, name="view-users"),
    path("edit-user/<int:user_id>", views.edit_user, name="edit-user"),
    path("add-file/<int:user_id>", views.add_file, name="add-file"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
