import os
import discord
from discord.ext import tasks
from server import keep_alive
from discord import app_commands
from yt_dlp import YoutubeDL

# 接続に必要なオブジェクトを生成
intents = discord.Intents.default()  # デフォルトのIntentsオブジェクトを生成
intents.typing = False  # typingを受け取らないように
intents.members = True  # membersを受け取る
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

if not discord.opus.is_loaded():
  discord.opus.load_opus('./libopus.so')


@client.event
async def on_ready():
  print('Ready!')
  await tree.sync()  #スラッシュコマンドを同期
  myLoop.start()
  myLoop2.start()


@tree.command(name="join", description="音楽機能を使用するためにこのBotを現在のボイスチャンネルに接続させます。")
async def voice_join(interaction: discord.Interaction):
  if interaction.user.voice is None:
    await interaction.response.send_message(
      "あなたはボイスチャンネルに接続していません。",
      ephemeral=True)  #ephemeral=True→「これらはあなただけに表示されています」
    return
  await interaction.user.voice.channel.connect()
  await interaction.response.send_message(
    "ボイスチャンネルに接続しました。", ephemeral=False)  #ephemeral=True→「これらはあなただけに表示されています」


@tree.command(name="quit", description="音楽機能を使用するためにこのBotを現在のボイスチャンネルに接続させます。")
async def voice_quit(interaction: discord.Interaction):
  if interaction.guild.voice_client is None:
    await interaction.response.send_message(
      "ボイスチャンネルに接続していません。",
      ephemeral=True)  #ephemeral=True→「これらはあなただけに表示されています」
    return
  await interaction.guild.voice_client.disconnect()
  await interaction.response.send_message(
    "ボイスチャンネルから切断しました。", ephemeral=False)  #ephemeral=True→「これらはあなただけに表示されています」


@tree.command(name="play", description="音楽機能を使用するためにこのBotを現在のボイスチャンネルに接続させます。")
async def voice_play(interaction: discord.Interaction, url: str):
  if interaction.guild.voice_client is None:
    await interaction.response.send_message(
      "ボイスチャンネルに接続していません。",
      ephemeral=True)  #ephemeral=True→「これらはあなただけに表示されています」
    return
  # ダウンロード条件を設定する。今回は画質・音質ともに最高の動画をダウンロードする
  ydl_opts = {'outtmpl': f'{url}' + '.mp3', 'format': 'bestaudio'}

  # 動画のURLを指定
  with YoutubeDL(ydl_opts) as ydl:
    ydl.download([url])
  interaction.guild.voice_client.play(
    discord.FFmpegPCMAudio("{}.mp3".format(url)))
  await interaction.response.send_message(
    "現在のボイスチャンネルにて**{}**を再生します。".format(url),
    ephemeral=False)  #ephemeral=True→「これらはあなただけに表示されています」


@tasks.loop(seconds=10)  # repeat after every 10 seconds
async def myLoop():
  # work
  guild = client.get_guild(1124309483703763025)
  channel = guild.get_channel(1126754189331148841)
  member_count = len([guild.member_count for m in guild.members
                      if not m.bot])  # doesn't include bots
  await channel.edit(name="Member Count: {}".format(member_count))

  channel = guild.get_channel(1126754191986151444)
  member_count = len([guild.member_count for m in guild.members
                      if m.bot])  # Include bots
  await channel.edit(name="Bot Count: {}".format(member_count))
  print('It works!')


@tasks.loop(seconds=20)  # repeat after every 10 seconds
async def myLoop2():
  # work
  await client.change_presence(activity=discord.Game(
    name="NKコミュニティでニートとして活動中 / https://discord.gg/WesSDs29qT"))


TOKEN = os.getenv("discord")
keep_alive()
try:
  client.run(TOKEN)
except:
  os.system("kill 1")
