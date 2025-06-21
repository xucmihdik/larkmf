import discord
from discord.ext import commands
from discord import app_commands
from flask import Flask
from threading import Thread
import os
import time

TOKEN = os.getenv("DISCORD_TOKEN")

app = Flask('')

@app.route('/')
def home():
    return "Bot is alive!"

def run():
    app.run(host='0.0.0.0', port=8080)

Thread(target=run).start()

intents = discord.Intents.default()
client = commands.Bot(command_prefix="!", intents=intents)
tree = app_commands.CommandTree(client)
start_time = time.time()

@client.event
async def on_ready():
    await tree.sync()
    print(f'Logged in as {client.user}')

@tree.command(name="ping", description="Check bot latency and uptime")
async def ping(interaction: discord.Interaction):
    latency = round(client.latency * 1000)
    uptime = round(time.time() - start_time)
    hrs, rem = divmod(uptime, 3600)
    mins, secs = divmod(rem, 60)
    uptime_str = f"{int(hrs)}h {int(mins)}m {int(secs)}s"
    await interaction.response.send_message(f"🏓 Pong!\nLatency: `{latency}ms`\nUptime: `{uptime_str}`", ephemeral=True)

client.run(TOKEN)
