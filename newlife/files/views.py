import string
import random
import os

from django.http import FileResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from database.models import Files
from rest_framework.parsers import MultiPartParser
from files.serializers import FilesSerializer, FileEditSerializer
from files.utils import get_file_or_404, check_file_permission


# Список разрешённых типов файлов
allowed_types = ["application/pdf",
                 "application/msword",
                 "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                 "application/zip",
                 "image/jpeg",
                 "image/png"
]

# Класс для загрузки файлов
class FileUploadView(APIView):
    permission_classes = [permissions.IsAuthenticated]  # Требует аутентификации
    parser_classes = [MultiPartParser]  # Разрешает использование multipart-формата для загрузки файлов

    def post(self, request, *args, **kwargs):
        files = request.FILES.getlist('files[]')  # Получает список файлов из запроса

        if not files:
            # Если файлы не были отправлены, возвращает ошибку
            return Response({
                "success": False,
                "message": "No files provided"
            }, status=status.HTTP_400_BAD_REQUEST)

        response_data = []  # Список для хранения данных об обработанных файлах

        for file in files:
            if file.size > 2 * 1024 * 1024:
                # Проверяет размер файла (не более 2 МБ)
                response_data.append({
                    "success": False,
                    "message": f"File {file.name} exceeds 2 MB size limit",
                })
                continue

            if file.content_type not in allowed_types:
                # Проверяет тип файла (должен быть в списке разрешённых)
                response_data.append({
                    "success": False,
                    "message": f"File {file.name} has an unsupported file type",
                })
                continue

            file_id = ''.join(random.choices(string.ascii_letters + string.digits, k=10))  # Генерирует уникальный идентификатор файла

            # Создаёт запись о файле в базе данных
            user_file = Files.objects.create(
                user=request.user,
                file=file,
                name=file.name,
                file_id=file_id,
            )

            # Сериализует объект файла для ответа
            serializer = FilesSerializer(user_file, context={'request': request})
            response_data.append({
                "success": True,
                "message": "success",
                **serializer.data
            })

        return Response(response_data, status=status.HTTP_200_OK)  # Возвращает ответ с результатами

# Класс для управления файлами (удаление, изменение, скачивание)
class FileEmployView(APIView):
    permission_classes = [permissions.IsAuthenticated]  # Требует аутентификации

    def delete(self, request, file_id, *args, **kwargs):
        # Удаляет файл по его идентификатору
        file_or_error = get_file_or_404(file_id)  # Получает файл или возвращает ошибку 404
        if isinstance(file_or_error, Response):
            return file_or_error

        file = file_or_error
        permission_error = check_file_permission(file, request.user)  # Проверяет права доступа пользователя к файлу
        if permission_error:
            return permission_error

        if os.path.exists(file.file.path):  # Проверяет существование файла на сервере
            os.remove(file.file.path)  # Удаляет файл с сервера

        file.delete()  # Удаляет запись о файле из базы данных

        return Response({
            "success": True,
            "message": "File deleted",
        }, status=status.HTTP_200_OK)

    def patch(self, request, file_id, *args, **kwargs):
        # Обновляет данные файла (например, переименовывает)
        file_or_error = get_file_or_404(file_id)  # Получает файл или возвращает ошибку 404
        if isinstance(file_or_error, Response):
            return file_or_error

        file = file_or_error
        permission_error = check_file_permission(file, request.user)  # Проверяет права доступа пользователя к файлу
        if permission_error:
            return permission_error

        serializer = FileEditSerializer(file, data=request.data, partial=True)  # Сериализует данные для изменения
        if serializer.is_valid():  # Проверяет валидность данных
            serializer.save()  # Сохраняет изменения
            return Response(
                {"success": True, "message": "Renamed"},  # Возвращает успешный ответ
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # Возвращает ошибки валидации

    def get(self, request, file_id):
        # Возвращает файл по его идентификатору
        file = get_file_or_404(file_id)  # Получает файл или возвращает ошибку 404
        if isinstance(file, Response):
            return file

        permission_error = check_file_permission(file, request.user)  # Проверяет права доступа пользователя к файлу
        if permission_error:
            return permission_error

        try:
            file_path = file.file.path  # Получает путь к файлу на сервере
            response = FileResponse(open(file_path, 'rb'), as_attachment=True)  # Создаёт ответ с файлом для скачивания
            response['Content-Disposition'] = f'attachment; filename="{file_path}"'  # Устанавливает заголовок для скачивания файла
            return response
        except FileNotFoundError:
            # Обрабатывает ошибку, если файл не найден
            return Response({
                "success": False,
                "message": "File not found on the server",
            }, status=status.HTTP_404_NOT_FOUND)
