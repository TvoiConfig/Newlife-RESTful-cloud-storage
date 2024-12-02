from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from database.models import Files, FileAccess, CustomUser
from set_files_access.serializers import FileSerializer, FileAccessSerializer

class AccessView(APIView):
    permission_classes = [IsAuthenticated]  # Указывает, что доступ к представлению имеет только аутентифицированный пользователь

    def post(self, request, file_id):
        # Получаем файл по строковому ID из базы данных или возвращаем 404 ошибку
        file = get_object_or_404(Files, file_id=file_id)

        # Проверяем, является ли текущий пользователь владельцем файла
        if file.user != request.user:
            return Response({"message": "Forbidden for you"}, status=status.HTTP_403_FORBIDDEN)  # Указывает, что доступ запрещен

        # Получаем email пользователя для добавления доступа
        email = request.data.get('email')
        user = get_object_or_404(CustomUser, email=email)  # Находим пользователя по email или возвращаем 404 ошибку

        # Добавляем право доступа для найденного пользователя
        FileAccess.objects.create(file=file, user=user)  # Указывает, что создаётся новое право доступа для файла

        # Получаем список всех пользователей, имеющих доступ к файлу
        accesses = FileAccess.objects.filter(file=file)  # Указывает, что мы получаем все права доступа для конкретного файла
        serializer = FileAccessSerializer(accesses, many=True)  # Сериализуем данные о доступах
        return Response(serializer.data, status=status.HTTP_200_OK)  # Возвращаем список пользователей с доступом

    def delete(self, request, file_id):
        # Получаем файл по строковому ID из базы данных или возвращаем 404 ошибку
        file = get_object_or_404(Files, file_id=file_id)

        # Проверка, что пользователь является владельцем файла, иначе доступ запрещен
        if file.user != request.user:
            return Response({"detail": "Access denied."}, status=status.HTTP_403_FORBIDDEN)  # Указывает, что доступ запрещён

        # Получаем email пользователя для удаления доступа
        email = request.data.get('email')
        user = get_object_or_404(CustomUser, email=email)  # Находим пользователя по email или возвращаем 404 ошибку

        # Проверка, что не пытаемся удалить доступ себе
        if user == request.user:
            return Response({"detail": "Cannot remove yourself."}, status=status.HTTP_403_FORBIDDEN)  # Указывает, что нельзя удалить доступ себе

        # Удаляем право доступа для пользователя, если оно существует
        access = FileAccess.objects.filter(file=file, user=user).first()  # Находим первое совпадение доступа
        if not access:
            return Response({"detail": "Access not found."}, status=status.HTTP_404_NOT_FOUND)  # Указывает, что доступ не найден

        access.delete()  # Удаляет право доступа

        # Получаем обновлённый список пользователей с доступом
        accesses = FileAccess.objects.filter(file=file)

        # Формируем список пользователей с доступом и их ролью
        response_data = []
        for access in accesses:
            # Формируем полное имя пользователя (имя + фамилия)
            fullname = f"{access.user.first_name} {access.user.last_name}".strip()
            if not fullname:
                fullname = access.user.email  # Если полное имя отсутствует, используем email

            # Формируем данные для ответа
            user_data = {
                "fullname": fullname,  # Имя пользователя
                "email": access.user.email,  # Email пользователя
                "type": access.access_type  # Тип доступа (автор или соавтор)
            }
            response_data.append(user_data)  # Добавляем данные пользователя в ответ

        return Response(response_data, status=status.HTTP_200_OK)  # Возвращаем обновлённый список пользователей с доступом

class UserFilesView(APIView):
    permission_classes = [IsAuthenticated]  # Указывает, что доступ имеет только аутентифицированный пользователь

    def get(self, request):
        # Получаем все файлы, принадлежащие текущему пользователю
        files = Files.objects.filter(user=request.user)  # Указывает, что извлекаются только файлы, принадлежащие пользователю
        serializer = FileSerializer(files, many=True, context={'request': request})  # Сериализуем данные о файлах
        return Response(serializer.data, status=status.HTTP_200_OK)  # Возвращаем данные файлов пользователя

class SharedFilesView(APIView):
    permission_classes = [IsAuthenticated]  # Указывает, что доступ имеет только аутентифицированный пользователь

    def get(self, request):
        # Получаем файлы, которыми пользователь делится, исключая его собственные файлы
        files = Files.objects.filter(shared_with=request.user).exclude(user=request.user)  # Ищем файлы, с которыми пользователь делится, исключая файлы владельца
        serializer = FileSerializer(files, many=True, context={'request': request})  # Сериализуем данные о файлах
        return Response(serializer.data, status=status.HTTP_200_OK)  # Возвращаем данные файлов, которыми делится пользователь
