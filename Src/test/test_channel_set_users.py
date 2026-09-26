import unittest
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

from event.on_message.command.channel import set as channel_set
from function.discord.channel import edit_channel


class ChannelSetUserTests(unittest.IsolatedAsyncioTestCase):
    async def test_text_channel_member_access_permissions(self):
        class TextChannelStub:
            pass

        guild = object()
        channel = TextChannelStub()
        channel.guild = guild
        channel.set_permissions = AsyncMock()
        member = SimpleNamespace(guild=guild)

        with patch.object(edit_channel.discord, "TextChannel", TextChannelStub):
            await edit_channel.grant_channel_member_access(channel, member)

        channel.set_permissions.assert_awaited_once_with(
            member,
            view_channel=True,
            send_messages=True,
            read_message_history=True,
        )

    async def test_voice_channel_member_access_permissions(self):
        class VoiceChannelStub:
            pass

        guild = object()
        channel = VoiceChannelStub()
        channel.guild = guild
        channel.set_permissions = AsyncMock()
        member = SimpleNamespace(guild=guild)

        with patch.object(edit_channel.discord, "VoiceChannel", VoiceChannelStub):
            await edit_channel.grant_channel_member_access(channel, member)

        channel.set_permissions.assert_awaited_once_with(
            member,
            view_channel=True,
            connect=True,
            speak=True,
        )

    async def test_user_columns_grant_access_by_case_insensitive_username(self):
        member = SimpleNamespace(id=123, name="ExampleUser")
        guild = SimpleNamespace(id=456, channels=[], members=[member])
        created_channel = object()
        csv_text = (
            "name,type,category,user_1,user_2\n"
            "private,text,,exampleuser,ExampleUser\n"
        )

        with (
            patch.object(
                edit_channel,
                "create_text_channel",
                new=AsyncMock(return_value=created_channel),
            ),
            patch.object(
                edit_channel,
                "grant_channel_member_access",
                new=AsyncMock(),
            ) as grant_access,
        ):
            success_count, _ = await channel_set.set_channels_from_csv(
                guild,
                csv_text,
            )

        self.assertEqual(success_count, 1)
        grant_access.assert_awaited_once_with(created_channel, member)

    async def test_unknown_username_does_not_create_or_change_channel(self):
        guild = SimpleNamespace(id=456, channels=[], members=[])
        csv_text = "name,type,category,user_1\nprivate,text,,missing_user\n"

        with patch.object(
            edit_channel,
            "create_text_channel",
            new=AsyncMock(),
        ) as create_channel:
            success_count, result_csv = await channel_set.set_channels_from_csv(
                guild,
                csv_text,
            )

        self.assertEqual(success_count, 0)
        self.assertIn("ユーザーが見つかりません: missing_user", result_csv.decode("utf-8-sig"))
        create_channel.assert_not_awaited()


if __name__ == "__main__":
    unittest.main()