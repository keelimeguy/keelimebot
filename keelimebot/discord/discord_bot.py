import logging

from discord_slash import SlashCommand, SlashContext
from discord.ext.commands import Context
from discord import Embed

from keelimebot.discord.discord_core import DiscordCore
from keelimebot.discord.message_handlers.manual_message_handler import manual_message_handler

logger = logging.getLogger(__name__)


def get_discord_bot(args) -> DiscordCore:
    core = DiscordCore(prefix=args.prefix, channel_data_dir=args.channel_data_dir)
    core.add_message_handler(manual_message_handler)
    return core


def add_custom_commands(core: DiscordCore):
    core.command(name='bottest', aliases=['test', 'ping'], func=DiscordCore.cmd_bottest)


def add_slash_commands(slash: SlashCommand):
    core = DiscordCore.get_instance()
    slash.add_slash_command(DiscordCore.slash_kanna, name="kanna", description="Prints Kanna art",
                            guild_ids=[guild.id for guild in core.guilds])


async def cmd_bottest(ctx: Context):
    """Check that the bot is connected
    """

    core = DiscordCore.get_instance()
    await ctx.send(f"I am surviving and thriving {str(core.emojis['taigaSalute'])}")


async def slash_kanna(ctx: SlashContext):
    """Print Kanna art
    """

    core = DiscordCore.get_instance()
    s = str(core.emojis['kannaSip'])
    a = str(core.emojis['kanna1'])
    b = str(core.emojis['kanna2'])
    c = str(core.emojis['kanna3'])
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
