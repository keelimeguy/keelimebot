import unittest

from keelimebot.commands.usage_command import UsageFormattingError, parse_usage


class UsageCommandTestCase(unittest.TestCase):
    def test_parse_usage_failure(self):
        fail_cases = [
            '<a><b>',
            '<a>[b]',
            '[a][b]',
            '[a]<b>',
            '<a><b> <c>',
            '<a>[b] <c>',
            '[a][b] <c>',
            '[a]<b> <c>',
            '<a><b> [c]',
            '<a>[b] [c]',
            '[a][b] [c]',
            '[a]<b> [c]',
            '<a> <b><c>',
            '<a> [b]<c>',
            '[a] [b]<c>',
            '[a] <b><c>',
            '<a> <b>[c]',
            '<a> [b][c]',
            '[a] [b][c]',
            '[a] <b>[c]',
            '[a] <b>',
            '<a> [b] <c>',
            '[a] [b] <c>',
            '[a] <b> <c>',
            '[a] <b> [c]',
            '<>',
            '[]',
            '<?>',
            '[?]',
            'a',
            ' <a>',
            ' [a]',
            '<a> <a>',
            '<a> [a]',
            '[a] [a]',
            '[a] <a>',
        ]
        for case in fail_cases:
            self.assertRaises(UsageFormattingError, parse_usage, case)

    def test_parse_usage(self):
        success_cases = {
            '<a> <b>': {'names': ['a', 'b'], 'num_required': 2},
            '<a> [b]': {'names': ['a', 'b'], 'num_required': 1},
            '[a] [b]': {'names': ['a', 'b'], 'num_required': 0},
            '<a> <b> <c>': {'names': ['a', 'b', 'c'], 'num_required': 3},
            '<a> <b> [c]': {'names': ['a', 'b', 'c'], 'num_required': 2},
            '<a> [b] [c]': {'names': ['a', 'b', 'c'], 'num_required': 1},
            '[a] [b] [c]': {'names': ['a', 'b', 'c'], 'num_required': 0},
            '<a>': {'names': ['a'], 'num_required': 1},
            '[b]': {'names': ['b'], 'num_required': 0},
        }
        for case, parsed in success_cases.items():
            self.assertEqual(parsed, parse_usage(case))


if __name__ == '__main__':
    unittest.main()
