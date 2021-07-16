import logging

from discord_slash import SlashContext
from discord.ext.commands import Context
from discord import Embed

from keelimebot.discord.discord_core import DiscordCore
from keelimebot.discord.message_handlers.manual_message_handler import manual_message_handler

logger = logging.getLogger(__name__)


class DiscordBot:
    core = None

    @classmethod
    def add_custom_commands(cls):
        cls.core.command(name='bottest', aliases=['test', 'ping'], func=DiscordBot.cmd_bottest)
        cls.core.initialize_custom_commands()

    @classmethod
    def add_slash_commands(cls):
        cls.core.slash.add_slash_command(DiscordBot.slash_kanna, name="kanna", description="Prints Kanna art",
                                         guild_ids=[guild.id for guild in cls.core.guilds])

    @classmethod
    def get_core(cls) -> DiscordCore:
        return cls.core

    @classmethod
    def run(cls):
        cls.core.run_bot()

    def __init__(self, args):
        if DiscordBot.core is None:

            DiscordBot.core = DiscordCore(prefix=args.prefix, channel_data_dir=args.channel_data_dir, no_sync=args.no_sync)
            self.add_custom_commands()
            self.add_slash_commands()

            if args.manual_mode:
                DiscordBot.core.add_message_handler(manual_message_handler)

        else:
            raise RuntimeError("You cannot create another instance of DiscordBot")

    @staticmethod
    async def cmd_bottest(ctx: Context):
        """Check that the bot is connected
        """

        core = DiscordBot.get_core()
        await ctx.send(f"I am surviving and thriving {str(core.emoji_map['taigaSalute'])}")

    @staticmethod
    async def slash_kanna(ctx: SlashContext):
        """Print Kanna art
        """

        core = DiscordBot.get_core()
        s = str(core.emoji_map['kannaSip'])
        a = str(core.emoji_map['kanna1'])
        b = str(core.emoji_map['kanna2'])
        c = str(core.emoji_map['kanna3'])
        msg = f"""­­­ ­   {s}                {s}                 {s}
        {s}­{s}­{s}        {s}­{s}­{s}        {s}­{s}­{s}
    ­{s}­{a}{b}{c}­{s}­­{s}­{a}{b}{c}­{s}­­{s}­{a}{b}{c}­{s}­
        {s}­{s}­{s}        {s}­{s}­{s}        {s}­{s}­{s}
            {s}                {s}                {s}
            {s}                {s}                {s}
        {s}­{s}­{s}        {s}­{s}­{s}        {s}­{s}­{s}
    ­{s}­{a}{b}{c}­{s}­­{s}­{a}{b}{c}­{s}­­{s}­{a}{b}{c}­{s}­
        {s}­{s}­{s}        {s}­{s}­{s}        {s}­{s}­{s}
            {s}                {s}                {s}
            {s}                {s}                {s}
        {s}­{s}­{s}        {s}­{s}­{s}        {s}­{s}­{s}
    ­{s}­{a}{b}{c}­{s}­­{s}­{a}{b}{c}­{s}­­{s}­{a}{b}{c}­{s}­
        {s}­{s}­{s}        {s}­{s}­{s}        {s}­{s}­{s}
            {s}                {s}                {s}"""

        embed = Embed(description=msg, color=0xf4afca)
        await ctx.send(embed=embed)
