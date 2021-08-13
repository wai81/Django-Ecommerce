from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager  # импорт модели аутентификации
from django.db.models import BooleanField


# Create your models here.

class MyAccountManager(BaseUserManager):
    # фунция создания пользователя
    def create_user(self, first_name, last_name, username, email, password=None):
        if not email:
            raise ValueError('User must have an email address')  # воврвщаем при пустом email

        if not username:
            raise ValueError('User must have an username')  # воврвщаем при пустом email

        user = self.model(
            email=self.normalize_email(email),  # normalize_email - емаил с маленькой буквы
            username=username,
            first_name=first_name,
            last_name=last_name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    # фунция создания супер пользователя
    def create_superuser(self, first_name, last_name, username, email, password):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=50)

    # required это обязательные поля при создании модели account (модели пльзователей)
    date_joined = models.DateTimeField(auto_now=True)
    last_login = models.DateTimeField(auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'  # поле 'username' будет равно 'email'
    # обязательные поля
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    object = MyAccountManager()  # переопределяем что мы используем свой класс создания пользователя MyAccountManager()

    # функция возвращаем объект учетной записи внутри шаблона. Возвращает адрес электронной почты
    def __str__(self):
        return self.email

    # функция возращает является ли пользователем с правами администратора
    def has_perm(self, perm, obj=None):
        return self.is_admin

    #
    def has_module_perms(self, add_label):
        return True
