import discord

#----------Bot起動時の処理はここ----------
async def on_ready_main(client):
    # 起動したらターミナルにログイン通知が表示される
    print(f'{client.user}としてログインしました')
    