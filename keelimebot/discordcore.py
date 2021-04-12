import threading

class DiscordCore(threading.Thread):
    __instance__ = None

    @classmethod
    def get_instance(cls):
        return cls.__instance__

    def __init__(self, irc_token: str, client_id: str, channel_data_dir: str = '.'):
        if DiscordCore.__instance__ is None:
            DiscordCore.__instance__ = self
        else:
            raise RuntimeError("You cannot create another instance of DiscordCore")

        threading.Thread.__init__(self)

    def start(self):
        threading.Thread.start(self)
