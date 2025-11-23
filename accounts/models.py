from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser, BaseUserManager


# Create your models here.


class CustomUserManager(BaseUserManager):
    def create_user(self, phone, password = None, **extra_fields):
        if not phone:
            raise ValueError("Foydalanuvhci telefon raqamini kiritshi muajburiy")
        user = self.model(phone=phone, **extra_fields)
        if not password:
            raise ValueError("Fodyalanuvchi parol kiritishi majburiy")
        user.set_password(password)
        user.save(using = self._db)
        return user

    def create_superuser(self, phone, password = None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if not password:
            raise ValueError("Superuser uchun parol majburiy")

        return self.create_user(phone, password, **extra_fields)


class CustomUser(AbstractUser, CustomUserManager):
    phone = models.CharField(max_length=20, unique=True)
    profession = models.CharField(max_length=50)
    image = models.FileField(upload_to = 'users')

    objects = CustomUserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['email']

    @property
    def fullname(self):
        return f'{self.first_name} {self.last_name}'
