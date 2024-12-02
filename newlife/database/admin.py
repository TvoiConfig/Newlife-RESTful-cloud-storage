from django.contrib import admin
from database.models import CustomUser, Files, FileAccess

# Регистрирует модель CustomUser в админ-панели
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    # Определяет структуру отображения и редактирования пользователя в админке
    fieldsets = (
        ("Основная информация", {'fields': ('email', 'password')}),  # Указывает поля основной информации
        ('Личная информация', {'fields': ('first_name', 'last_name')}),  # Указывает поля для личной информации
        ('Разрешения', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),  # Указывает поля управления доступом
        ('Важные даты', {'fields': ('last_login', 'date_joined')}),  # Указывает поля с важными датами
    )

# Регистрирует модель Files в админ-панели
@admin.register(Files)
class FilesAdmin(admin.ModelAdmin):
    # Определяет отображаемые столбцы в списке объектов
    list_display = ('file', 'user', 'file_id', 'name')  # Указывает поля, которые отображаются в списке файлов

# Регистрирует модель FileAccess в админ-панели
@admin.register(FileAccess)
class FileAccessAdmin(admin.ModelAdmin):
    # Определяет отображаемые столбцы в списке объектов
    list_display = ('file', 'user', 'access_type')  # Указывает поля, которые отображаются в списке прав доступа
