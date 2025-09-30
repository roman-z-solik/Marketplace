class ValidationConstants:
    """Класс для хранения констант, используемых в валидации форм"""

    FORBIDDEN_WORDS = (
        "казино",
        "криптовалюта",
        "крипта",
        "биржа",
        "дешево",
        "бесплатно",
        "обман",
        "полиция",
        "радар",
    )
    MIN_PRICE = 0
    MIN_NAME_LENGTH = 3
    MAX_NAME_LENGTH = 100
    ALLOWED_IMAGE_EXTENSIONS = ["jpg", "jpeg", "png"]
    MAX_IMAGE_SIZE = 5 * 1024 * 1024  # 5 МБ в байтах
    MAX_IMAGE_SIZE_MB = 5

    ERROR_MESSAGES = {
        "negative_price": "Цена не может быть отрицательной",
        "none_price": "Цена обязательна для заполнения",
        "name_too_short": f"Название должно быть не короче {MIN_NAME_LENGTH} символов",
        "image_format": "Разрешены только изображения в формате JPEG или PNG",
        "image_size": f"Размер изображения не должен превышать {MAX_IMAGE_SIZE_MB} МБ",
        "image_corrupted": "Файл поврежден или не является изображением",
    }
