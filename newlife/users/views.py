from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from users.serializers import RegistrationSerializer, AuthorizationSerializer
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.authtoken.models import Token

class RegistrationView(APIView):
    permission_classes = [permissions.AllowAny]  # Указывает, что доступ к данному представлению разрешён любому пользователю

    def post(self, request, *args, **kwargs):
        # Создание и валидация сериализатора для регистрации пользователя
        serializer = RegistrationSerializer(data=request.data)

        if serializer.is_valid():
            # Если данные валидны, сохраняем пользователя и получаем данные
            user_data = serializer.save()

            return Response({
                'success': True,  # Указывает, что операция прошла успешно
                'message': 'Success',  # Сообщение о успешной регистрации
                'token': user_data['token']  # Токен пользователя, возвращаемый при успешной регистрации
            }, status=status.HTTP_200_OK)

        return Response({
            'success': False,  # Указывает, что операция не удалась
            'message': serializer.errors  # Возвращаем ошибки валидации
        }, status=status.HTTP_422_UNPROCESSABLE_ENTITY)  # Указывает, что данные не прошли валидацию

class AuthorizationView(APIView):
    permission_classes = [permissions.AllowAny]  # Указывает, что доступ к данному представлению разрешён любому пользователю

    def post(self, request, *args, **kwargs):
        # Создание и валидация сериализатора для авторизации пользователя
        serializer = AuthorizationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]  # Получаем пользователя из сериализатора

            # Создаём новый токен или получаем существующий для пользователя
            token, create = Token.objects.get_or_create(user=user)

            return Response({
                "success": True,  # Указывает, что операция прошла успешно
                "message": "Success",  # Сообщение об успешной авторизации
                "token": token.key  # Возвращаем токен пользователя
            }, status=status.HTTP_200_OK)
        error_message = serializer.errors.get("non_field_errors", ["Invalid data"])[0]
        return Response({
            "success": False,  # Указывает, что операция не удалась
            "message": error_message  # Возвращаем ошибки валидации
        }, status=status.HTTP_400_BAD_REQUEST)  # Указывает, что запрос содержит ошибки

class LogoutView(APIView):
    authentication_classes = [TokenAuthentication]  # Указывает, что для доступа требуется токен аутентификации
    permission_classes = [permissions.IsAuthenticated]  # Указывает, что доступ к этому представлению только для аутентифицированных пользователей

    def get(self, request, *args, **kwargs):
        # Проверяем, есть ли у запроса токен аутентификации
        if not request.auth:
            return Response({
                "message": "Login failed"  # Указывает, что пользователь не аутентифицирован
            }, status=status.HTTP_403_FORBIDDEN)  # Указывает, что доступ запрещён

        # Удаляем токен из базы данных, тем самым завершая сессию пользователя
        request.auth.delete()
        return Response({
            "success": True,  # Указывает, что операция прошла успешно
            "message": "Logout",  # Сообщение о том, что пользователь вышел из системы
        }, status=status.HTTP_200_OK)
