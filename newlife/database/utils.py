def user_directory_path(instance, filename):
    # Возвращает путь для сохранения файла в зависимости от пользователя
    # instance - экземпляр модели Files
    # filename - имя загружаемого файла
    return f"user_{instance.user.id}/{filename}"  # Формирует путь вида "user_<id пользователя>/<имя файла>"
