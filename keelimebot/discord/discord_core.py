import inspect
import logging
import os

from discord.ext import commands as basecommands
from discord.ext.commands import Context
from discord import Message, Member

from keelimebot.serializer import json_deserialize_from_file, json_serialize_to_string
from .commands import commands

logger = logging.getLogger(__name__)


class DiscordCore(basecommands.Bot):
    __instance__ = None

    @classmethod
    def get_instance(cls):
        return cls.__instance__

    def __init__(self, prefix='!', channel_data_dir: str = '.'):
        if DiscordCore.__instance__ is None:
            DiscordCore.__instance__ = self
        else:
            raise RuntimeError("You cannot create another instance of DiscordCore")

        self._channel_data_dir = channel_data_dir
        self._lock_json = True
        self._commandlist = {}
        self._excluded_commands = []

        super().__init__(
            command_prefix=prefix,
            owner_id=os.getenv('DISCORD_OWNER_ID'),
            help_command=None
        )
        self.add_custom_commands()

        self._excluded_commands = list(self.all_commands.keys())
        self._commandlist = {}
        self._lock_json = False

        self.add_commands_from_json_file(f"{self._channel_data_dir}/discord_commands.json")
        self.dump_commands_to_json_file()
        self.add_commands_from_json_file(f"{self._channel_data_dir}/discord_commands.json")

    def run_bot(self):
        basecommands.Bot.run(self, os.getenv('DISCORD_TOKEN'))

    def add_commands_from_json_file(self, filename: str):
        self._lock_json = True

        try:
            with open(filename, 'r') as f:
                command_dict = json_deserialize_from_file(f)

                for name, args in command_dict.items():
                    if isinstance(args['func'], basecommands.Command):
                        command = args['cls'](name=args['name'], func=args['func']._func, text=args['text'],
                                              aliases=args['aliases'])
                    else:
                        command = args['cls'](name=args['name'], func=args['func'], text=args['text'],
                                              aliases=args['aliases'])

                    if command.name in self.all_commands:
                        for name in [command.name] + command.aliases:
                            self.all_commands[name] = command

                    else:
                        self.add_command(command)

        except FileNotFoundError:
            pass

        self._lock_json = False

    def dump_commands_to_json_file(self):
        if self._lock_json:
            return

        with open(f"{self._channel_data_dir}/discord_commands.json", 'w') as f:
            f.write(json_serialize_to_string(self.all_commands))

    def add_command(self, command: commands.DefaultCommand):
        super().add_command(command)

        if command.name not in self._excluded_commands:
            self._commandlist[command.name] = f"{command.name}"

        self.dump_commands_to_json_file()

    def remove_command(self, command: commands.DefaultCommand):
        super().remove_command(command)

        if command.name in self._commandlist:
            del self._commandlist[command.name]

        self.dump_commands_to_json_file()

    def command(self, *, name: str = None, cls=commands.DefaultCommand, func=None, **attrs):
        """Decorator which registers a command on the bot.

        Commands must be a coroutine.
        """

        if not inspect.isclass(cls):
            raise TypeError(f'cls must be of type <class> not <{type(cls)}>')

        cmd_name = name or func.__name__

        command = cls(name=cmd_name, func=func, **attrs)
        self.add_command(command)

    async def on_ready(self):
        """Called once when the bot goes online.
        """

        logger.info(f'Ready | {os.getenv("BOTNAME")}')

        for guild in self.guilds:
            logger.info(f'{self.user} is connected to: {guild.name}(id: {guild.id})')

            members = '\n - '.join([member.name for member in guild.members])
            logger.info(f'Guild Members:\n - {members}')

    async def on_member_join(self, member: Member):
        """Called when new member joins
        """

        pass

    async def on_message(self, message: Message):
        """Called when a new message is posted
        """

        # Firstly, ignore any of our own messages
        if message.author == self.user:
            return

        ordered_message_handlers = [
            # TODO: e.g. moderation handling
        ]

        message_handled = False
        for handler in ordered_message_handlers:
            message_handled = handler(message)
            if message_handled:
                break

        if not message_handled:
            await self.process_commands(message)

    async def on_error(self, event_method: str, *args, **kwargs):
        """Called once when an error occurs
        """
        logger.info(f'Ignoring exception in {event_method}')
        logger.debug('', exc_info=True)

    async def on_command_error(self, context: Context, exception: Exception):
        """Called once when an error occurs during command handling
        """
        if self.extra_events.get('on_command_error', None):
            return

        command = context.command
        if command and command.has_error_handler():
            return

        cog = context.cog
        if cog and cog.has_error_handler():
            return

        logger.info(f'Ignoring exception in command {context.command}:')
        logger.debug('', exc_info=True)

    def add_custom_commands(self):
        self.command(name='bottest', aliases=['test', 'ping'], func=DiscordCore.cmd_bottest)

    ########################
    # Commands
    ########################

    async def cmd_bottest(ctx: Context):
        """Check that the bot is connected
        """

        await ctx.send('I am surviving and thriving <:taigaSalute:813611124988575794>')
