import discord

# カテゴリーの変更に関する処理はここ
def create_category_channel(guild, category_name):
    existing_category = discord.utils.get(guild.categories, name=category_name)
    if existing_category is None:
        return guild.create_category(category_name)
    else:
        return existing_category