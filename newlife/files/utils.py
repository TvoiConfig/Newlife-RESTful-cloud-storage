from database.models import Files
from rest_framework.response import Response
from rest_framework import status


def get_file_or_404(file_id):
    """
    Проверяет существование файла и возвращает его.
    Если файл не существует, возвращает Response с ошибкой 404.
    """
    try:
        return Files.objects.get(file_id=file_id)
    except Files.DoesNotExist:
        return Response({
            "success": False,
            "message": "File does not exist",
        }, status=status.HTTP_404_NOT_FOUND)

def check_file_permission(file, user):
    """
    Проверяет, принадлежит ли файл текущему пользователю.
    Если нет, возвращает Response с ошибкой 403.
    """
    if file.user != user:
        return Response({
            "success": False,
            "message": "You do not have permission to access this file",
        }, status=status.HTTP_403_FORBIDDEN)
    return None