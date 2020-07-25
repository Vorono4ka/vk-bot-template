from vk_api.vk_api import VkApiMethod


class CommandsFactory:
    def __init__(self):
        self.commands_variations = [

        ]

        self.commands_classes = {

        }

    def handle_command(self, vk: VkApiMethod, cmd: str, cmd_payload: str, access_level: int, message):
        command_index = None
        for command in self.commands_variations:
            for variation in command:
                if variation == cmd.lower():
                    command_index = self.commands_variations.index(command)
                    break

        if command_index is not None:
            command = self.commands_classes[command_index](vk)
            if command.access_level <= access_level:
                return command.process(cmd_payload, message), command.status_code
            else:
                return False, 3
        else:
            return False, 0

    def add_command(self, variations: list, command_class):
        self.commands_variations.append(variations)

        command_index = self.commands_variations.index(variations)
        self.commands_classes[command_index] = command_class

# Status codes:
# 0 - Такой команды не существует!
# 1 - Успешно выполнено!
# 2 - Произошла ошибка!
# 3 - Уровень доступа слишком маленький
# 4 - Команда запрещена!
