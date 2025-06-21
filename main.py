import discord
from discord.ext import commands
from discord import app_commands
from flask import Flask
import threading
import os
import time

TOKEN = os.getenv("DISCORD_TOKEN")

app = Flask(__name__)
start_time = time.time()

intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix="!", intents=intents)
tree = app_commands.CommandTree(client)

@app.route("/")
def home():
    return "Bot is online."

@tree.command(name="ping", description="Check latency and uptime")
async def ping(interaction: discord.Interaction):
    latency = round(client.latency * 1000)
    uptime = round(time.time() - start_time)
    hrs, rem = divmod(uptime, 3600)
    mins, secs = divmod(rem, 60)
    uptime_str = f"{int(hrs)}h {int(mins)}m {int(secs)}s"
    await interaction.response.send_message(f"Pong! `{latency}ms` | Uptime: `{uptime_str}`", ephemeral=True)

@client.event
async def on_ready():
    await tree.sync()
    print(f"Logged in as {client.user}")

def run_bot():
    client.run(TOKEN)

# Start bot in a separate thread
threading.Thread(target=run_bot).start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
