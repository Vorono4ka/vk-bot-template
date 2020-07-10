from vk_api.vk_api import VkApiMethod


class Hello(VkApiMethod):
    def __init__(self, vk: VkApiMethod):
        super().__init__(vk)

        self.access_level = 0
        self.status_code = 1

    def process(self, cmd_payload: str, message: dict):
        try:
            self._vk.messages.send(peer_id=int(message['peer_id']),
                                   message='HI!',
                                   random_id=0)

            exec('ban')

            return True
        except Exception as e:
            print(e)
            self.status_code = 2
            return False
