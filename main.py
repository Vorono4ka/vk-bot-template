import time

from vk_api.longpoll import VkEventType, VkLongPoll
from vk_api.vk_api import VkApiMethod
import vk_api


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
        vk_session = vk_api.VkApi(token=token)

        self.users = {
            356219576: {
                'access_level': 3,
                'kicked': False,
                'kick_reason': None,
                'banned': False,
                'ban_reason': None,

                'warns_count': -1337228
            },
            498578289: {
                'access_level': 1,
                'kicked': False,
                'kick_reason': None,
                'banned': False,
                'ban_reason': None,

                'warns_count': -1
            },
        }

        self.longpoll = VkLongPoll(vk_session)
        self.vk = VkApiMethod(vk_session)

    def listen(self):
        for event in self.longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW:
                msg_id = event.message_id
                p_id = event.peer_id
                msg = self.vk.messages.getById(message_ids=msg_id,
                                               peer_id=p_id)['items'][0]

                text = msg['text']
                f_id = msg['from_id']

                if f_id not in self.users:
                    self.users[f_id] = {
                        'access_level': 0,
                        'kicked': False,
                        'kick_reason': None,
                        'banned': False,
                        'ban_reason': None,

                        'warns_count': 0
                    }

                access_level = self.users[f_id]['access_level']

                cmd_payload = None
                cmd = None

                if 'action' in msg:
                    action = msg['action']

                    _(action)

                    action_type = action['type']
                    if action_type == 'chat_kick_user':
                        member_id = action['member_id']

                        try:
                            if p_id > 2000000000:
                                self.vk.messages.removeChatUser(chat_id=p_id - 2000000000,
                                                                user_id=member_id)
                        except Exception as e:
                            _(e)

                        self.users[member_id]['kicked'] = True
                    elif action_type == 'chat_invite_user':
                        member_id = action['member_id']

                        if self.users[member_id]['banned']:
                            try:
                                if p_id > 2000000000:
                                    self.vk.messages.removeChatUser(chat_id=p_id - 2000000000,
                                                                    user_id=member_id)
                            except Exception as e:
                                _(e)

                        self.users[member_id]['kicked'] = False
                        self.users[member_id]['kick_reason'] = None
                    continue

                for prefix in ['!!', '/', '.']:
                    if text.startswith(prefix):
                        msg_without_prefix = text[len(prefix):]
                        cmd = msg_without_prefix.split()[0]
                        cmd_payload = msg_without_prefix[len(cmd) + 1:]
                        if len(cmd_payload) >= 1:
                            pass
                        else:
                            cmd_payload = None
                        break

                if cmd is not None:
                    if access_level >= 0:
                        if cmd in ['id', 'vk_id', 'айди']:
                            if cmd_payload is not None:
                                vk_id = self.vk.users.get(user_ids=cmd_payload.split()[0])['items'][0]['id']
                            elif 'reply_message' in msg:
                                vk_id = msg['reply_message']['from_id']
                            else:
                                vk_id = f_id

                            self.vk.messages.send(peer_id=p_id,
                                                  message=f'VK ID:\n {vk_id}',
                                                  random_id=0)
                        if access_level >= 1:
                            if cmd in ['kick', 'кик']:
                                # if cmd_payload is not None:
                                #     vk_id = self.vk.users.get(user_ids=cmd_payload.split()[0])['items'][0]['id']
                                if 'reply_message' in msg:
                                    vk_id = msg['reply_message']['from_id']
                                else:
                                    self.vk.messages.send(peer_id=p_id,
                                                          message='А кого кикать-то?',
                                                          random_id=0)
                                    continue

                                if p_id > 2000000000:
                                    removed = self.vk.messages.removeChatUser(chat_id=p_id - 2000000000,
                                                                              user_id=vk_id)

                                    if removed:
                                        self.vk.messages.send(peer_id=p_id,
                                                              message=f'@id{vk_id} (Пользователь) успешно кикнут!',
                                                              random_id=0)

                                        self.users[vk_id]['kick_reason'] = cmd_payload
                                    else:
                                        self.vk.messages.send(peer_id=p_id,
                                                              message='Что-то пошло не так...',
                                                              random_id=0)
                                else:
                                    self.vk.messages.send(peer_id=p_id,
                                                          message='Дурень, мы не в беседе!',
                                                          random_id=0,
                                                          reply_to=msg_id)
                            elif cmd in ['kickinfo', 'кикинфо']:
                                # if cmd_payload is not None:
                                #     vk_id = self.vk.users.get(user_ids=cmd_payload.split()[0])['items'][0]['id']
                                if 'reply_message' in msg:
                                    vk_id = msg['reply_message']['from_id']
                                else:
                                    vk_id = f_id

                                kick_info = f'Кикнут: {self.users[vk_id]["kicked"]}\n'

                                if self.users[vk_id]['kicked']:
                                    kick_info += f'Причина кика: {self.users[vk_id]["kick_reason"]}'

                                self.vk.messages.send(peer_id=p_id,
                                                      message=kick_info,
                                                      random_id=0)
                            if access_level >= 2:
                                if cmd in ['ban', 'бан']:
                                    # if cmd_payload is not None:
                                    #     vk_id = self.vk.users.get(user_ids=cmd_payload.split()[0])['items'][0]['id']
                                    if 'reply_message' in msg:
                                        vk_id = msg['reply_message']['from_id']
                                    else:
                                        self.vk.messages.send(peer_id=p_id,
                                                              message='А кого банить-то?',
                                                              random_id=0)
                                        continue

                                    if p_id > 2000000000:
                                        removed = self.vk.messages.removeChatUser(chat_id=p_id - 2000000000,
                                                                                  user_id=vk_id)

                                        if removed:
                                            self.vk.messages.send(peer_id=p_id,
                                                                  message=f'@id{vk_id} (Пользователь) успешно забанен!',
                                                                  random_id=0)

                                            self.users[vk_id]['kick_reason'] = 'ban'

                                            self.users[vk_id]['banned'] = True
                                            self.users[vk_id]['ban_reason'] = cmd_payload
                                        else:
                                            self.vk.messages.send(peer_id=p_id,
                                                                  message='Что-то пошло не так...',
                                                                  random_id=0)
                                    else:
                                        self.vk.messages.send(peer_id=p_id,
                                                              message='Дурень, мы не в беседе!',
                                                              random_id=0,
                                                              reply_to=msg_id)
                                elif cmd in ['baninfo', 'банинфо']:
                                    # if cmd_payload is not None:
                                    #     vk_id = self.vk.users.get(user_ids=cmd_payload.split()[0])['items'][0]['id']
                                    if 'reply_message' in msg:
                                        vk_id = msg['reply_message']['from_id']
                                    else:
                                        vk_id = f_id

                                    ban_info = f'Забанен: {self.users[vk_id]["banned"]}\n'

                                    if self.users[vk_id]['banned']:
                                        ban_info += f'Причина бана: {self.users[vk_id]["ban_reason"]}'

                                    self.vk.messages.send(peer_id=p_id,
                                                          message=ban_info,
                                                          random_id=0)
                                elif cmd in ['unwarn']:
                                    # if cmd_payload is not None:
                                    #     vk_id = self.vk.users.get(user_ids=cmd_payload.split()[0])['items'][0]['id']
                                    if 'reply_message' in msg:
                                        vk_id = msg['reply_message']['from_id']
                                    else:
                                        vk_id = f_id

                                    self.users[vk_id]['warns_count'] = 0

                                    self.vk.messages.edit(peer_id=p_id,
                                                          message_id=msg_id,
                                                          message='Варны сняты!')
                                elif cmd in ['fix', 'почини']:
                                    if 'reply_message' in msg:
                                        text = msg['reply_message']['text']
                                    else:
                                        text = cmd_payload
                                    fixed_text = ''

                                    for letter in text:
                                        isupper = letter.isupper()
                                        if letter in english_keyboard:
                                            letter_index = english_keyboard.index(letter.lower())
                                            fixed_letter = russian_keyboard[letter_index]
                                        elif letter in russian_keyboard:
                                            letter_index = russian_keyboard.index(letter.lower())
                                            fixed_letter = english_keyboard[letter_index]
                                        else:
                                            fixed_letter = letter

                                        fixed_text += fixed_letter.upper() if isupper else fixed_letter

                                    self.vk.messages.edit(peer_id=p_id,
                                                          message_id=msg_id,
                                                          message=fixed_text)
                                elif cmd in ['f', 'ф']:
                                    f_map = [
                                        ['🌕', '🌗', '🌑', '🌑', '🌑', '🌑', '🌑', '🌓', '🌕'],
                                        ['🌕', '🌗', '🌑', '🌑', '🌑', '🌑', '🌑', '🌕', '🌕'],
                                        ['🌕', '🌗', '🌑', '🌓', '🌕', '🌕', '🌕', '🌕', '🌕'],
                                        ['🌕', '🌗', '🌑', '🌓', '🌕', '🌕', '🌕', '🌕', '🌕'],
                                        ['🌕', '🌗', '🌑', '🌑', '🌑', '🌑', '🌓', '🌕', '🌕'],
                                        ['🌕', '🌗', '🌑', '🌑', '🌑', '🌑', '🌕', '🌕', '🌕'],
                                        ['🌕', '🌗', '🌑', '🌓', '🌕', '🌕', '🌕', '🌕', '🌕'],
                                        ['🌕', '🌗', '🌑', '🌓', '🌕', '🌕', '🌕', '🌕', '🌕'],
                                        ['🌕', '🌗', '🌑', '🌓', '🌕', '🌕', '🌕', '🌕', '🌕']
                                    ]

                                    for x in range(10):
                                        # map_to_text
                                        text = '\n'.join([''.join(line) for line in f_map])

                                        self.vk.messages.edit(peer_id=p_id,
                                                              message_id=msg_id,
                                                              message=text)

                                        [chars_list.append(chars_list.pop(0)) for chars_list in f_map]

                                        time.sleep(0.5)
                                elif cmd in ['exec', 'выполни']:
                                    try:
                                        exec(cmd_payload)

                                        self.vk.messages.edit(peer_id=p_id,
                                                              message_id=msg_id,
                                                              message='Выполнено!')
                                    except Exception as e:
                                        self.vk.messages.edit(peer_id=p_id,
                                                              message_id=msg_id,
                                                              message=str(e))
                                elif cmd in ['echo', 'eval']:
                                    try:
                                        evaluated_cmd = eval(cmd_payload)
                                        print(evaluated_cmd)

                                        self.vk.messages.edit(peer_id=p_id,
                                                              message_id=msg_id,
                                                              message=evaluated_cmd)
                                    except Exception as e:
                                        self.vk.messages.edit(peer_id=p_id,
                                                              message_id=msg_id,
                                                              message=str(e))
                                if access_level >= 3:
                                    pass
                    _('Command:', cmd, 'Command Payload:\n', cmd_payload)


if __name__ == '__main__':
    bot = VkBot('172da3a0dae9f99545bb712af4bf34faedbcb4f13dadfa10fb1327106d82aecd5c7e5499e71d6c4fa5a70')
    bot.listen()
