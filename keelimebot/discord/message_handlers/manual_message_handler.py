import logging

from discord import Message

logger = logging.getLogger(__name__)


async def manual_message_handler(message: Message) -> bool:
    if not message.author.bot:
        response = input(f"{message.author.name}: {message.content}\n> ")
        if response:
            await message.channel.send(response)
            return True

    return False
