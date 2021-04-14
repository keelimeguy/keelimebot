import unittest

from keelimebot.twitch.permissions import Permissions


class PermissionsTestCase(unittest.TestCase):
    def test_permission_ordering(self):
        permissions_in_decreasing_order = [
            Permissions.STREAMER,
            Permissions.BOT,
            Permissions.MODERATOR,
            Permissions.VIP,
            Permissions.SUBSCRIBER,
            Permissions.NONE,
        ]
        for i, high_permission in enumerate(permissions_in_decreasing_order):
            for low_permission in permissions_in_decreasing_order[i+1:]:
                self.assertTrue(high_permission.value > low_permission.value)


if __name__ == '__main__':
    unittest.main()
