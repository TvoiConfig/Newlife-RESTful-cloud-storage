from rest_framework import serializers
from database.models import Files, FileAccess

# Сериализатор для работы с доступами к файлам
class FileAccessSerializer(serializers.ModelSerializer):
    # Добавляет поле full_name для отображения полного имени пользователя
    full_name = serializers.SerializerMethodField()
    # Поле email, берется из поля email пользователя
    email = serializers.EmailField(source='user.email')
    # Поле type, переименованное из access_type
    type = serializers.CharField(source='access_type')

    class Meta:
        model = FileAccess  # Указывает модель, с которой работает сериализатор
        fields = ['full_name', 'email', 'type']  # Определяет поля, которые будут включены в сериализацию

    def get_full_name(self, obj):
        # Метод для получения полного имени пользователя
        # obj - экземпляр модели FileAccess
        return f"{obj.user.first_name} {obj.user.last_name}"  # Возвращает строку с полным именем

# Сериализатор для работы с файлами
class FileSerializer(serializers.ModelSerializer):
    # Добавляет поле accesses, которое сериализует доступы к файлу
    accesses = FileAccessSerializer(source='fileaccess_set', many=True, read_only=True)
    # Добавляет поле url для получения абсолютного URL файла
    url = serializers.SerializerMethodField()

    class Meta:
        model = Files  # Указывает модель, с которой работает сериализатор
        fields = ['file_id', 'name', 'url', 'accesses']  # Определяет поля, которые будут включены в сериализацию

    def get_url(self, obj):
        # Генерирует абсолютный URL для доступа к файлу
        request = self.context.get('request')  # Получает объект запроса из контекста
        return request.build_absolute_uri(f"/files/{obj.id}")  # Строит полный URL для скачивания файла
