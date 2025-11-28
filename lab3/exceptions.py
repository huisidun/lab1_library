# некорректные данные при регистрации
class InvalidUserDataError(Exception):
    pass


# неверный пароль или телефон при авторизации
class InvalidCredentialsError(Exception):
    pass