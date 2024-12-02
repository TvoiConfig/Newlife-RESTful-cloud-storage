from rest_framework import serializers
from database.models import Files

# Сериализатор для работы с моделью Files
class FilesSerializer(serializers.ModelSerializer):
    # Добавляет поле для получения URL файла
    url = serializers.SerializerMethodField()

    class Meta:
        model = Files  # Указывает модель, с которой работает сериализатор
        fields = ('file', 'user', 'name', 'file_id', 'url')  # Определяет поля, включённые в сериализацию

    def get_url(self, obj):
        # Генерирует абсолютный URL для файла на основе его file_id
        # obj - экземпляр модели Files
        return self.context['request'].build_absolute_uri(f'/files/{obj.file_id}/')
        # Использует контекст запроса для получения базового URL и формирует полный путь к ресурсу

# Сериализатор для редактирования модели Files
class FileEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Files  # Указывает модель, с которой работает сериализатор
        fields = ('name',)  # Определяет, что редактируется только поле name

    def validate(self, data):
        # Валидирует поле name перед сохранением
        name = data.get('name', '').strip()  # Удаляет лишние пробелы из имени
        if not name:
            raise serializers.ValidationError('Name cannot be empty')  # Проверяет, что имя не пустое
        data['name'] = name  # Сохраняет очищенное имя
        return data  # Возвращает валидированные данные
