import os
from openai import OpenAI
import discord
import nest_asyncio
from dotenv import load_dotenv

#環境変数ファイルを読み込み
load_dotenv()

# 必要なインテントを設定
intents = discord.Intents.default()
intents.message_content = True  # メッセージイベントをリッスンするために必要
#intents.guilds = True    # サーバー（ギルド）関連のイベントをリッスンするために必要

# Client インスタンスを作成
d_client = discord.Client(intents=intents)
o_client = OpenAI()

# discordと接続した時に呼ばれる
@d_client.event
async def on_ready():
    print(f'{d_client.user} としてログインしました')

# メッセージを受信した時に呼ばれる
@d_client.event
async def on_message(message):
    if message.author == d_client.user:
        return

    if message.content.startswith('!talk'):

        #生成開始
        await message.channel.send("生成中...")

        #ユーザーからの入力を受け取る
        user_input = message.content[6:]

        #ChatGPTへのデータを作成
        completion = o_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a Japanese assistant, skilled in explaining complex programming concepts with creative flair."},
            {"role": "user", "content": user_input}
        ]
        )

        await message.channel.send(completion.choices[0].message.content)

# nest_asyncioを適用
nest_asyncio.apply()

# Botを実行
d_client.run(os.getenv("DISCORD_TOKEN"))
