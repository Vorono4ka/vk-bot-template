from vk_api.vk_api import VkApiMethod


english_keyboard = [
    'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '[', ']',
    'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ';', '\'',
    'z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '/'
]

russian_keyboard = [
    'й', 'ц', 'у', 'к', 'е', 'н', 'г', 'ш', 'щ', 'з', 'х', 'ъ',
    'ф', 'ы', 'в', 'а', 'п', 'р', 'о', 'л', 'д', 'ж', 'э',
    'я', 'ч', 'с', 'м', 'и', 'т', 'ь', 'б', 'ю', '.'
]


class Fix(VkApiMethod):
    def __init__(self, vk: VkApiMethod):
        super().__init__(vk)

        self.access_level = 0
        self.status_code = 1

    def process(self, cmd_payload: str, message: dict):
        try:
            if 'reply_message' in message:
                text = message['reply_message']['text']
            else:
                text = cmd_payload
            fixed_text = ''

            for letter in text:
                isupper = letter.isupper()
                letter = letter.lower()
                if letter in english_keyboard:
                    letter_index = english_keyboard.index(letter)
                    fixed_letter = russian_keyboard[letter_index]
                elif letter in russian_keyboard:
                    letter_index = russian_keyboard.index(letter)
                    fixed_letter = english_keyboard[letter_index]
                else:
                    fixed_letter = letter

                fixed_text += fixed_letter.upper() if isupper else fixed_letter

            self.vk.messages.edit(peer_id=message['peer_id'],
                                  message_id=message['id'],
                                  message=fixed_text)

            return True
        except Exception as e:
            print(e)
            self.status_code = 2
            return False
