from vk_api.longpoll import VkEventType, VkLongPoll
import vk_api

from commands.factory import CommandsFactory
from commands.receive.Hello import Hello
from utils.errors import Errors


def _(*args):
    print('[VK Bot] ', end='')
    for arg in args:
        print(arg, end=' ')
    print()


def calculate_file_size(size_in_bytes):
    suffix = 'Bytes'
    size = size_in_bytes
    if size_in_bytes > 1024:
        suffix = 'Kb'
        size /= 1024
        if size_in_bytes > 1024 * 1024:
            suffix = 'Mb'
            size /= 1024

    return f'{int(round(size, 0))}{suffix}'


class VkBot:
    def __init__(self, token: str):
        self.commands_factory = CommandsFactory()
        self.errors = Errors()

        vk_session = vk_api.VkApi(token=token)

        self.longpoll = VkLongPoll(vk_session)
        self.vk = vk_session.get_api()

    def listen(self):
        for event in self.longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW:
                msg_id = event.message_id
                p_id = event.peer_id
                msg = self.vk.messages.getById(message_ids=msg_id,
                                               peer_id=p_id)['items'][0]

                text = msg['text']
                f_id = msg['from_id']

                cmd_payload = None
                cmd = None

                for prefix in ['!!', '/', '.']:
                    if text.startswith(prefix):
                        msg_without_prefix = text[len(prefix):]
                        if len(msg_without_prefix) > 0:
                            cmd = msg_without_prefix.split()[0]
                            cmd_payload = msg_without_prefix[len(cmd) + 1:]
                            if len(cmd_payload) == 0:
                                cmd_payload = None
                        break

                if cmd is not None:
                    executed, error_code = self.commands_factory.handle_command(self.vk, cmd, cmd_payload, 0, msg)
                    if not executed:
                        if p_id == 564750551:
                            self.vk.messages.send(
                                peer_id=p_id,
                                message=self.errors.localize_error(error_code, 'ru-RU'),
                                random_id=0
                            )
                    _('Command:', cmd, 'Command Payload:', cmd_payload)


if __name__ == '__main__':
    bot = VkBot('172da3a0dae9f99545bb712af4bf34faedbcb4f13dadfa10fb1327106d82aecd5c7e5499e71d6c4fa5a70')

    bot.commands_factory.add_command(['hello', 'test', 'привет', 'тест'], Hello)

    bot.listen()
