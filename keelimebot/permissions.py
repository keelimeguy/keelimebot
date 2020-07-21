import logging

from twitchio import Message
from enum import Enum

from .globalnames import BOTNAME

logger = logging.getLogger(__name__)

# Permissions listed in increasing order
Permissions = Enum('Permissions', 'NONE SUBSCRIBER VIP MODERATOR BOT STREAMER')


class PermissionsError(Exception):
    pass


def get_author_permissions(message: Message) -> Permissions:
    """Returns the permissions of the given message's author
    """

    if message.tags and message.tags['room-id'] == message.author.id:
        return Permissions.STREAMER

    elif message.author.name.lower() == BOTNAME:
        return Permissions.BOT

    elif message.author.is_mod:
        return Permissions.MODERATOR

    elif message.tags and 'vip/1' in message.tags['badges'].split(','):
        return Permissions.VIP

    elif message.author.is_subscriber:
        return Permissions.SUBSCRIBER

    return Permissions.NONE


def check_permissions(message: Message, required_permissions: Permissions, command_name: str) -> bool:
    """Determine if a user has the given required permissions

    :raises: PermissionsError
    """

    author_permissions = get_author_permissions(message)
    if author_permissions.value < required_permissions.value:
        error_msg = f"{message.author} does not have required permissions to use !{command_name}"
        raise PermissionsError(error_msg)

    return True
