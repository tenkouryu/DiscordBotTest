import unittest
from types import SimpleNamespace

from event.on_message.command.member.role_get import _find_members_by_username
from event.on_message.command.member.role_set import _find_member_by_username


class MemberRoleUsernameTests(unittest.TestCase):
    def setUp(self):
        self.member = SimpleNamespace(
            id=123,
            name="example_user",
            display_name="Example Display Name",
        )
        self.guild = SimpleNamespace(members=[self.member])

    def test_role_get_matches_username_case_insensitively(self):
        self.assertEqual(
            _find_members_by_username(self.guild, "EXAMPLE_USER"),
            [self.member],
        )

    def test_role_set_matches_username_case_insensitively(self):
        self.assertIs(
            _find_member_by_username(self.guild, "EXAMPLE_USER"),
            self.member,
        )

    def test_role_lookups_do_not_match_display_name(self):
        self.assertEqual(
            _find_members_by_username(self.guild, "Example Display Name"),
            [],
        )
        self.assertIsNone(
            _find_member_by_username(self.guild, "Example Display Name")
        )


if __name__ == "__main__":
    unittest.main()