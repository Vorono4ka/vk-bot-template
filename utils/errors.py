class Errors:
    def __init__(self):
        self.languages = {
            'ru-RU': [
                'Такой команды не существует!',
                'Успешно выполнено!',
                'Произошла ошибка!',
                'Уровень доступа слишком маленький',
                'Команда запрещена!'
            ]
        }

    def localize_error(self, error_code: int, language: str):
        if language in self.languages:
            strings = self.languages[language]
            return strings[error_code]
        raise IndexError('I do not have such a language!')

# Status codes:
# 0 - Такой команды не существует!
# 1 - Успешно выполнено!
# 2 - Произошла ошибка!
# 3 - Уровень доступа слишком маленький
# 4 - Команда запрещена!
