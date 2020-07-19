from keelimebot.permissions import Permissions
from .permissions_command import PermissionsCommand


class DefaultCommand(PermissionsCommand):
    @property
    def required_permissions(self):
        return Permissions.NONE


class StreamerCommand(DefaultCommand):
    @property
    def required_permissions(self):
        return Permissions.STREAMER


class ModCommand(DefaultCommand):
    @property
    def required_permissions(self):
        return Permissions.MODERATOR


class SubscriberCommand(DefaultCommand):
    @property
    def required_permissions(self):
        return Permissions.SUBSCRIBER


class VipCommand(DefaultCommand):
    @property
    def required_permissions(self):
        return Permissions.VIP
