from django.contrib import admin
from bank_statement import models


# Register your models here.
admin.site.register(models.Profile)
admin.site.register(models.UserStatement)
admin.site.register(models.Document)


