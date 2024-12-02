from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model, authenticate


def password_validator(password):
    # Валидация пароля:
    # Проверяет, что длина пароля не менее 3 символов
    if len(password) < 3:
        raise ValidationError('Password must be at least 3 characters long')

    # Проверяет, что пароль содержит хотя бы одну строчную букву
    if not any(char.islower() for char in password):
        raise ValidationError('Password must contain at least one lowercase letter')

    # Проверяет, что пароль содержит хотя бы одну заглавную букву
    if not any(char.isupper() for char in password):
        raise ValidationError('Password must contain at least one uppercase letter')

    # Проверяет, что пароль содержит хотя бы одну цифру
    if not any(char.isdigit() for char in password):
        raise ValidationError('Password must contain at least one digit')

    return password


def email_validator(email):
    # Проверка, что email уже не зарегистрирован
    if get_user_model().objects.filter(email=email).exists():
        raise ValidationError('Email already registered')  # Указывает, что email уже существует в базе данных
    return email


class RegistrationSerializer(serializers.Serializer):
    # Сериализатор для регистрации нового пользователя
    email = serializers.EmailField(
        required=True,
        validators=[email_validator]  # Валидация email через функцию email_validator
    )
    password = serializers.CharField(
        required=True,
        write_only=True,  # Указывает, что поле будет доступно только для записи
        validators=[password_validator]  # Валидация пароля через функцию password_validator
    )
    first_name = serializers.CharField(required=True)  # Поле для имени пользователя
    last_name = serializers.CharField(required=True)  # Поле для фамилии пользователя

    def create(self, validated_data):
        # Создание пользователя и генерация токена
        try:
            user = get_user_model().objects.create_user(
                email=validated_data['email'],
                password=validated_data['password'],
                first_name=validated_data['first_name'],
                last_name=validated_data['last_name']
            )

            # Создаём токен для пользователя
            token = Token.objects.create(user=user)
            return {
                'user': user,
                'token': token.key  # Возвращаем данные пользователя и токен
            }
        except ValidationError as e:
            # В случае ошибки валидации, передаем ошибку через сериализатор
            raise serializers.ValidationError({'message': str(e)})


class AuthorizationSerializer(serializers.Serializer):
    # Сериализатор для аутентификации пользователя
    email = serializers.EmailField()  # Поле для email
    password = serializers.CharField(write_only=True)  # Поле для пароля, доступное только для записи

    def validate(self, data):
        # Валидация аутентификации пользователя
        email = data.get("email")
        password = data.get("password")

        # Попытка аутентификации пользователя по email и паролю
        user = authenticate(email=email, password=password)

        if not user:
            # Если пользователь не найден, выбрасываем ошибку
            raise serializers.ValidationError("Login failed") # Указывает, что email или пароль неверные

        data["user"] = user  # Добавляем найденного пользователя в данные
        return data  # Возвращаем данные с пользователем
