import discord


def can_manage_roles(member: discord.Member | discord.User) -> bool:
    """Return whether a guild user can manage roles, including administrators."""
    permissions = getattr(member, "guild_permissions", None)
    return bool(
        permissions
        and (permissions.manage_roles or permissions.administrator)
    )


def can_manage_channels(member: discord.Member | discord.User) -> bool:
    """Return whether a guild user can manage channels, including administrators."""
    permissions = getattr(member, "guild_permissions", None)
    return bool(
        permissions
        and (permissions.manage_channels or permissions.administrator)
    )