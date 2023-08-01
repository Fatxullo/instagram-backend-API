from django.contrib import admin
from .models import User, UserConfirmation

 

@admin.register(User)
class UserAdminView(admin.ModelAdmin):
    list_display = ['id', 'email', 'phone_number','username']
    
@admin.register(UserConfirmation)
class UserConfirmationView(admin.ModelAdmin):
    list_display = ['verify_type', 'user', 'code']