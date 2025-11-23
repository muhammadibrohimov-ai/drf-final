from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


# Register your models here.


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    
    list_display = ('phone', 'fullname', 'email', 'is_staff', 'is_active', 'is_superuser')
    search_fields = ('phone', 'fullname', 'email')
    ordering = ('phone',)
    
    
    fieldsets = (
        ('Asosiy ma\'lumotlar', {
            'fields' : ('phone', 'password', 'email', 'first_name', 'last_name', 'profession', 'image'),
        }),
        ('Ruxsatlar' , {
            'fields' : ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Tizim ma\'lumotlari', {
            'fields' : ('last_login', 'date_joined'),
        })
    )
    
    add_fieldsets = (
        (None, {
            'classes' : ('wide', ),
            'fields' : ('phone', 'email', 'first_name', 'last_name', 'profession', 'image', 'password1', 'password2', 'is_staff', 'is_superuser'),
        })
    )

