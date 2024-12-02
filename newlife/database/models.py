from django.contrib.auth.models import User, AbstractUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.conf import settings
from .utils import user_directory_path
import os

class CustomUserManager(BaseUserManager):
    # Менеджер для создания кастомных пользователей

    def create_user(self, email, password=None, **extra_fields):
        # Создаёт обычного пользователя с обязательным email
        if not email:
            raise ValueError('Email is required')  # Указывает, что email обязателен
        email = self.normalize_email(email)  # Приводит email к стандартному формату
        user = self.model(email=email, **extra_fields)  # Создаёт экземпляр пользователя
        user.set_password(password)  # Устанавливает пароль для пользователя
        user.save(using=self._db)  # Сохраняет пользователя в базу данных
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        # Создаёт суперпользователя с обязательными правами is_staff и is_superuser
        extra_fields.setdefault('is_staff', True)  # Устанавливает флаг is_staff в True
        extra_fields.setdefault('is_superuser', True)  # Устанавливает флаг is_superuser в True

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')  # Проверяет наличие флага is_staff
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')  # Проверяет наличие флага is_superuser

        return self.create_user(email, password, **extra_fields)  # Возвращает созданного суперпользователя

class CustomUser(AbstractUser):
    # Кастомная модель пользователя с заменой username на email
    username = None  # Удаляет поле username
    email = models.EmailField(unique=True)  # Добавляет поле email с уникальным значением
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',  # Устанавливает уникальное имя для связи
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_permissions_set',  # Устанавливает уникальное имя для связи
        blank=True
    )

    objects = CustomUserManager()  # Заменяет менеджер пользователей на кастомный

    USERNAME_FIELD = 'email'  # Указывает email как поле для аутентификации
    REQUIRED_FIELDS = []  # Указывает, что дополнительных обязательных полей нет

    def __str__(self):
        # Возвращает строковое представление пользователя
        return self.email

class Files(models.Model):
    # Модель для представления файлов, связанных с пользователями
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,  # Удаляет файл при удалении пользователя
        related_name='files',  # Устанавливает связь с именем 'files' у пользователя
        verbose_name='Пользователь'
    )
    file = models.FileField(
        upload_to=user_directory_path,  # Указывает путь для загрузки файла
        verbose_name='Файл'
    )
    name = models.CharField(max_length=255, verbose_name='Владелец')  # Добавляет имя файла
    file_id = models.CharField(max_length=10, unique=True)  # Указывает уникальный идентификатор файла
    shared_with = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='FileAccess',  # Указывает промежуточную модель для связи
        related_name="shared_files"
    )

    class Meta:
        verbose_name = 'Файл'
        verbose_name_plural = 'Файлы'
        unique_together = ('user', 'file_id')  # Устанавливает уникальность пары user-file_id

    def __str__(self):
        # Возвращает строковое представление файла
        return self.name

    def save(self, *args, **kwargs):
        # Переопределяет метод сохранения для уникализации имени файла
        if not self.pk:  # Проверяет, создаётся ли новый объект
            file_name, file_extension = os.path.splitext(self.file.name)  # Разделяет имя файла и его расширение

            new_name = file_name + file_extension  # Формирует имя файла по умолчанию
            counter = 1  # Инициализирует счётчик для уникализации имени

            while Files.objects.filter(file__endswith=new_name).exists():
                # Проверяет существование файла с таким именем
                new_name = file_name + '_' + str(counter) + file_extension  # Создаёт новое уникальное имя
                self.name = f"{file_name} ({counter}){file_extension}"  # Обновляет название файла
                counter += 1  # Увеличивает счётчик

            self.file.name = new_name  # Устанавливает новое имя файла

        super().save(*args, **kwargs)  # Вызывает метод сохранения родительского класса

    def delete(self, *args, **kwargs):
        # Переопределяет метод удаления для удаления файла с диска
        if os.path.exists(self.file.path):  # Проверяет, существует ли файл на диске
            os.remove(self.file.path)  # Удаляет файл
        super().delete(*args, **kwargs)  # Вызывает метод удаления родительского класса

class FileAccess(models.Model):
    # Модель для управления доступом пользователей к файлам
    ACCESS_CHOICES = [
        ('author', 'Автор'),  # Указывает, что пользователь является автором
        ('co-author', 'Соавтор'),  # Указывает, что пользователь является соавтором
    ]

    file = models.ForeignKey(
        Files,
        on_delete=models.CASCADE,  # Удаляет права доступа при удалении файла
        verbose_name="Файл"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,  # Удаляет права доступа при удалении пользователя
        verbose_name="Пользователь файла"
    )
    access_type = models.CharField(
        max_length=20,
        choices=ACCESS_CHOICES,  # Устанавливает типы доступа
        default="co-author",  # Устанавливает тип доступа по умолчанию
        verbose_name="Тип доступа"
    )

    class Meta:
        verbose_name = "Право"
        verbose_name_plural = "Права"
