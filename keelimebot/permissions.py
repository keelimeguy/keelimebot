import logging

from twitchio.ext import commands
from twitchio import Context, Message
from typing import *
from enum import Enum
from abc import ABC, abstractmethod

from .globalnames import BOTNAME

logger = logging.getLogger(__name__)

# Permissions listed in increasing order
Permissions = Enum('Permissions', 'NONE SUBSCRIBER MODERATOR BOT STREAMER')


class PermissionsError(Exception):
    pass


class PermissionsCommand(commands.Command, ABC):
    def __init__(self, name: str, func, **attrs):
        super().__init__(name, func, **attrs)

        self._checks.append(self.command_permissions_check)
        self._func = func

    def serialize(self):
        return {
            'cls': self.__class__,
            'name': self.name,
            'aliases': self.aliases,
            'func': self._func,
            'no_global_checks': self.no_global_checks,
        }

    def command_permissions_check(self, ctx: Context) -> bool:
        """A command check that verifies that the appropriate permissions are met
        """
        return check_permissions(ctx.message, self.required_permissions, self.name)

    @property
    @abstractmethod
    def required_permissions(self):
        """Returns the required permissions for the command
        """
        pass


class StreamerCommand(PermissionsCommand):
    @property
    def required_permissions(self):
        return Permissions.STREAMER


class ModCommand(PermissionsCommand):
    @property
    def required_permissions(self):
        return Permissions.MODERATOR


class SubscriberCommand(PermissionsCommand):
    @property
    def required_permissions(self):
        return Permissions.SUBSCRIBER


class DefaultCommand(PermissionsCommand):
    @property
    def required_permissions(self):
        return Permissions.NONE


def get_author_permissions(message: Message) -> Permissions:
    """Returns the permissions of the given message's author
    """

    if message.tags and message.tags['room-id'] == message.author.id:
        return Permissions.STREAMER

    elif message.author.name.lower() == BOTNAME:
        return Permissions.BOT

    elif message.author.is_mod:
        return Permissions.MODERATOR

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
