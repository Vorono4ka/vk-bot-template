import json

from vk_api import *
from vk_api.keyboard import *
from vk_api.longpoll import VkEventType, VkLongPoll

commands = []


def command(command_name, **kwargs):
    aliases = kwargs['aliases'] if 'aliases' in kwargs else []
    access_level = kwargs['access_level'] if 'access_level' in kwargs else 0

    def wrapper(function):
        commands.append((function, command_name, aliases, access_level))

    return wrapper


def _(*args):
    print('[VK Bot] ', end='')
    for arg in args:
        print(arg, end=' ')
    print()


class VkBot:
    def __init__(self, token: str, group_id: int = None):
        vk_session = vk_api.VkApi(token=token)

        self.longpoll = VkLongPoll(vk_session, group_id=group_id)
        self.vk = vk_session.get_api()

    def listen(self):
        for event in self.longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW:
                message_id = event.message_id
                peer_id = event.peer_id
                message = self.vk.messages.getById(message_ids=message_id, peer_id=peer_id)['items'][0]

                from_id = message['from_id']
                text = message['text']

                if 'payload' in message:
                    payload = json.loads(message['payload'])

                payload = None
                cmd = None

                for prefix in ['!!', '/', '.']:
                    if text.startswith(prefix):
                        msg_without_prefix = text[len(prefix):]
                        if len(msg_without_prefix) > 0:
                            cmd = msg_without_prefix.split()[0].lower()
                            payload = msg_without_prefix[len(cmd) + 1:] or None
                        break

                if cmd is not None:
                    access_level = 0

                    if from_id == 356219576:
                        access_level = 4

                    try:
                        for executor, name, aliases, required in commands:
                            if access_level < required:
                                self.vk.messages.send(
                                    peer_id=peer_id,
                                    message='Ваш уровень доступа меньше нужного.',
                                    random_id=0
                                )
                                continue
                            elif not (cmd in aliases or cmd == name):
                                continue
                            executor(self, message, payload, access_level)
                            _('Command:', cmd, 'Command Payload:', payload)
                    except Exception as e:
                        if from_id == 356219576:
                            self.vk.messages.send(
                                peer_id=356219576,
                                message=e,
                                random_id=0
                            )

    @command('help', aliases=['помощь'])
    def help(self, message: dict, payload, access_level):
        text = ''
        for _, name, aliases, command_access_level in commands:
            if access_level < command_access_level:
                continue
            
            text += f'{name.upper()}'
            if aliases:
                text += f': {", ".join(aliases)}'
            text += '\n'

        self.vk.messages.send(peer_id=message['peer_id'], message=text, random_id=0)


if __name__ == '__main__':
    bot = VkBot('TOKEN')
    bot.listen()
