import unittest
import asyncio
import io

from contextlib import redirect_stderr

from keelimebot.keelimebot import Keelimebot
from keelimebot.commands.usage_command import CommandFormattingError


class _Context:
    def __init__(self, content):
        self.content = content

    async def send(self, msg):
        pass


class KeelimebotTestCase(unittest.TestCase):

    def test_cmd_addcommand_failure(self):
        fail_cases = [
            'a b c',
            'a\'b c\'',
            'a"b c"',
            '\'a b\'c',
            '"a b"c',
            '\'a b\' c',
            '"a b" c',
            'a \'b c\'\'',
            'a \'b c\'"',
            'a "b c""',
            'a "b c"\'',
            'a ""b c""',
            'a \'\'b c\'\'',
        ]

        def assertFails(msg):
            ctx = _Context(msg)
            loop = asyncio.get_event_loop()

            f = io.StringIO()
            with redirect_stderr(f):
                self.assertRaises(CommandFormattingError, loop.run_until_complete, Keelimebot.cmd_addcommand._func(ctx))

        for case in fail_cases:
            assertFails(f"!addcommand {case}")

    def test_cmd_addcommand(self):
        success_cases = [
            'a b',
            'a \'b c\'',
            'a "b c"',
            'a "\'b c\'"',
            'a \'"b c"\'',
        ]

        def assertSuccess(msg):
            ctx = _Context(msg)
            loop = asyncio.get_event_loop()
            self.assertEqual(None, loop.run_until_complete(Keelimebot.cmd_addcommand._func(ctx)))

        for case in success_cases:
            assertSuccess(f"!addcommand {case}")

    def run_test_get_args(self, test_cases, required=None, optional=None, check_args=None):
        for msg, ret in test_cases.items():
            ctx = _Context(msg)
            loop = asyncio.get_event_loop()
            self.assertEqual(ret, loop.run_until_complete(Keelimebot.get_args(ctx, required=required, optional=optional, check_args=check_args)).__dict__)

    def run_test_get_args_failure(self, test_cases, required=None, optional=None, check_args=None):
        for msg in test_cases:
            ctx = _Context(msg)
            loop = asyncio.get_event_loop()

            f = io.StringIO()
            with redirect_stderr(f):
                self.assertRaises(CommandFormattingError, loop.run_until_complete, Keelimebot.get_args(ctx, required=required, optional=optional, check_args=check_args))

    def test_get_args_empty(self):
        required = None
        optional = None
        check_args = None
        test_cases = {
            '!test': {},
        }
        self.run_test_get_args(test_cases, required=required, optional=optional, check_args=check_args)

    def test_get_args_required(self):
        required = ['a']
        optional = None
        check_args = None
        test_cases = {
            '!test 123': {'a': '123'},
            '!test "1 2 3"': {'a': '1 2 3'},
            '!test \'1 2 3\'': {'a': '1 2 3'},
        }
        self.run_test_get_args(test_cases, required=required, optional=optional, check_args=check_args)

        required = ['a', 'b']
        test_cases = {
            '!test 123 456': {'a': '123', 'b': '456'},
        }
        self.run_test_get_args(test_cases, required=required, optional=optional, check_args=check_args)

    def test_get_args_required_failure(self):
        required = ['a']
        optional = None
        check_args = None
        test_cases = [
            '!test',
            '!test 1 2 3',
        ]
        self.run_test_get_args_failure(test_cases, required=required, optional=optional, check_args=check_args)

        required = ['a', 'b']
        self.run_test_get_args_failure(test_cases, required=required, optional=optional, check_args=check_args)

    def test_get_args_optional(self):
        required = None
        optional = ['a']
        check_args = None
        test_cases = {
            '!test 123': {'a': '123'},
            '!test "1 2 3"': {'a': '1 2 3'},
            '!test \'1 2 3\'': {'a': '1 2 3'},
            '!test': {'a': None},
        }
        self.run_test_get_args(test_cases, required=required, optional=optional, check_args=check_args)

        optional = ['a', 'b']
        test_cases = {
            '!test 123': {'a': '123', 'b': None},
            '!test "1 2 3"': {'a': '1 2 3', 'b': None},
            '!test \'1 2 3\'': {'a': '1 2 3', 'b': None},
            '!test': {'a': None, 'b': None},
        }
        self.run_test_get_args(test_cases, required=required, optional=optional, check_args=check_args)

        test_cases = {
            '!test 123 456': {'a': '123', 'b': '456'},
        }
        self.run_test_get_args(test_cases, required=required, optional=optional, check_args=check_args)

    def test_get_args_mixed(self):
        required = ['a']
        optional = ['b']
        check_args = None
        test_cases = {
            '!test 123': {'a': '123', 'b': None},
            '!test 123 456': {'a': '123', 'b': '456'},
        }
        self.run_test_get_args(test_cases, required=required, optional=optional, check_args=check_args)

    def test_get_args_mixed_failure(self):
        required = ['a']
        optional = ['b']
        check_args = None
        test_cases = [
            '!test',
            '!test 1 2 3',
        ]
        self.run_test_get_args_failure(test_cases, required=required, optional=optional, check_args=check_args)

    def test_get_args_check_args(self):
        def check_args(args):
            assert(len(args.a.split()) == 1)
            return True

        required = ['a']
        optional = None
        test_cases = {
            '!test 123': {'a': '123'},
        }
        self.run_test_get_args(test_cases, required=required, optional=optional, check_args=check_args)

    def test_get_args_check_args_failure(self):
        def check_args(args):
            assert(len(args.a.split()) == 1)
            return True

        required = ['a']
        optional = None
        test_cases = [
            '!test "1 2 3"',
            '!test \'1 2 3\'',
        ]
        self.run_test_get_args_failure(test_cases, required=required, optional=optional, check_args=check_args)


if __name__ == '__main__':
    unittest.main()
